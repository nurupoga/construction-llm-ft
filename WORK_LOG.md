# WORK_LOG

## 2026-04-23 セッション（プロジェクト立ち上げ）

### ゴール
- 建設ドメインLLMファインチューニングの方針を決める
- 議論メモを残す場所を作る

### 作業ログ
- [初期相談] ファインチューニング初体験。Colab無料枠で建設ドメインに挑戦したい
- [3案提示] A=施工管理過去問特化 / B=安全・労災 / C=仕様書・法令
- [Colab可否確認] 無料枠+Unsloth+QLoRAで7B級は十分回せると確認
- [3者協議] Gemini（戦略）+ Copilot（デビルズ・アドボケイト）+ Claude（統合）で方針レビュー
  - Gemini: A案推し、Qwen2.5-7B推奨、HF/GitHub/Zenn公開で職務経歴強化
  - Copilot: A案は「丸暗記」リスク、データ整形が真の鬼門、FT前ベースライン必須
  - 統合: A案採用、ただし落とし穴3点（時系列holdout/採点固定/ベースライン取得）反映
- [方針修正] 目的を「FT経験を積む」に絞り、過剰評価設計（catastrophic forgetting厳密検出など）を削除
- [スコープ拡張] 1級建築施工管理技士に絞らず、複数試験種ミックスする方向で検討中
- [プロジェクト整理] `construction-llm-ft/` フォルダ作成、CLAUDE.md / WORK_LOG.md / 3者協議メモを配置

### 次回やること
- 試験種スコープ確定（施工管理6種 + 建築士 全部入り? 絞る?）
- 試験種holdoutやるか決定
- データ収集の着手（過去問PDFの入手元リサーチから）

---

### 追加: 計画レビュー2回 + Mac Mini移行決定

- [追加3者協議1] タスクリスト本体レビュー → Phase 1.5(PoC)新設、Phase 2が工数の7割と再認識、比較条件凍結必須
- [追加3者協議2] 自走計画レビュー → スコープ縮退方針追加、A7-A11/B5-B9追加、「実は止まる」リスト整備
- [構成変更] 長時間作業のため**メイン作業マシンをMac Miniに移行**決定
  - データ準備・整形・公開はMac Mini、Colab実行のみブラウザ
  - GitHub経由でローカル⇔Mac Mini同期
- [タスクリストv2 承認] PoC新設・Phase 7まで再整理した最終版を採用
- [準備] GitHubリポ作成→push→Mac Miniにclone→Mac Mini側Claudeセッション立ち上げ予定

---

## 2026-04-23 Mac Mini Claudeセッション開始

### ゴール
- Phase 0（凍結・準備）完走
- Phase 2-1〜2-3（過去問入手元調査・PDFダウンロード・著作権確認）完了
- Phase 1 PoC と Phase 3 解説合成はBブロック準備待ちのため **進めない**

### 作業ログ
- [開始] Mac Mini Claudeセッション開始、Phase 0着手
- [Phase 0-1] 試験種スコープ確定: PoCは1級建築施工管理技士1種（直近5年, 2021-2025）。CLAUDE.md更新
- [Phase 0-2] `docs/freeze-spec.md` 作成。プロンプト形式・採点ロジック・生成パラメータ・LoRAハイパラを固定
- [Phase 0-3] ディレクトリ初期化: data/{raw,jsonl/{train,eval},eval} + scripts/ + notebooks/ + results/
- [Phase 0-3] `.gitignore` 新規作成（Python/Colab/HF/モデル成果物/Mac系を除外）
- [Phase 2-1,2-3] 背景サブエージェント2件を並列起動（過去問入手元調査・著作権調査）、完了待ち
- [Phase 2-3 完了] 施工管理6種の利用規約調査完了。建築系（振興基金）「転載禁止」明示、土木系（JCTC）相対的にクリーン、建設機械系（JCMA）「如何なる権利も許諾しない」で最厳。サブエージェントからはPoC起点を土木1級に寄せる推奨あり

## 計画変更: 試験種スコープ（施工管理6種 → 宅建士1種）

