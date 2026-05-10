#!/usr/bin/env python3
"""
Phase 2-5: 中間構造化 JSON (data/jsonl/intermediate/*.json) を
freeze-spec.md §2 準拠の Alpaca 風 instruction-tuning JSONL に変換する。

入力:
    data/jsonl/intermediate/<year>[_<session>].json
        例: 2023.json, 2024.json, 2025.json, 2020_oct.json, 2020_dec.json
        スキーマは scripts/extract_pdf_text.py の出力に準拠。

出力:
    data/jsonl/train/takken_train.jsonl   (2016〜2024、最終550問想定)
    data/jsonl/eval/takken_eval.jsonl     (2025のみ、50問)
    data/jsonl/manifest.json              (含めた年度・件数・SHA256・生成時刻)

使い方:
    python3 scripts/build_jsonl.py
    引数なし。intermediate ディレクトリ内の全ファイルを動的に読み込む。

設計方針:
    - クリーニングは保守的（NFKC, 空白正規化, (cid:NNNN) 除去, 問番号ヘッダ削除）
    - train / eval を物理的に分離（出力ディレクトリも分離）
    - 冪等: 再実行で同じ出力（ただし manifest の built_at/checksum は更新される）
    - eval リーク検出: train と eval の id 重複は exit 1
    - 2025 が無ければ eval が空になりエラー、2024以前のいずれも無ければ train が空でも警告して続行
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
INTERMEDIATE_DIR = REPO_ROOT / "data" / "jsonl" / "intermediate"
TRAIN_DIR = REPO_ROOT / "data" / "jsonl" / "train"
EVAL_DIR = REPO_ROOT / "data" / "jsonl" / "eval"
MANIFEST_PATH = REPO_ROOT / "data" / "jsonl" / "manifest.json"

TRAIN_OUT = TRAIN_DIR / "takken_train.jsonl"
EVAL_OUT = EVAL_DIR / "takken_eval.jsonl"

# freeze-spec.md §2 で固定された instruction 文言
INSTRUCTION_TEXT = (
    "以下は宅地建物取引士資格試験の四択問題です。"
    "最も適切な選択肢の番号(1〜4)を1つだけ半角数字で答えよ。"
    "番号以外は出力しないこと。"
)

# train/eval 分割ルール (CLAUDE.md / freeze-spec.md §1)
EVAL_YEARS: set[int] = {2025}
TRAIN_YEARS: set[int] = {2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024}

# 期待される intermediate ファイル一覧 (year, session)。OCR 待ちの欠落検出用。
EXPECTED_FILES: list[tuple[int, str | None]] = [
    (2016, None),
    (2017, None),
    (2018, None),
    (2019, None),
    (2020, "oct"),
    (2020, "dec"),
    (2021, "oct"),
    (2021, "dec"),
    (2022, None),
    (2023, None),
    (2024, None),
    (2025, None),
]


# ---- クリーニング -----------------------------------------------------------

# (cid:1234) のようなフォント未復号トークン
_CID_RE = re.compile(r"\(cid:\d+\)")
# 「【問 1】」「問1」「問 １」など、問題文先頭に残った問番号ヘッダ
_QHEADER_RE = re.compile(r"^[\s　]*(?:【\s*問\s*[0-9０-９]+\s*】|問[\s　]*[0-9０-９]+[\s　]*[\.．、]?)")
# 連続空白（改行含む全種）
_WS_RE = re.compile(r"\s+")


def clean_text(s: str, *, strip_qheader: bool = False) -> str:
    """中間JSONのテキストフィールドを正規化する。

    手順:
      1. None / 空文字なら空文字を返す
      2. NFKC 正規化（全角空白→半角、全角数字→半角など）
      3. (cid:NNNN) を削除
      4. (オプション) 問題文先頭の「【問 N】」「問N」を削除
      5. 連続空白 (改行含む) を半角空白1つに畳み込み、両端を strip
    """
    if not s:
        return ""
    t = unicodedata.normalize("NFKC", s)
    t = _CID_RE.sub("", t)
    if strip_qheader:
        # 先頭の問番号ヘッダのみ除去（複数回ヒットすることは想定しない）
        t = _QHEADER_RE.sub("", t, count=1)
    t = _WS_RE.sub(" ", t).strip()
    return t


# ---- レコード生成 -----------------------------------------------------------

def file_id_to_year_session(stem: str) -> tuple[int, str | None]:
    """ファイル名 stem (例: '2023', '2020_oct') から (year, session) を取り出す。"""
    parts = stem.split("_")
    if len(parts) == 1:
        return int(parts[0]), None
    if len(parts) == 2:
        return int(parts[0]), parts[1]
    raise ValueError(f"unexpected intermediate file stem: {stem!r}")


def build_record(q: dict[str, Any]) -> dict[str, Any] | None:
    """中間JSONの question dict 1件を JSONL レコードに変換する。

    返り値:
        {"id", "instruction", "input", "output"} の dict
        変換不能（選択肢欠落など）なら None
    """
    qid = q.get("id")
    qtext_raw = q.get("question_text") or ""
    choices_raw = q.get("choices") or {}
    correct = q.get("correct_answer")

    if not qid:
        return None

    # output 検証
    if correct not in {"1", "2", "3", "4"}:
        return None

    # 4選択肢が揃っているか
    if not all(k in choices_raw for k in ("1", "2", "3", "4")):
        return None
    cleaned_choices: dict[str, str] = {}
    for k in ("1", "2", "3", "4"):
        cv = clean_text(choices_raw[k])
        if not cv:
            return None
        cleaned_choices[k] = cv

    # question_text 正規化（先頭の問番号ヘッダ削除）
    qtext = clean_text(qtext_raw, strip_qheader=True)
    if not qtext:
        return None

    input_text = (
        f"問題: {qtext}\n\n"
        f"1. {cleaned_choices['1']}\n"
        f"2. {cleaned_choices['2']}\n"
        f"3. {cleaned_choices['3']}\n"
        f"4. {cleaned_choices['4']}"
    )

    return {
        "id": qid,
        "instruction": INSTRUCTION_TEXT,
        "input": input_text,
        "output": correct,
    }


# ---- バリデーション ---------------------------------------------------------

def validate(
    train_records: list[dict[str, Any]],
    eval_records: list[dict[str, Any]],
    train_years_present: set[int],
    train_session_files: int,
) -> list[str]:
    """全レコードを検証してエラーメッセージのリストを返す（空ならOK）。"""
    errors: list[str] = []

    # 1. id 重複（train 内、eval 内、train×eval）
    train_ids = [r["id"] for r in train_records]
    eval_ids = [r["id"] for r in eval_records]
    if len(train_ids) != len(set(train_ids)):
        dups = [x for x in set(train_ids) if train_ids.count(x) > 1]
        errors.append(f"duplicate ids in train: {dups[:10]}")
    if len(eval_ids) != len(set(eval_ids)):
        dups = [x for x in set(eval_ids) if eval_ids.count(x) > 1]
        errors.append(f"duplicate ids in eval: {dups[:10]}")
    cross = set(train_ids) & set(eval_ids)
    if cross:
        errors.append(f"id leakage between train and eval: {sorted(cross)[:10]}")

    # 2. output 形式
    for split_name, recs in (("train", train_records), ("eval", eval_records)):
        bad = [r["id"] for r in recs if r["output"] not in {"1", "2", "3", "4"}]
        if bad:
            errors.append(f"invalid output in {split_name}: {bad[:10]}")

    # 3. input に 1.〜4. の選択肢4つが含まれる（行頭ベース）
    pat = re.compile(r"(?m)^[1-4]\. ")
    for split_name, recs in (("train", train_records), ("eval", eval_records)):
        bad = []
        for r in recs:
            ids_in_line = pat.findall(r["input"])
            # ids_in_line は ["1. ", "2. ", "3. ", "4. "] 相当
            nums = sorted({s[0] for s in ids_in_line})
            if nums != ["1", "2", "3", "4"]:
                bad.append(r["id"])
        if bad:
            errors.append(f"{split_name} records missing 4 choice lines: {bad[:10]}")

    # 4. instruction 固定確認
    for split_name, recs in (("train", train_records), ("eval", eval_records)):
        bad = [r["id"] for r in recs if r["instruction"] != INSTRUCTION_TEXT]
        if bad:
            errors.append(f"{split_name} records have non-fixed instruction: {bad[:10]}")

    # 5. eval 件数
    if len(eval_records) != 50:
        errors.append(
            f"eval count must be exactly 50 (2025 only); got {len(eval_records)}"
        )

    # 6. train 件数 = 含めた intermediate ファイル数 × 50
    expected_train = train_session_files * 50
    if len(train_records) != expected_train:
        errors.append(
            f"train count mismatch: got {len(train_records)}, "
            f"expected {expected_train} ({train_session_files} files × 50)"
        )

    return errors


# ---- I/O ヘルパ -------------------------------------------------------------

def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False))
            f.write("\n")


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---- メイン処理 -------------------------------------------------------------

def main() -> int:
    if not INTERMEDIATE_DIR.exists():
        print(
            f"[ERROR] intermediate directory not found: {INTERMEDIATE_DIR}",
            file=sys.stderr,
        )
        return 1

    # intermediate ファイルを動的にスキャン (manifest.json は除外)
    intermediate_files = sorted(
        p
        for p in INTERMEDIATE_DIR.glob("*.json")
        if p.name != "manifest.json"
    )
    if not intermediate_files:
        print(f"[ERROR] no intermediate JSON files in {INTERMEDIATE_DIR}", file=sys.stderr)
        return 1

    # 期待ファイル一覧 vs 実在ファイル一覧
    present_keys: set[tuple[int, str | None]] = set()

    train_records: list[dict[str, Any]] = []
    eval_records: list[dict[str, Any]] = []
    train_session_files = 0

    include_entries: list[dict[str, Any]] = []

    for jf in intermediate_files:
        try:
            year, session = file_id_to_year_session(jf.stem)
        except ValueError as e:
            print(f"[WARN] skip {jf.name}: {e}", file=sys.stderr)
            continue

        present_keys.add((year, session))

        with jf.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        questions = payload.get("questions", [])
        records: list[dict[str, Any]] = []
        for q in questions:
            rec = build_record(q)
            if rec is None:
                print(
                    f"[WARN] {jf.name}: skip question {q.get('id', '?')} "
                    f"(missing/invalid choices or answer)",
                    file=sys.stderr,
                )
                continue
            records.append(rec)

        # train/eval 仕分け
        if year in EVAL_YEARS:
            eval_records.extend(records)
            split = "eval"
        elif year in TRAIN_YEARS:
            train_records.extend(records)
            train_session_files += 1
            split = "train"
        else:
            print(
                f"[WARN] {jf.name}: year {year} is outside train/eval scope; skipped",
                file=sys.stderr,
            )
            continue

        print(
            f"[load] {jf.name}: year={year} session={session or '-'} "
            f"questions={len(records)} -> {split}",
            file=sys.stderr,
        )
        include_entries.append(
            {
                "year": year,
                "session": session,
                "split": split,
                "source": str(jf.relative_to(REPO_ROOT)),
                "count": len(records),
            }
        )

    # 欠落年度 (OCR 待ち) を計算
    missing_keys = [
        (y, s) for (y, s) in EXPECTED_FILES if (y, s) not in present_keys
    ]
    if missing_keys:
        formatted = ", ".join(f"{y}{('_' + s) if s else ''}" for y, s in missing_keys)
        print(f"[info] missing intermediate files (OCR pending?): {formatted}", file=sys.stderr)

    # train で実在した「セッション数」を計算（バリデーション用）
    train_years_present: set[int] = {
        e["year"] for e in include_entries if e["split"] == "train"
    }

    # ソート: id 順で並べると再現性がよい
    train_records.sort(key=lambda r: r["id"])
    eval_records.sort(key=lambda r: r["id"])

    # 書き出し
    write_jsonl(TRAIN_OUT, train_records)
    write_jsonl(EVAL_OUT, eval_records)

    print(
        f"[write] train: {len(train_records)} records -> {TRAIN_OUT.relative_to(REPO_ROOT)}",
        file=sys.stderr,
    )
    print(
        f"[write] eval:  {len(eval_records)} records -> {EVAL_OUT.relative_to(REPO_ROOT)}",
        file=sys.stderr,
    )

    # バリデーション
    errors = validate(
        train_records,
        eval_records,
        train_years_present,
        train_session_files,
    )
    if errors:
        print("[FAIL] validation errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        # manifest はエラー時も書き出さない方が安全
        return 1

    print("[ok] all validations passed", file=sys.stderr)

    # manifest
    manifest = {
        "exam_code": "takken",
        "built_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "instruction_text": INSTRUCTION_TEXT,
        "include_years": sorted(
            include_entries, key=lambda e: (e["year"], e["session"] or "")
        ),
        "train_count": len(train_records),
        "eval_count": len(eval_records),
        "missing": [
            {"year": y, "session": s} for (y, s) in missing_keys
        ],
        "outputs": {
            "train": {
                "path": str(TRAIN_OUT.relative_to(REPO_ROOT)),
                "sha256": sha256_of_file(TRAIN_OUT),
                "bytes": TRAIN_OUT.stat().st_size,
            },
            "eval": {
                "path": str(EVAL_OUT.relative_to(REPO_ROOT)),
                "sha256": sha256_of_file(EVAL_OUT),
                "bytes": EVAL_OUT.stat().st_size,
            },
        },
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[manifest] wrote {MANIFEST_PATH.relative_to(REPO_ROOT)}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
