# 緊急: Drive 認証承認待ち（Phase 1 ベースライン実行中）

> **更新 (2026-05-11 12:30 JST)**: リポジトリ public 化後、ローカルClaude がColab `baseline_eval.ipynb` の自動実行に成功。**現在 Mac Mini Chrome の tab 5 で Google アカウント選択画面表示中**。ユーザー（在席中）の認証承認のみで完走可能。

## いますぐお願いしたいこと（30秒で済みます）

### ステップA: Drive 認証承認（必須）

Mac Mini Chrome を見てください:

1. **tab 5**（「ログイン - Google アカウント」）が現在アクティブになっています
2. **`oota401@gmail.com` を選択してクリック**
3. （初回なら）アクセス許可確認画面で **「許可」** をクリック
4. 認証ポップアップが自動でクローズし、tab 3（baseline_eval.ipynb）に戻り、Drive がマウントされてベースライン評価が継続実行されます

### ステップB: その後の自動進行（ユーザーは何もしなくてOK）

承認後は以下が自動進行（10〜20分想定）:
- モデル DL（Qwen2.5-7B-Instruct、4bit）: 5〜10 分
- 推論 50 問: 5〜10 分
- 結果が `/content/drive/MyDrive/construction-llm-ft/results/baseline_eval.json` に保存される
- ノート最下部のセル 18 出力に `Baseline accuracy: X/50 = 0.XXXX` が表示される

### ステップC: 完走後の Mac Mini 側ユーザーアクション

1. ノート最下部のセル出力で `Baseline accuracy: X/50 = 0.XXXX` を確認
2. 数値を Slack なり別ターミナルなりでローカルClaude / Mac Mini Claude に伝える
3. **結果ファイル `results/baseline_eval.json` の取り込み**:
   - **方法1（簡単）**: Colab UI の左サイドバー「ファイル」アイコン → drive/MyDrive/construction-llm-ft/results/baseline_eval.json を右クリック→「ダウンロード」→ `~/construction-llm-ft/results/` に置く
   - **方法2 (rclone等の同期手段があれば使用)**
4. 取り込んだら Mac Mini Claude に「ベースライン結果取り込み完了」と指示
   - Mac Mini Claude が次の Phase 4-5 (FT) 着手か、結果プロットへ進む

## ローカルClaude の自動実行進捗（参考）

| Step | 状態 |
|---|---|
| 1. CDP attach（既存 chrome セッション） | OK |
| 2. Colab URL `https://colab.research.google.com/github/nurupoga/construction-llm-ft/blob/main/notebooks/baseline_eval.ipynb` navigate | OK |
| 3. T4 GPU 設定確認（既に [checked]） | OK |
| 4. 「すべてのセルを実行」 | OK |
| 5. 警告ダイアログ「Google 作成ノートじゃない」→「このまま実行」 | OK |
| 6. Drive 認証ダイアログ表示 → 「Google ドライブに接続」 | OK |
| **7. Google OAuth アカウント選択画面 (tab 5)** | **← ユーザー対応待ち（いまここ）** |
| 8. Drive マウント成功 → モデル DL → 推論 50 問 → 結果保存 | 承認後自動 |

## ローカルClaude が止まった理由

- Bash 連続 25 回到達（hook ブロック）
- OAuth アカウント選択は仕様上 cross-origin で playwright-cli からの操作も Google 側でブロックされる可能性大 → どちらにせよユーザー対応必要

## リポ public 戻しタイミング

- ベースライン完走後、`gh repo edit --visibility private` で戻して OK
- 念のため FT (ft_qlora.ipynb) も同じ public 期間中に Colab 起動できるとよい
  - FT は 1.5〜3h 想定なので、認証承認だけで放置可能
- ただし優先度: まずベースライン完走 → 結果確認 → 後で FT 着手 でも問題なし

---

作成日時: 2026-05-11 01:15 JST
更新日時: 2026-05-11 12:30 JST（ローカル Claude 自動実行 partial 成功 → OAuth 承認待ち）