- **計画**: 1級建築施工管理技士1種でPoC、PoC成功後に施工管理6種へ拡張
- **実装**: 宅地建物取引士（宅建士）1試験に変更。直近10年（2016-2025）×50問=500問
- **理由**:
  - ユーザー自身の学習動機と一致（副次価値）
  - データ整備が良好（年1回50問4択で構造クリーン）
  - 著作権面でも比較的クリーン（Phase 2-3 再実行で検証）
  - 知名度高く公開時インパクト大（建設・不動産業界向けLLMとしての訴求力）
  - Phase 2-3 調査でも建築系（振興基金）は「転載禁止」明示でリスク高く、代替試験種検討が妥当化
- **ユーザー許可**: あり（会話で明示）
- **許可の取り方**: ユーザーから方針変更メッセージで明示指示
- **日時**: 2026-04-23
- **影響範囲**:
  - 進行中の Phase 2-1 サブエージェント（施工管理入手元調査）→ 停止
  - 既作成の `docs/data-sources.md` `docs/license-check.md` → `docs/archive/` に退避（ファイル名に `-construction` サフィックス付与）
  - `CLAUDE.md` のタイトル・データ戦略・未決定事項セクション書き換え
  - `docs/freeze-spec.md` を宅建士ベースに全面書き換え（試験コード arch1 → takken、年度2021-2025 → 2016-2025、問題数 → 50問/年固定）
  - リポジトリ名 `construction-llm-ft` は据え置き（建設・不動産ドメインLLMの包括名として）

### 方針変更後の作業ログ
- [停止] サブエージェント a7bffe74... (Phase 2-1 施工管理調査) を TaskStop で停止
- [退避] `docs/data-sources.md` → `docs/archive/data-sources-construction.md`（mv）
- [退避] `docs/license-check.md` → `docs/archive/license-check-construction.md`（mv）
- [Phase 0-1 再実行] CLAUDE.md を宅建士ベースに書き換え（データ戦略・未決定事項・関連ドキュメント）
- [Phase 0-2 再実行] `docs/freeze-spec.md` を宅建士ベースに全面書き換え（試験コード takken、10年分500問、2020年分割実施対応、法令基準日注記追加）
- [環境変数] Gemini APIキーをユーザーから受領 → `~/construction-llm-ft/.env`（chmod 600、.gitignore済）保存確認。CLAUDE.md に「環境変数・APIキー管理」セクション追加。Phase 3解説合成で `python-dotenv` + `os.getenv("GEMINI_API_KEY")` で参照する方針記録
- [Phase 2-1 再起動] 宅建士過去問入手元調査の背景サブエージェント再起動（RETIO起点、10年分PDF URL列挙）
- [Phase 2-3 再起動] 宅建士著作権調査の背景サブエージェント再起動（RETIO規約、著作権法30条の4 適用評価）
- [Phase 2-1 完了] `docs/data-sources.md` 新規作成。RETIO公式で 2016-2025 全12ファイル（2020/2021はコロナ分割で各2ファイル）の直リンクを HTTP 200 確認済で列挙。主な発見:
  - 昭和63年〜令和7年の全年度公開あり（拡張余地大）
  - 問題+正答が1つのPDFに同梱、公式解説なし（自作/合成必要 → Phase 3 Gemini API）
  - PDFがCCITT Fax画像形式の可能性 → `pdftotext` では抽出不可、OCR（`pdftoppm + tesseract -l jpn`）が必要見込み
  - 2023年度(R5)のPDFファイル名に全角スペース＋typo（`qestion`）、URLエンコード必須
  - 利用規約は「私的使用・引用以外は無断転載不可」、AI学習用途の明示的許諾記述なし → 公開運用方針は Phase 2-3 調査結果と合わせて確定
- [Phase 2-3 完了] `docs/license-check.md` 新規作成。主な判定:
  - ① ローカル前処理・学習（30条の4 情報解析）: **OK（条件付き）**
  - ② LoRAアダプタのHF公開: **要確認**（逐語再生成テスト必須）
  - ③ 学習データ（JSONL/PDF抽出）の再配布: **NG/慎重**（非コミット維持）
  - ④ 問題全文の逐語再生成: **NG**
  - ⑤ 自作要約・合成解説の公開: **OK（条件付き）**
  - RETIO規約にAI学習の個別規定なし → 30条の4に戻って判断
  - 文化庁見解により学習は原則合法、ただし「享受目的併存」「特定作風再現」だとNG
  - RETIOへの事前問い合わせは「問合せには一切回答しない」方針のため期待薄

