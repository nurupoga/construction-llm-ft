# NEXT_TASK（Mac Mini側Claude起動時に最初に読むファイル）

## あなたへの指示

このプロジェクトの Mac Mini 側 Claude Code セッションです。
以下のドキュメントを順に読んでから着手してください:

1. `CLAUDE.md` - プロジェクト全体方針・進捗共有ルール（**確定済み判断セクション必読**）
2. `WORK_LOG.md` - これまでの経緯（**最新末尾の 2026-05-10 セッションを必ず読む**）
3. `docs/freeze-spec.md` - 比較条件凍結仕様
4. `docs/data-sources.md` - 12PDF入手元（HTTP 200確認済）
5. `docs/license-check.md` - 著作権判定（30条の4でOK、配布NG）

## 現在のステータス（2026-05-10 更新）

- **試験種スコープ**: 宅地建物取引士（宅建士）1試験、2016-2025 の10年分（500問オーダー）
- **公開方針**: **全非公開**（HF/Zenn/GitHub public は **すべてしない**）
- **進行中**: Phase 0 / Phase 2-1〜2-3 完了
- **直近のブロッカー**: なし（ユーザー判断4件すべて確定、Colab自動保存はユーザー設定中だが Phase 2-4/2-5 は並行で進められる）

## 2026-05-10 確定済みのユーザー判断

ローカル新セッションでユーザーから以下4件の判断を取得済。これに従って進めてください。

| 項目 | 決定 |
|---|---|
| 2020/2021の10月/12月分割実施分 | **両方train**（年度内で別問題、リーク無し） |
| Phase 3 合成解説（Gemini API） | **不実施**（PoC後に再検討） |
| OCRパイプライン構築場所 | **Colab上**（Mac Miniにtesseract不要） |
| Colab自動保存 | ユーザー設定中（Drive `/content/drive/MyDrive/construction-llm-ft/checkpoints/`） |

## 次の着手対象（優先順）

### A. Phase 2-4: PDF→構造化（テキスト抽出）

**経路1: 2023-2025 の3PDF（pdfplumber直抽出、Mac Miniローカル）**
- `data/raw/takken/2023/`, `2024/`, `2025/` 配下のPDF
- `scripts/extract_pdf_text.py` を作成し `pdfplumber` で問題文・選択肢・正答を抽出
- 出力: `data/jsonl/intermediate/<year>.json`（中間構造化データ、未整形）

**経路2: 2016-2022 の9PDF（OCR、Colab上で実行）**
- 対象: 2016, 2017, 2018, 2019, 2020-oct, 2020-dec, 2021-oct, 2021-dec, 2022
- Colabノート `notebooks/ocr_pipeline.ipynb` を新規作成
  - Driveマウント → `data/raw/takken/<year>/*.pdf` を読み込み
  - `pdftoppm` でPNG化 → `tesseract -l jpn` でOCR
  - 出力を `data/jsonl/intermediate/<year>.json` でDriveに保存し、Mac Miniにgit経由で持ち帰る
- 既知の罠: 2023年度のファイル名全角スペース（既にダウンロード済なのでファイル名は問題なし、テキスト内容のみ注意）

### B. Phase 2-5: JSONL整形（Mac Miniローカル）

- 中間データ（intermediate）を `freeze-spec.md` 準拠の `{instruction, input, output}` 形式に変換
- `scripts/build_jsonl.py` を作成
- 出力:
  - `data/jsonl/train/takken_train.jsonl`（2016-2024、500問 - 50問 = **約500問** ※ 2020/2021が4セットあるため約550問）
  - `data/jsonl/eval/takken_eval.jsonl`（2025、50問）
- 形式（freeze-spec.md準拠）:
  ```json
  {"instruction": "次の宅建試験問題に対し、最も適切な選択肢の番号(1-4)と短い理由を日本語で答えよ。",
   "input": "問題文 + 選択肢1〜4",
   "output": "3\n理由: ..."}
  ```
- **output方針**: 正解選択肢番号 + 1-2行の短い理由文のみ（合成解説は実施しない）

### C. Phase 1: PoC（Colab自動保存準備完了後）

- Colab自動保存が完了したらユーザーがWORK_LOG.mdに「Colab準備完了、Phase 1着手OK」と書きます
- それを確認したら Qwen2.5-7B-Instruct のベースライン（FT前正答率）取得 → Phase 4-5 へ

### D. Phase 4-5: ベースライン + FT（Colab）

- ベースライン: Qwen2.5-7B-Instruct anonymous DL → eval 50問で正答率測定
- FT: QLoRA(4bit) + Unsloth で2-3 epoch、lr 2e-4
- checkpointは Drive `/content/drive/MyDrive/construction-llm-ft/checkpoints/takken-qwen25-7b/`

### E. Phase 6: 評価・前後比較

- 同一スクリプト・同一プロンプトで FT前後の正答率比較
- 出力: 1枚のグラフ（`results/score_comparison.png`）

### F. Phase 7: 公開 → 不要（全非公開で完了）

## ユーザー判断が必要になったら

`WAITING_FOR_USER.md` を作成して以下フォーマットで内容を書き、git commit & push してください。

```markdown
## 待機中: <タイトル>

### 状況
（何をやっていて、なぜ止まったか）

### 必要な判断
（具体的に何を決めてほしいか）

### 推奨案
（あなたのおすすめ）

### 影響
（決まらないと何が止まるか）

作成日時: YYYY-MM-DD HH:MM
```

## 進捗共有ルール（再掲）

- 節目ごとに WORK_LOG.md 更新 → commit → push
- 最低1時間に1回はpush（長時間処理中なら「実行中」ステータス）
- ユーザー判断必要時は WAITING_FOR_USER.md 作成

## 着手の確認

着手前に WORK_LOG.md 末尾に「2026-05-XX Mac Mini Claudeセッション再開、Phase 2-4着手」と書いてpushしてから始めてください。
