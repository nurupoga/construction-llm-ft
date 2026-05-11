# 緊急: Drive マウント失敗、Baseline 再実行が必要

> **更新 (2026-05-11 12:35 JST)**: ローカル Claude が Colab tab3 の snapshot を取得して状況確認。**drive.mount セルで `ValueError: mount failed` が発生し、それ以降のセルは未実行**。Baseline accuracy は **未取得**。再実行が必要。

## 現在の Colab 実行状態（snapshot 確認結果）

| セル | 内容 | 結果 |
|---|---|---|
| 1 | `!nvidia-smi` | OK (Tesla T4, Mon May 11 03:27:33 2026) |
| 2 | `torch.cuda.is_available()` | OK (True, Tesla T4) |
| 3 | `pip install transformers==4.46.* accelerate bitsandbytes` | OK |
| **4** | **`drive.mount('/content/drive')`** | **ValueError: mount failed** |
| 5-18 | WORK_DIR cd / モデルロード / 推論 50 問 / accuracy 出力 | 未実行 |

## 失敗の想定原因

- OAuth アカウント選択画面 (Mac Mini Chrome tab5) で **`oota401@gmail.com` 選択 + 「許可」承認が完了していない / 途中で離脱した**
- Colab 公式 FAQ: `mount failed` は OAuth 承認未完了 or タイムアウト（数分）が原因
  - https://research.google.com/colaboratory/faq.html#drive-timeout

## いますぐお願いしたいこと（5分）

### ステップ1: Colab tab3 をアクティブにする

Mac Mini Chrome の **tab 3 (baseline_eval.ipynb)** を開いてください。

### ステップ2: ランタイムをリセットして再実行（推奨）

1. メニュー: **「ランタイム → ランタイムを接続解除して削除」** をクリック（既存セッションをクリアする）
2. メニュー: **「ランタイム → ランタイムのタイプを変更」** で **T4 GPU** を選択
3. メニュー: **「ランタイム → すべてのセルを実行」** をクリック
4. 警告ダイアログ「Google が作成したノートではありません」→ **「このまま実行」**
5. drive.mount セルで認証ダイアログ → **「Google ドライブに接続」** クリック
6. ポップアップで **`oota401@gmail.com` を選択 → 「許可」(最後まで)** クリック
   - **重要**: 「許可」ボタンが画面下にあり、スクロール必要な場合あり。最後まで承認する
7. 認証ポップアップが自動でクローズし、ノートに戻り Drive がマウントされる

### ステップ3 (代替案): drive.mount セルだけ再実行

- ランタイムを残したまま、セル4 (drive.mount) を **再生ボタン** で単独実行する
- 上記ステップ2の 5〜7 と同じく OAuth 完了させる
- その後、未実行の セル5〜18 を順に実行（または「ランタイム → 以下のセルを実行」）

### ステップ4: 完走確認

- 10〜20分後、ノート末尾セル (セル18想定) の出力に
  ```
  Baseline accuracy: X/50 = 0.XXXX
  saved: /content/drive/MyDrive/construction-llm-ft/results/baseline_eval.json
  ```
  が表示される
- ユーザーが accuracy 数値を ローカル/Mac Mini Claude に伝える

### ステップ5: 結果ファイル取り込み

- Colab UI 左サイドバー「ファイル」アイコン → `drive/MyDrive/construction-llm-ft/results/baseline_eval.json` を右クリック → 「ダウンロード」
- ダウンロードした json を `~/construction-llm-ft/results/baseline_eval.json` に配置
- ローカル/Mac Mini Claude に「ベースライン結果取り込み完了」と指示

## ローカル Claude 側のステータス

- 進行可能なステップなし（OAuth 承認は cross-origin で playwright-cli から自動化不可）
- 次に Claude が動けるタイミング: ユーザーが accuracy 数値を伝えるか、`results/baseline_eval.json` をリポに配置した時

---

作成日時: 2026-05-11 01:15 JST
更新日時: 2026-05-11 12:35 JST（Drive マウント失敗確認、再実行依頼）