## 計画変更: 公開スコープ全廃（2026-04-23）

- **計画**: HuggingFaceモデル公開 + Zenn記事 + GitHub public で「職務経歴に書ける成果物」
- **実装**: **全非公開**。HF公開なし / Zenn記事なし / GitHub は private 固定。成果は Mac Mini + private repo 保管。面接時に private repo 招待 or ローカルデモで提示
- **理由**:
  - 宅建過去問の著作権配慮（RETIO「無断転載不可」、逐語再生成リスクの最安全回避策）
  - 勉強用途・面接デモで十分、公開手続き（モデルカード・逐語再生成チェック等）のコスト回避
  - Phase 2-3 調査結果で「モデル重み公開は要確認」と出ており、公開しないことでリスクゼロ化
- **ユーザー許可**: あり（会話で明示）
- **許可の取り方**: ユーザーから追加方針変更メッセージで明示指示
- **日時**: 2026-04-23
- **影響範囲**:
  - `CLAUDE.md` に「公開方針」セクション追加、目的欄・成果公開欄を書き換え
  - `NEXT_TASK.md` のBブロック準備物を整理（HFトークン不要に格下げ、Qwen2.5ライセンス同意不要、Colab自動保存のみ残る）
  - コード実装方針: `push_to_hub()` 類を書かない、公開用README/モデルカード生成タスクは削除
  - Qwen2.5 ベースモデルは anonymous ダウンロードで試行、拒否時のみHFトークン再取得を検討

### 方針変更後の作業ログ（続き）
- [CLAUDE.md] 「公開方針（2026-04-23 確定: 全非公開）」セクション追加、目的欄・成果保管欄を更新
- [NEXT_TASK.md] 宅建士スコープ・Phase 0/2完了ステータス・公開撤廃を反映、残ブロッカーを Colab 自動保存のみに整理
- [Phase 2-2 準備] サブエージェントで RETIO 12PDF ダウンロードへ進む予定（著作権法30条の4下のローカル学習用途でクリア、公開しないのでリスクさらに低下）
- [Phase 2-2 完了] 12PDF ダウンロード成功（失敗0件、合計12.2MB）
  - 保存先: `data/raw/takken/<year>/*.pdf`、2020/2021 は oct/dec 別ファイル
  - 全ファイル `file` コマンドで PDF 認識、SHA-256 を `data/raw/takken/manifest.json` に記録
  - 2023年度 R5 の全角スペース URL は `%E3%80%80` エンコードで正常取得
  - **テキスト抽出性の事前調査**:
    - 2023/2024/2025: `pdfplumber` で直接日本語テキスト抽出可能
    - 2016〜2022（9ファイル）: 画像PDF（CCITT Fax）、**OCR必須**（tesseract -l jpn 予定）
    - Phase 2-4（PDF→構造化）では 2022以前と 2023以降で別パイプラインを用意する必要あり
- [.gitignore 更新] 著作権配慮で `data/raw/**/*.pdf` と `data/jsonl/**/*.jsonl` を除外対象に追加。manifest.json はメタデータのみのため commit 対象として残す

## セッション終了前のまとめ（2026-04-23 Mac Mini Claude）

### 完了した作業（自走指示範囲）
- Phase 0（凍結・準備）全完了
  - 試験種スコープ確定（宅建士1試験、2016-2025）
  - `docs/freeze-spec.md` 作成
  - プロジェクトディレクトリ + `.gitignore` 初期化
- Phase 2-1/2-2/2-3（データ収集前半）全完了
  - `docs/data-sources.md`（RETIO 12PDF URL 列挙、HTTP 200 確認）
  - `docs/license-check.md`（30条の4 で学習OK、逐語再生成対策必要）
  - 12PDF ローカルダウンロード + manifest.json + 抽出性事前チェック

### 計画変更 2件（ユーザー決定）
1. 試験種スコープ: 施工管理6種 → 宅建士1試験（旧調査は `docs/archive/` に退避）
2. 公開スコープ: HF/Zenn/GitHub public → 全非公開（Mac Mini + private repo 保管）

