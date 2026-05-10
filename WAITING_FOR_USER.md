## 待機中: OCRノート実行 + Phase 1 PoC ベースライン取得

### 状況

Mac Mini Claude が朝までの作業を完了し、以下の状態：

- **Phase 2-4 経路1 完了**: pdfplumberで 2023/2024/2025 PDFから 50問×3 = 150問抽出成功（`data/jsonl/intermediate/{2023,2024,2025}.json`）
- **Phase 2-4 経路2 ノート雛形完成**: `notebooks/ocr_pipeline.ipynb` (22セル、Colab CPU想定)。実行待ち
- **Phase 2-5 完了**: `scripts/build_jsonl.py` で train 100件 + eval 50件 + manifest 生成済（validation全パス、id重複0）

これ以降は **Colab 上での実行が必要** で、Mac Mini Claude では進められない。

### 必要な判断・作業

#### 作業1: OCRノートの Colab 実行（30-45分）

1. Mac Mini Chrome で以下のいずれかの方法でノートを開く:
   - **方法A (推奨)**: Drive の `MyDrive/construction-llm-ft/notebooks/ocr_pipeline.ipynb` を右クリック→「Colabで開く」
     - その前に `git pull` してあるリポジトリを Drive へ同期する手順が必要（同期方法はユーザー判断）
   - **方法B**: GitHub から直接開く: `https://colab.research.google.com/github/nurupoga/construction-llm-ft/blob/main/notebooks/ocr_pipeline.ipynb`
2. 「ランタイム → すべてのセルを実行」（CPUランタイムで十分、GPU不要）
3. セル4 (Drive mount) で認証ダイアログが出たら承認
4. 30〜45分待機 → 検証セルで「警告0件」を確認
5. 完了後、Drive上の `data/jsonl/intermediate/` 配下に9個のJSON（2016-2022分）が生成される
6. Mac Mini側で `git pull` し、`python3 scripts/build_jsonl.py` を再実行 → train が **550問** に拡張される

> **注意**: ノートは経路1 (pdfplumber) と完全同一の中間JSONスキーマで出力する設計。`OVERWRITE=False` で冪等。途中失敗してもセル単位で再実行可能。

#### 作業2: Phase 1 PoC（ベースライン取得）

OCR完了後、Qwen2.5-7B-Instruct で eval 50問のベースライン正答率を測定する Colab セッションが必要。
- 担当ノート: 未作成（OCR完了後にMac Mini Claude側で `notebooks/baseline_eval.ipynb` を新規作成）
- 必要なもの: Colab GPU ランタイム (T4 16GB)、Qwen2.5-7B anonymous DL
- attach 承認 or 手動実行ボタン押下が必要

> Mac Mini Claude側でノート作成は進められるが、attach 自動化禁止のため実行はユーザー対応となる

### 推奨案

**朝起きたら次の順序で進める**:

1. WORK_LOG.md 末尾を確認（Phase 2-4/2-5 の完了状況）
2. 上記の方法B (GitHub → Colab) で OCRノートを開いて実行ボタン押下
3. 30-45分後、Drive→ローカルへJSON取り込み + Mac Mini Claude に Phase 2-5 再実行を依頼（または手動で `python3 scripts/build_jsonl.py`）
4. その後 Phase 1 PoC 用の baseline_eval ノート作成→実行を Mac Mini Claude に再開させる

### 影響

- 解消されないと Phase 2-4/2-5 が train 100問のままで、Phase 1 PoC のFT精度にも影響する（学習データが小さい）
- ただし train 100問でもPoC自体は実行可能（FT前後比較は eval 50問固定なので成立）
- **「とりあえず100問でPoCを走らせる」も選択肢としてはあり**（学習効果が薄いリスクはある）

### Mac Mini Claudeの自走範囲（不在時の許可済）

ユーザー就寝中の指示「データ破壊・課金・認証以外は自走判断」に従い、本日中に Phase 2-4/2-5 まで完了した。Phase 1 PoC のノート作成までは自走判断で先行着手可能。実行のみ attach 承認待ち。

作成日時: 2026-05-11 00:25 JST
