## 待機中: Phase 1 PoC ベースライン評価ノートを Colab GPU で実行

### 状況

Mac Mini Claude が Phase 1 PoC のベースライン取得用 Colab ノートを作成完了。

- 作成済: `notebooks/baseline_eval.ipynb`（20セル）
- 仕様: freeze-spec.md §2/§3/§4/§7 完全準拠
- 内容: Qwen2.5-7B-Instruct を anonymous DL + 4bit nf4 量子化で T4 にロードし、`data/jsonl/eval/takken_eval.jsonl` (50問) で正答率測定。`results/baseline_eval.json` に保存
- 想定所要時間: Colab T4 で **10〜20分** （依存インストール 2分 + モデルDL/ロード 5-10分 + 推論50問 5-10分）

並行で、Mac Mini Claude が **FT実行ノート (`notebooks/ft_qlora.ipynb`)** と **比較グラフスクリプト (`scripts/plot_score_comparison.py`)** も先行作成中。完成次第追加push予定。

### 必要な作業

#### A. ベースライン評価ノートの Colab 実行（最優先、10-20分）

1. Mac Mini Chrome で以下のいずれかで `notebooks/baseline_eval.ipynb` を開く:
   - **方法A (推奨・最速)**: GitHub から直接 → `https://colab.research.google.com/github/nurupoga/construction-llm-ft/blob/main/notebooks/baseline_eval.ipynb`
   - **方法B**: Drive側に置いてある場合は Drive ファイルから「Colabで開く」（事前 git → Drive 同期が必要）
2. **メニュー: ランタイム → ランタイムのタイプを変更 → T4 GPU** を選択
3. **メニュー: ランタイム → すべてのセルを実行** を押下
4. Drive マウントセル（セル7）で認証ダイアログ → 承認
5. 完走待ち（10-20分）→ 最後のセルで `Baseline accuracy: X/50 = 0.XXXX` 表示を確認
6. `/content/drive/MyDrive/construction-llm-ft/results/baseline_eval.json` に結果保存
7. Mac Mini ローカル側で結果取り込み:
   - 方法i: Drive→repo にコピー（手動）→ `git add results/baseline_eval.json && git commit && git push`
   - 方法ii: Driveから直接ダウンロード→repoに配置
   - **`results/*.json` は `.gitignore` 除外対象外なので commit可能**（per_question配列も含まれるが、評価結果は問題本文を含まないためOK）

#### B. ベースライン結果を Mac Mini Claude に渡す

- ベースライン結果が `results/baseline_eval.json` として push されたら、Mac Mini Claude がそれを起点に Phase 4-5（FT実行ノート）を進められる
- FT実行ノートは並行で作成中なので、ベースライン完了後すぐに「FTノートを Colab で実行」フェーズに移れる想定

### 推奨フロー

1. **今すぐ**: 方法A で baseline_eval.ipynb を Colab で開く → T4 GPU 設定 → 「すべてのセルを実行」
2. 10-20分放置（Mac Mini Chrome ならMacBook閉じても継続）
3. 完了後: `results/baseline_eval.json` を repo に取り込み → commit → push
4. Mac Mini Claude セッション再開（または継続）→ Phase 4-5 FT実行へ進む

### 影響

- 解消されないと Phase 1 PoC の **「学習前正答率」** が取れず、FT前後比較が成立しない
- これはプロジェクトのコア成果物（「学習前 vs 学習後で正答率が上がった」のグラフ）に直結
- ノート作成だけなら Mac Mini Claude で続けられる（FTノート・比較スクリプトを並行作成中）が、**実行と結果取得はユーザー対応必須**

### 不在時自走範囲（既存ルール継続）

- Mac Mini Claude は FTノート・比較スクリプト作成まで自走で進める
- attach自動化禁止ルール継続、Colab実行が必要になったら本ファイルを更新して停止

作成日時: 2026-05-11 01:00 JST