### 次回やること（Phase 2-4 以降）
- **Phase 2-4 (PDF→構造化)**: 2023以降は `pdfplumber` で直抽出、2016-2022 は `pdftoppm + tesseract -l jpn` で OCR する2経路パイプライン構築
- **Phase 2-5〜 (JSONL 整形)**: 50問×10年 をfreeze-spec.md 準拠の `{instruction, input, output}` 形式へ
- **Phase 1 (PoC) 着手可否**: Colab 自動保存設定のユーザー側準備のみブロッカー（HFトークン・Qwen2.5同意は公開撤廃により不要化）

### ユーザー判断が必要になりそうな点（メモ）
- 2020/2021 の10月・12月試験を train にどう入れるか（両方 train or 片方に寄せる）
- 2025年度eval の正解データ取得タイミング（R7 PDFに同梱済みのため解決済、要再確認）
- Phase 3 解説合成を実施するか（Gemini API はキー受領済、費用と学習効果のトレードオフ）
- OCR パイプラインを Mac Mini ローカルで構築する前提でよいか（GPU不要だが tesseract 導入が必要）

### セッション終了

---

## 2026-05-10 セッション（ローカル新セッション・進捗確認＆判断ヒアリング）

### ゴール
- 2.5週間放置されていたプロジェクトの残タスクを整理
- ブロッカーになっていたユーザー判断4件を確定し、Mac Mini側を再始動できる状態にする

### 作業ログ
- [確認] 最終commit 4/23、`WAITING_FOR_USER.md` 不在。Mac Mini側 `ftwork` セッションも停止していると推測
- [整理] 残Phase（2-4 / 2-5 / 1 / 4-5 / 6）と判断保留事項4件を抽出してユーザー提示
- [判断確定（4件）]
  1. **2020/2021の10月/12月分割実施分**: 両方train（年度内で別問題、リーク無し）
  2. **Phase 3（Gemini API合成解説）**: 不実施。`output` は正解番号+短い理由文のみで学習。効果不足ならPoC後に追加投入
  3. **OCRパイプライン構築場所**: Colab上で実行（Mac Miniにtesseract導入不要）
  4. **Colab自動保存**: ユーザー設定中（Drive `/content/drive/MyDrive/construction-llm-ft/checkpoints/`、`save_strategy="steps"`, `save_steps=50`, `save_total_limit=2`）
- [反映] CLAUDE.md「学習/評価分割」「未決定事項→確定済み判断」セクションを書き換え
- [反映] NEXT_TASK.md を 2026-05-10 ステータスに刷新（Phase 2-4を Mac Mini経路 + Colab経路に分割、ブロッカー解消、着手手順A〜F明記）

### 次回（Mac Mini側Claude）やること
1. **Phase 2-4 経路1（Mac Mini）**: `scripts/extract_pdf_text.py` で 2023/2024/2025 を `pdfplumber` 抽出
2. **Phase 2-4 経路2（Colab）**: `notebooks/ocr_pipeline.ipynb` で 2016-2022 の9PDF を `pdftoppm + tesseract -l jpn` でOCR
3. **Phase 2-5（Mac Mini）**: 中間データを freeze-spec.md 準拠の JSONL へ整形、train/eval分割
4. Colab自動保存準備完了を WORK_LOG で確認したら **Phase 1 PoC** へ進む

### 状態
- ローカル側で commit & push 実施 → Mac Mini側 `ftwork` セッションが次回起動時に拾う想定
- Phase 2-4/2-5 は Colab自動保存完了を待たずに並行で進められる

### セッション終了

---

## 2026-05-11 追記: Colab準備完了

- ユーザーが Colab で Drive マウント + checkpointディレクトリ作成を実施
- 確認結果: `Exists: True`（`/content/drive/MyDrive/construction-llm-ft/checkpoints/takken-qwen25-7b`）
- **Colab準備完了、Phase 1 着手OK**
- Mac Mini側 `ftwork` セッションは Phase 2-4 → 2-5 → 1（PoC）の順で進めて構いません

---

## 2026-05-11 Mac Mini Claudeセッション再開、Phase 2-4 着手

### ゴール
- Phase 2-4 経路1: pdfplumberで2023/2024/2025の3PDFから中間JSON抽出
- Phase 2-4 経路2: 2016-2022用のOCR Colabノート雛形作成
- Phase 2-5: build_jsonl.py 作成、train/eval JSONL生成
- Phase 1着手OK状態（Colab自動保存準備完了済）

