## 待機中: Phase 1〜6 の全Colab実行と結果取り込み

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

1. Mac Mini Chrome で開く: `https://colab.research.google.com/github/nurupoga/construction-llm-ft/blob/main/notebooks/baseline_eval.ipynb`
2. **ランタイム → ランタイムのタイプを変更 → T4 GPU**
3. **ランタイム → すべてのセルを実行**
4. Drive マウントセルで認証承認
5. 完走後、`Baseline accuracy: X/50 = 0.XXXX` を確認
6. Drive `MyDrive/construction-llm-ft/results/baseline_eval.json` をローカル repo の `results/` に取り込み

#### ステップ2: FT実行（1.5-3時間、ベースライン結果確認後）

1. Mac Mini Chrome で開く: `https://colab.research.google.com/github/nurupoga/construction-llm-ft/blob/main/notebooks/ft_qlora.ipynb`
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

### 自走範囲（不在時継続）

ユーザー就寝中の指示「データ破壊・課金・認証以外は自走判断」に従い、本セッションで Phase 1-6 の全コード作成物を完成。Colab実行のみ attach 自動化禁止のためここで停止。

作成日時: 2026-05-11 01:15 JST
