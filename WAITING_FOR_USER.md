## 待機中: Phase 1〜6 の全Colab実行と結果取り込み

> **追記 (2026-05-11 11:05)**: ローカルClaudeがplaywright-cli経由で `baseline_eval.ipynb` の自動起動を試みたが、**リポジトリがprivateのためColab GitHubインポートが404**で失敗。Colabの「アップロード」タブまでは到達済みだが、Bashコマンド回数上限と本SDK環境のサブエージェント未対応により続行不可。詳細は WORK_LOG.md 末尾参照。
>
> **手動実行のお願い**: 下記ステップ1を実行してください。簡単な代替手段（A/B/Cいずれか）も用意。

### 状況

Mac Mini Claude が **Phase 1〜6 全工程の作成物を完成・push 済**。あとは Colab GPU での実行のみユーザー対応待ち。

| ファイル | 役割 | 状態 | 想定所要時間 |
|---|---|---|---|
| `notebooks/baseline_eval.ipynb` | FT前ベースライン正答率 (eval 50問) | 完成・push済 | T4で **10-20分** |
| `notebooks/ft_qlora.ipynb` | QLoRA FT (train 100問) + FT後評価 | 完成・push済 | T4で **1.5-3時間** |
| `scripts/plot_score_comparison.py` | baseline/ft の比較棒グラフ生成 | 完成・push済（ダミー動作確認済） | ローカル数秒 |

仕様準拠: 3つとも freeze-spec.md §2/§3/§4/§5/§6/§7 完全準拠（同一プロンプト/生成パラメータ/採点ロジックで FT前後比較が成立）。

### 必要な作業（順序）

#### ステップ1: ベースライン取得（10-20分、最優先）

**ノートを開く方法は以下のいずれか**（リポが private なので GitHub経由は不可）:

- **方法A（最も簡単）: Colabの「アップロード」からローカルファイルを選ぶ**
  1. Mac Mini Chrome で `https://colab.research.google.com/` を開く
  2. 「ノートブックを開く」ダイアログ → 左の「**アップロード**」タブ
  3. 「**参照**」ボタンから `~/construction-llm-ft/notebooks/baseline_eval.ipynb` を選択
- **方法B: Drive Desktop App導入で恒久解決（将来のFT実行ノートも自動化したい場合に推奨）**
  1. https://www.google.com/drive/download/ から Drive Desktop App をインストール
  2. Mac Mini で Drive を `~/Library/CloudStorage/GoogleDrive-<アカウント>/My Drive/` にマウント
  3. `cp ~/construction-llm-ft/notebooks/*.ipynb ~/Library/CloudStorage/GoogleDrive-*/My\ Drive/construction-llm-ft/notebooks/`
  4. Colabの「Google ドライブ」タブから開く
- **方法C: 一時的にリポを public 化（推奨しない）**
  - CLAUDE.mdの公開方針（全非公開）に違反するため非推奨。テンポラリにpublic→実行後即private戻しの運用は可能だが推奨しない

**ノートを開いた後**:
1. **ランタイム → ランタイムのタイプを変更 → T4 GPU**
2. **ランタイム → すべてのセルを実行**
3. Drive マウントセルで認証承認
4. 完走後、`Baseline accuracy: X/50 = 0.XXXX` を確認
5. Drive `MyDrive/construction-llm-ft/results/baseline_eval.json` をローカル repo の `results/` に取り込み

#### ステップ2: FT実行（1.5-3時間、ベースライン結果確認後）

1. Mac Mini Chrome で `ft_qlora.ipynb` を上記同じ方法で開く（A/B/Cいずれか）
2. **ランタイム → ランタイムのタイプを変更 → T4 GPU**
3. **ランタイム → すべてのセルを実行**
4. MacBook 閉じてもMac Mini Chromeで継続学習（VRAM 8-10GB想定、T4 16GBで余裕）
5. 完走後、`FT accuracy: X/50 = 0.XXXX` を確認
6. Drive `MyDrive/construction-llm-ft/results/ft_eval.json` をローカル repo の `results/` に取り込み
   - checkpoint は Drive `checkpoints/takken-qwen25-7b/` に自動保存される（save_steps=50, save_total_limit=2）

#### ステップ3: 比較グラフ生成（Mac Mini ローカル、数秒）

両 eval JSON が揃ったら Mac Mini ローカルで:
```bash
cd ~/construction-llm-ft
python3 scripts/plot_score_comparison.py
# results/score_comparison.png と results/score_comparison.json が生成される
```

### 結果取り込みの推奨方法

Drive → Mac Mini ローカル repo への同期は方法選択自由（rclone, 手動DL, Driveアプリ同期 等）。
- `results/*.json` は `.gitignore` 除外対象外なので commit可能（評価結果は問題本文を含まないため著作権配慮不要）
- commit/push されたら Mac Mini Claude が plot を自走で実行できる

### Mac Mini Claude のやることリスト（ユーザー対応後）

ユーザーが結果を repo に取り込み push したら、Mac Mini Claude は以下を自走で実行:
1. `git pull` で結果取り込み確認
2. `python3 scripts/plot_score_comparison.py` 実行
3. 結果サマリを WORK_LOG.md に記録（baseline / FT / 改善量）
4. プロジェクト完了報告

### 自動化リトライ用メモ（次回ローカルClaude向け）

自動実行を再試行する場合の前提条件:
- リポ private + Drive Desktop App 未導入 だと **playwright-cli経由でipynbを開けない**（GitHub 404、Driveパスなし）
- 方法B（Drive Desktop App導入）か `python3 -m colab_kernel_launcher` 系の代替経路があれば自動化再開可能
- playwright-cli セッション `chrome` でCDP attach 成功実績あり（このセッションで継続利用可、attach再要求は不要）
- 既存タブ:tab0=`takken_ft_poc.ipynb`(Drive), tab1=bizreach, tab2=doda, tab3=Colab welcome, tab4=GitHub OAuth（不要なら閉じてよい）

作成日時: 2026-05-11 01:15 JST
更新日時: 2026-05-11 11:08 JST（自動実行試行と失敗追記）