### 確認済前提
- 2020/2021 oct/dec 分割は両方train、Phase 3合成解説は不実施、OCRはColab上、Drive checkpoint確認済(Exists: True)
- WAITING_FOR_USER.md 不在、ブロッカーなし

### 作業ログ（実行中）
- [開始] WORK_LOGにセッション開始記録、Phase 2-4 サブエージェント委譲予定

## 2026-05-11 追記: Mac Mini Chrome に Colab ノート常駐（ローカル側追記）

- ユーザーが **Mac Mini の Chrome で `takken_ft_poc.ipynb` を開放済み**（同じGoogleアカウント、Driveマウント済の状態）
- ノートURL: https://colab.research.google.com/drive/1IUNyG5WHxYY_otKCzRgbeyzPoX8Ynq5c?hl=ja
- Mac Mini側Claudeへの含意:
  - **Phase 4-5 (FT本体)** は Mac Mini Chrome で実行する想定。MacBook閉じてもセッション切れない
  - **Phase 2-4 経路2 (OCR)** で `notebooks/ocr_pipeline.ipynb` を新規作成する場合、Driveに置いてMac Mini Chromeで開いて実行すればOK（ユーザーへの実行依頼は WAITING_FOR_USER.md で）
  - もし playwright-cli 等で Claude が直接 Mac Mini Chrome を操作する余地があれば検討可（ただし「Allow remote debugging」の状態は未確認、無理せずユーザーに実行ボタンを押してもらう運用で十分）

## 2026-05-11 追記2: 【重要】Mac Mini Chrome の attach 自動化は禁止

ユーザーから明確な再警告（**過去に同じミスを何度も繰り返している**）:

- Mac Mini Chrome の Allow remote debugging トグルは常時ON
- **しかし** Chrome側の挙動として、`playwright-cli attach --cdp=chrome` を実行するたびに **「Allow remote debugging」承認ダイアログ**が出て、ユーザーの操作（クリック）が必要
- **ユーザーが席を外している間に attach を要求すると承認できず、Mac Mini側Claude が詰まる**
- 過去にこのパターンで複数回詰まっており、ユーザーから「絶対やめろ」と再三指示されている

### Mac Mini Claude への厳格ルール（サブエージェントにも継承）

1. **ユーザー不在時の `playwright-cli attach` 禁止**
   - 在席確認なしに attach 試行は禁止
   - サブエージェント委譲時も「attach使ってOK」を含めない
2. **Colab 実行は基本 WAITING_FOR_USER.md 経由**
   - `notebooks/<name>.ipynb` を Drive にアップしたら、`WAITING_FOR_USER.md` を作って push
   - 内容: 「Mac Mini Chromeで `<URL>` を開いて『ランタイム → すべてのセルを実行』を押してください」
   - ユーザーは Mac Mini Chrome で実行ボタンを押すだけ
3. **長時間自動化が必要な時のみ、ユーザー在席中に事前 attach**
   - そのケースは事前にユーザーへ相談（`WAITING_FOR_USER.md` で「次のXX時間で attach 承認お願いします」）
   - 承認後は `-s=<session_name>` でセッション保持、不在時間中はそのセッション内でのみ操作
   - **「自動化したいから attach する」を独断で判断するな**
4. **PCR (post-commit reflection)**: サブエージェントへの指示に「playwright-cli」「ブラウザ自動化」「attach」のいずれかを含める時、必ず本ルールも添付して継承させる

## 2026-05-11 00:18 ユーザー就寝中の自走指針

ユーザーから「おやすみ。それでは画面さわれないから続けておいてね」「サブエージェントにも遵守させないと結構attachし直されてうざいことになる」との指示。

### 不在中（数時間〜翌朝）に進めてよい範囲
- ✅ **Phase 2-4 経路1**: `scripts/extract_pdf_text.py` 作成、2023-2025の3PDFを `pdfplumber` 抽出（Mac Miniローカル、attach不要）
- ✅ **Phase 2-4 経路2 の準備**: `notebooks/ocr_pipeline.ipynb` の**雛形作成のみ**。Driveに置くところまで。**実行はユーザー在席後**
- ✅ **Phase 2-5 一部**: 2023-2025分の中間JSONを `freeze-spec.md` 準拠JSONL（train side）に整形開始。OCR待ちの2016-2022分は穴を開けて待つ

