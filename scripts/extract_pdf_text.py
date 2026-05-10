#!/usr/bin/env python3
"""
RETIO 宅建士 過去問 PDF (問題 + 正答) を pdfplumber で抽出して
中間構造化 JSON を data/jsonl/intermediate/<year>.json に書き出すスクリプト。

Phase 2-4 経路1。出力スキーマは CLAUDE.md / Phase 2-4 仕様に従う。
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pdfplumber

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw" / "takken"
OUT_DIR = REPO_ROOT / "data" / "jsonl" / "intermediate"

# 年度→PDFパス
PDF_BY_YEAR: dict[int, Path] = {
    2023: RAW_DIR / "2023" / "R5-q_a.pdf",
    2024: RAW_DIR / "2024" / "R6_question_answer.pdf",
    2025: RAW_DIR / "2025" / "R7_question_answer.pdf",
}

# ---- regex / 文字種ユーティリティ -------------------------------------------------

# 「【問 1】」「【問 １】」「【問1】」など。間の空白は半角/全角どちらでも 0..n 個許容
QUESTION_HEADER_RE = re.compile(r"【\s*問\s*([0-9０-９]+)\s*】")

# 行頭の選択肢番号: "1 ", "1　", "1 .", "1）" など。ここでは「半角数字 + 空白(半角/全角)」を主軸とする
CHOICE_LINE_RE = re.compile(r"^([1-4])[\s　]+(.*)$")


def to_int_zenhan(s: str) -> int:
    """全角数字も含めて int 化。"""
    return int(unicodedata.normalize("NFKC", s))


def normalize_answer_token(token: str) -> Optional[str]:
    """正答テーブルから取り出したトークン (半角/全角の 1〜4) を半角文字列にする。
    1〜4 でなければ None を返す。
    """
    nfkc = unicodedata.normalize("NFKC", token)
    if nfkc in {"1", "2", "3", "4"}:
        return nfkc
    return None


# ---- データクラス ------------------------------------------------------------

@dataclass
class Question:
    id: str
    number: int
    question_text: str
    choices: dict[str, str] = field(default_factory=dict)
    correct_answer: Optional[str] = None
    raw_block: str = ""


# ---- 抽出ロジック ------------------------------------------------------------

def extract_full_text(pdf_path: Path) -> tuple[str, list[str]]:
    """PDF全体テキスト(改行保持)と、ページ単位テキスト一覧を返す。"""
    pages: list[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            pages.append(txt)
    full = "\n".join(pages)
    return full, pages


def parse_questions_from_text(full_text: str, year: int) -> list[Question]:
    """全テキストから 50 問をパースして返す。

    アプローチ:
      1. 「【問 N】」マッチ位置で全文を分割。
      2. 各ブロックを「問題本文 + 4選択肢」に分割（行ベースで先頭が "1 ".."4 " となる行を選択肢開始と扱う）。
      3. ノイズ行（ページ番号、ヘッダ「AABB..iinndddd」、年度表記など）はスキップ。
    """
    matches = list(QUESTION_HEADER_RE.finditer(full_text))

    # 各 qno について「全てのマッチ候補」を集め、最後に「4選択肢が取れる最良の候補」を採用する。
    # こうすることで、解答冊子の参照（「【問 46】から…」のような注意書き）に引っかかった
    # 短いブロックが先に拾われても、本物の問題ブロックに上書きされる。
    candidates: dict[int, list[Question]] = {}

    for idx, m in enumerate(matches):
        qno = to_int_zenhan(m.group(1))
        if not (1 <= qno <= 50):
            continue

        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(full_text)
        raw_block = full_text[start:end]

        question_text, choices = split_question_block(raw_block)

        qid = f"takken_{year}_q{qno:03d}"
        cand = Question(
            id=qid,
            number=qno,
            question_text=question_text,
            choices=choices,
            raw_block=raw_block,
        )
        candidates.setdefault(qno, []).append(cand)

    questions: list[Question] = []
    for qno, cands in candidates.items():
        # 優先順位:
        #  1. choices が 4 つ揃っていて全選択肢が非空
        #  2. choices が多い方
        #  3. raw_block の長さが長い方（より大きいテキストを含む）
        def score(q: Question) -> tuple[int, int, int]:
            full_choices = (
                len(q.choices) == 4
                and all(v.strip() for v in q.choices.values())
            )
            return (1 if full_choices else 0, len(q.choices), len(q.raw_block))

        best = max(cands, key=score)
        questions.append(best)

    questions.sort(key=lambda q: q.number)
    return questions


# ページフッタなどスキップしたい行のパターン
NOISE_LINE_PATTERNS = [
    re.compile(r"^\s*AABB\..*"),      # 「AABB..iinndddd 11 22002255..」フッタ
    re.compile(r"^\s*-?\s*\d{1,3}\s*-?\s*$"),  # 単独のページ番号
]


def is_noise_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False  # 空行は構造保持上残す（後で扱い）
    for pat in NOISE_LINE_PATTERNS:
        if pat.match(s):
            return True
    return False


def split_question_block(raw_block: str) -> tuple[str, dict[str, str]]:
    """1問分のテキストブロックから問題本文と選択肢4つを取り出す。"""
    lines = raw_block.splitlines()
    # 先頭行は「【問 N】」を含む。ヘッダ部はそのまま問題本文側に残す。

    # ノイズ行除去
    cleaned: list[str] = []
    for ln in lines:
        if is_noise_line(ln):
            continue
        cleaned.append(ln)

    # 選択肢開始行を 4 つ見つける
    choice_starts: list[int] = []  # cleaned のインデックス
    expected_next = 1
    for i, ln in enumerate(cleaned):
        s = ln.lstrip()
        m = CHOICE_LINE_RE.match(s)
        if m and int(m.group(1)) == expected_next:
            choice_starts.append(i)
            expected_next += 1
            if expected_next > 4:
                break

    if len(choice_starts) < 4:
        # 4択を見つけられなかった → 全文を question_text に入れて choices 空で返す
        return _join_lines(cleaned).strip(), {}

    # 問題本文 = 0 .. choice_starts[0]-1 の範囲
    body_lines = cleaned[: choice_starts[0]]
    # 末尾改行をクリーンに
    question_text = _join_lines(body_lines).strip()

    choices: dict[str, str] = {}
    for k in range(4):
        i_start = choice_starts[k]
        i_end = choice_starts[k + 1] if k + 1 < 4 else len(cleaned)
        choice_lines = cleaned[i_start:i_end]
        # 先頭行は "N " を取り除く
        first = choice_lines[0].lstrip()
        m = CHOICE_LINE_RE.match(first)
        rest = m.group(2) if m else first
        merged = _join_lines([rest] + choice_lines[1:]).strip()
        choices[str(k + 1)] = merged

    return question_text, choices


def _join_lines(lines: list[str]) -> str:
    """改行を保ったまま結合（後段で必要なら正規化する）。
    PDF 由来の不要な行末改行は残しておく。
    """
    return "\n".join(lines)


# ---- 正答抽出 -------------------------------------------------------------

def parse_answers_from_text(full_text: str, year: int) -> dict[int, str]:
    """正答テーブルから問1..問50の正答を抽出する。

    フォーマット差:
      - 2023, 2025: 「問 １ 問 ２ ...」のヘッダ付きブロックがあり、続いて10個の数字が並ぶ。
      - 2024: ヘッダなし。最終ページに 10 個 × 5 行で 50 個の数字（半角）が並ぶ。
    どちらにも対応するため、まず「合格判定基準」付きの解答テーブルを優先で探し、
    無ければ最終ページの数字列に fall back する。
    """
    # ストラテジ A: 「問 １〜問１０」「問１１〜問２０」… の各テーブル行から正答を取り出す
    answers = _parse_answers_with_headers(full_text)
    if len(answers) == 50:
        return answers

    # ストラテジ B: 最終 N 行から「行内に 10 個の半角/全角 1-4」が連続する 5 行を探す
    answers_b = _parse_answers_simple_grid(full_text)
    if len(answers_b) == 50:
        return answers_b

    # 部分的にしか取れなかった場合は取れた方を優先
    return answers if len(answers) > len(answers_b) else answers_b


_HEADER_TABLE_BLOCK_RE = re.compile(
    r"問[\s　]*[0-9０-９]+(?:[\s　]+問[\s　]*[0-9０-９]+){0,9}\s*\n([^\n]+)"
)


def _parse_answers_with_headers(full_text: str) -> dict[int, str]:
    """「問 １ 問 ２ ... 問１０」のような行の直後の行に正答が並ぶ前提で抽出。"""
    answers: dict[int, str] = {}
    lines = full_text.splitlines()
    for i, line in enumerate(lines):
        # ヘッダ行: 「問」を含む数字ヘッダが 5 個以上並ぶ
        if line.count("問") < 5:
            continue
        # 数字を抽出
        header_nums = re.findall(r"問[\s　]*([0-9０-９]+)", line)
        try:
            header_ints = [to_int_zenhan(x) for x in header_nums]
        except ValueError:
            continue
        if not all(1 <= n <= 50 for n in header_ints):
            continue
        # 直後の行から正答を取得
        if i + 1 >= len(lines):
            continue
        ans_line = lines[i + 1]
        # 半角/全角の 1〜4 を順序通り拾う
        # 全角数字「１２３４」も対象
        tokens = re.findall(r"[1-4１２３４]", ans_line)
        if len(tokens) < len(header_ints):
            continue
        for n, t in zip(header_ints, tokens):
            v = normalize_answer_token(t)
            if v is not None:
                answers[n] = v
    return answers


def _parse_answers_simple_grid(full_text: str) -> dict[int, str]:
    """最終ページ風の 10×5 グリッドからの抽出。"""
    answers: dict[int, str] = {}
    lines = [ln for ln in full_text.splitlines() if ln.strip()]
    # 末尾から走査
    candidate_rows: list[list[str]] = []
    for ln in reversed(lines):
        # 行内の半角/全角 1-4 を抜く
        tokens = re.findall(r"[1-4１２３４]", ln)
        if len(tokens) == 10:
            candidate_rows.append(tokens)
            if len(candidate_rows) == 5:
                break
        elif candidate_rows and len(tokens) != 10:
            # 連続性が切れた
            break
    if len(candidate_rows) != 5:
        return {}
    candidate_rows.reverse()  # 上から順に
    for row_idx, row in enumerate(candidate_rows):
        for col_idx, t in enumerate(row):
            n = row_idx * 10 + col_idx + 1
            v = normalize_answer_token(t)
            if v is not None:
                answers[n] = v
    return answers


# ---- メイン処理 -------------------------------------------------------------

def extract_year(year: int, pdf_path: Path) -> dict:
    print(f"[{year}] opening {pdf_path}", file=sys.stderr)
    full_text, _pages = extract_full_text(pdf_path)

    questions = parse_questions_from_text(full_text, year)
    answers = parse_answers_from_text(full_text, year)

    # 正答を割当
    for q in questions:
        q.correct_answer = answers.get(q.number)

    # 検証
    n_q = len(questions)
    n_with_answer = sum(1 for q in questions if q.correct_answer in {"1", "2", "3", "4"})
    n_with_choices = sum(1 for q in questions if len(q.choices) == 4 and all(v.strip() for v in q.choices.values()))
    n_nonempty_text = sum(1 for q in questions if q.question_text.strip())

    print(f"[{year}] questions parsed: {n_q}", file=sys.stderr)
    print(f"[{year}] questions with 4 non-empty choices: {n_with_choices}", file=sys.stderr)
    print(f"[{year}] questions with non-empty body text:  {n_nonempty_text}", file=sys.stderr)
    print(f"[{year}] questions with answer 1-4:           {n_with_answer}", file=sys.stderr)
    print(f"[{year}] answers found total:                 {len(answers)}", file=sys.stderr)

    if n_q != 50:
        print(f"[{year}] WARNING: expected 50 questions, got {n_q}", file=sys.stderr)
    missing_q = [n for n in range(1, 51) if not any(q.number == n for q in questions)]
    if missing_q:
        print(f"[{year}] WARNING: missing question numbers: {missing_q}", file=sys.stderr)
    missing_a = [n for n in range(1, 51) if n not in answers]
    if missing_a:
        print(f"[{year}] WARNING: missing answer numbers:   {missing_a}", file=sys.stderr)

    payload = {
        "exam_code": "takken",
        "year": year,
        "session": None,
        "source_pdf": str(pdf_path.relative_to(REPO_ROOT)),
        "extracted_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "extractor": "pdfplumber",
        "extractor_version": pdfplumber.__version__,
        "stats": {
            "num_questions": n_q,
            "num_with_4_choices": n_with_choices,
            "num_with_answer": n_with_answer,
            "num_answers_found": len(answers),
            "missing_question_numbers": missing_q,
            "missing_answer_numbers": missing_a,
        },
        "questions": [
            {
                "id": q.id,
                "number": q.number,
                "question_text": q.question_text,
                "choices": q.choices,
                "correct_answer": q.correct_answer,
                "raw_block": q.raw_block,
            }
            for q in questions
        ],
    }
    return payload


def write_intermediate_json(year: int, payload: dict) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{year}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"[{year}] wrote {out_path}", file=sys.stderr)
    return out_path


def update_intermediate_manifest(results: list[dict]) -> Path:
    """data/jsonl/intermediate/manifest.json を上書きする。"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT_DIR / "manifest.json"
    manifest = {
        "exam_code": "takken",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "extractor": "pdfplumber",
        "extractor_version": pdfplumber.__version__,
        "entries": [
            {
                "year": r["year"],
                "source_pdf": r["source_pdf"],
                "output_json": str((OUT_DIR / f"{r['year']}.json").relative_to(REPO_ROOT)),
                "extracted_at": r["extracted_at"],
                "stats": r["stats"],
            }
            for r in results
        ],
    }
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[manifest] wrote {manifest_path}", file=sys.stderr)
    return manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--year", type=int, help="抽出対象年度 (2023/2024/2025)")
    g.add_argument("--all", action="store_true", help="2023/2024/2025 を一括抽出")
    args = parser.parse_args()

    if args.all:
        years = sorted(PDF_BY_YEAR.keys())
    else:
        if args.year not in PDF_BY_YEAR:
            print(f"unknown year {args.year}; supported: {sorted(PDF_BY_YEAR.keys())}", file=sys.stderr)
            return 2
        years = [args.year]

    results: list[dict] = []
    for year in years:
        pdf_path = PDF_BY_YEAR[year]
        if not pdf_path.exists():
            print(f"[{year}] ERROR: pdf not found: {pdf_path}", file=sys.stderr)
            continue
        payload = extract_year(year, pdf_path)
        write_intermediate_json(year, payload)
        results.append(payload)

    if results:
        update_intermediate_manifest(results)

    # exit code: 失敗年度ありなら 1
    ok = all(
        r["stats"]["num_questions"] == 50
        and r["stats"]["num_with_answer"] == 50
        and r["stats"]["num_with_4_choices"] == 50
        for r in results
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