### 不在中に絶対やってはいけないこと
- ❌ `playwright-cli attach --cdp=chrome` 実行（ダイアログ承認できない）
- ❌ サブエージェントに「Colabを開いて操作して」系の指示（サブエージェントが安易にattachする）
- ❌ Colab実行が必要なステップに進む（Phase 1, Phase 4-5 など）
- ❌ HF/PyPI への push, Slack等の外部送信

### Colab実行が必要な段階に到達したら
- そこで一旦止め、`WAITING_FOR_USER.md` を作って push
- ユーザーが朝起きて気付いたら手動で実行ボタンを押す or attach 承認する
- それまで Mac Mini Claude は別タスク or 待機

### サブエージェント指示文の必須テンプレート
Mac Mini Claude がサブエージェントを起動する時、prompt に以下を**必ず**含める:

```
【厳守】playwright-cli attach禁止、ブラウザ自動化禁止、Colabセル実行禁止。
ユーザーは現在不在。attach要求はダイアログ承認できず詰む。
Colab実行が必要になったら親セッションに「WAITING_FOR_USER.md作成依頼」で戻ること。
```

### 自走判断の範囲（ユーザー追加指示）

ユーザーから「**ユーザーの許可も、大きな問題（コストなど）出ない限りやっておいて。許可出せないから、寝ちゃうので**」との明示指示。

**止まる条件（この3つだけ）**:
1. **データ破壊リスク**: DROP, `git push --force` to main, `rm -rf` 系、既存重要ファイル上書き
2. **課金発生**: 有料API初使用、クラウドリソース新設、Colab Pro契約 等
3. **認証情報が必要**: 新規HFトークン取得、別Googleアカウント認証 等

**上記以外は自走判断で進めてよい**:
- 設計の細かい選択（ファイル名、関数名、ディレクトリ構成）
- サブエージェント分割粒度・並列度
- エラー時のリトライ戦略・代替手段選択
- 中間ファイルのフォーマット選択（JSON / JSONL / Parquet 等）
- LoRA hyperparam の微調整（freeze-spec.md 範囲内）
- ライブラリ選択（pdfplumber / PyMuPDF / pdfminer など同等のもの）

**判断したら WORK_LOG.md に「自己判断: X を選択、理由 Y」と記録するだけでOK**。WAITING_FOR_USER.md は不要。

### 改めて: 朝までの理想シナリオ

朝ユーザーが起きた時に WORK_LOG.md を見て、以下が完了していると最高:
- Phase 2-4 経路1 完了（2023-2025のJSON抽出）
- Phase 2-4 経路2 のColabノート雛形完成（実行待ち）
- Phase 2-5 train側のJSONL生成（OCR分は穴あき）
- WAITING_FOR_USER.md に「OCRノート実行と attach承認をお願いします」

### 作業ログ（続き）

- [Phase 2-4 経路1 完了] サブエージェントで `scripts/extract_pdf_text.py` 作成 + 実行
  - 2023/2024/2025 各50問・正答1-4 すべて抽出成功（失敗0件）
  - 出力: `data/jsonl/intermediate/{2023,2024,2025}.json` + `manifest.json`
  - 特殊ケース対応: 2025 Q41 全角「１」、2024年答えページにヘッダ無→グリッド検出フォールバック、同問番号の重複→4選択肢揃い+raw_block長でスコア比較
  - 既知の引き継ぎ事項: `(cid:NNNN)` のフォント未復号箇所が数件あり Phase 2-5 で正規化必要
- [Phase 2-4 経路2 完了] サブエージェントで `notebooks/ocr_pipeline.ipynb` 作成（22セル）
  - poppler-utils + tesseract-ocr-jpn + pytesseract 環境構築、Driveマウント、`pdftoppm -r 300` → tesseract `--psm 6 -l jpn` のパイプライン
  - 経路1と完全同一の中間JSONスキーマで出力、`OVERWRITE=False` で冪等
  - 想定実行時間: Colab CPU で 30-45分（9PDF）
  - ユーザー作業: Colabで「ランタイム > すべてのセルを実行」、完了後Mac Mini側で`git pull`
- [.gitignore更新] `data/jsonl/intermediate/*.json` 除外（manifest.jsonのみコミット）+ `data/cipher-sessions.db*` 追加除外。著作権配慮で問題本文を含むJSON非コミット維持
