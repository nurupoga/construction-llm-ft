# 比較条件凍結仕様書 (FT前後比較のための固定条件)

最終更新: 2026-04-23
目的: **学習前 vs 学習後の正答率比較を成立させる**ための条件を固定する。ここに書かれた条件はPoC完了まで変更しない。変更する場合はWORK_LOG.mdに理由を明記し、ベースライン再取得。

---

## 1. 評価対象と分割

### 対象試験（PoC）
- **1級建築施工管理技士 一次検定**（旧学科試験）
- 直近5年分: 2021 / 2022 / 2023 / 2024 / 2025 年度

### train / eval 分割（時系列 holdout）
- **train**: 2021〜2024 年度（4年分）
- **eval**: 2025 年度（最新1年）
- eval を学習データに混入させないため、`data/eval/` と `data/jsonl/train/` を物理的に分離する

### 評価問題 ID 命名規則
- フォーマット: `<exam_code>_<year>_<qNNN>`
- `<exam_code>`: 試験種コード（下表参照）
- `<year>`: 西暦4桁
- `<qNNN>`: 問題番号（ゼロ埋め3桁）
- 例: `arch1_2025_q001` = 1級建築施工管理技士 2025年度 問1

| 試験種コード | 正式名称 |
|---|---|
| `arch1` | 1級建築施工管理技士 |
| `arch2` | 2級建築施工管理技士 |
| `civil1` / `civil2` | 1級/2級 土木施工管理技士 |
| `pipe1` / `pipe2` | 1級/2級 管工事施工管理技士 |
| `elec1` / `elec2` | 1級/2級 電気工事施工管理技士 |
| `garden1` / `garden2` | 1級/2級 造園施工管理技士 |
| `machine1` / `machine2` | 1級/2級 建設機械施工技士 |

---

## 2. プロンプト形式（学習・推論共通）

### 学習データ形式（Alpaca風 instruction tuning）
```json
{
  "instruction": "以下は建設業関連の資格試験の四択問題です。最も適切な選択肢の番号(1〜4)を1つだけ半角数字で答えよ。番号以外は出力しないこと。",
  "input": "問題: {question_text}\n\n1. {choice1}\n2. {choice2}\n3. {choice3}\n4. {choice4}",
  "output": "{correct_number}"
}
```

### 推論時のプロンプト（Qwen2.5-Instruct ChatML 形式）
```
<|im_start|>system
あなたは建設業関連資格試験の問題に正確に回答するアシスタントです。最も適切な選択肢の番号(1〜4)を1つだけ半角数字で答え、番号以外は出力してはいけません。
<|im_end|>
<|im_start|>user
問題: {question_text}

1. {choice1}
2. {choice2}
3. {choice3}
4. {choice4}
<|im_end|>
<|im_start|>assistant
```

### 禁止事項（学習時・評価時ともに）
- few-shot 例の挿入（zero-shot で固定）
- CoT（Chain of Thought）指示の追加
- "Let's think step by step" 類の文言
- 選択肢を記号 (ア/イ/ウ/エ, A/B/C/D) で表記すること（**必ず 1〜4 の半角数字**）

---

## 3. 生成パラメータ（評価時の固定値）

| パラメータ | 値 | 理由 |
|---|---|---|
| `temperature` | `0.0` | 決定論的出力、再現性確保 |
| `top_p` | `1.0` | 温度0なので無影響だが明示 |
| `top_k` | `-1` (無効) | 〃 |
| `max_new_tokens` | `8` | 番号1文字出せば十分だが余裕を持たせる |
| `seed` | `42` | 温度0なので無影響だが明示 |
| `do_sample` | `false` | 温度0と等価 |
| `repetition_penalty` | `1.0` | 無調整 |

**重要**: ベースライン取得時と FT後評価時でこれらの値を変えてはいけない。

---

## 4. 採点ロジック

### 抽出ルール
1. モデル出力の先頭から連続する空白・改行を除去
2. 最初に出現する半角数字 (`1`, `2`, `3`, `4`) を回答とみなす
3. 上記で該当なしの場合は `unparseable`（不正解扱い）

疑似コード:
```python
import re

def extract_answer(raw_output: str) -> str:
    stripped = raw_output.strip()
    m = re.search(r'[1-4]', stripped)
    return m.group(0) if m else 'unparseable'
```

### 採点ルール
- 抽出した番号と正解番号が **完全一致**なら正解、それ以外は不正解
- `unparseable` は不正解としてカウント（部分点なし）
- 採点単位は `accuracy = 正解数 / 総問題数`

### 禁止事項
- 「選択肢の文字列類似度で判定」「LLM-as-Judge」など曖昧な採点
- eval セット内の問題を採点前に目視で除外すること
- 同じ問題に対する複数回生成の多数決（温度0なので不要）

---

## 5. 学習ハイパーパラメータ（参考、PoC時に調整可）

以下は**学習時**の値。ベースライン取得とは無関係なので、PoC中にチューニング可。ただし最終比較時は一度固定する。

| 項目 | PoC暫定値 |
|---|---|
| ベースモデル | `Qwen/Qwen2.5-7B-Instruct` |
| 量子化 | 4bit (nf4) via bitsandbytes |
| LoRA rank (`r`) | 16 |
| LoRA alpha | 32 |
| LoRA target_modules | `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` |
| LoRA dropout | 0.05 |
| epoch | 2〜3 |
| learning_rate | 2e-4 |
| batch_size (per device) | 2 |
| gradient_accumulation | 4 |
| max_seq_length | 2048 |
| optimizer | `adamw_8bit` |
| scheduler | cosine |
| warmup_ratio | 0.03 |
| seed (学習) | 42 |

---

## 6. 比較成立条件（チェックリスト）

FT前ベースライン取得 → FT実行 → FT後評価 の流れで、以下すべてを満たすこと:

- [ ] 同一 eval セット（2025年度分）を使用
- [ ] 同一プロンプトテンプレートを使用（§2）
- [ ] 同一生成パラメータを使用（§3）
- [ ] 同一採点ロジックを使用（§4）
- [ ] 同一ベースモデル / 同一量子化設定（学習時もFT後推論時も4bit）
- [ ] モデルロード時の `device_map`, `dtype` が一致
- [ ] train/eval の問題IDが重複していない（スクリプトで検証）
- [ ] 結果は `results/baseline.json` と `results/ft.json` に保存（後述）

---

## 7. 結果ファイルフォーマット

評価スクリプトの出力は以下の JSON 形式で保存:

```json
{
  "run_id": "baseline_20260423" or "ft_20260501_e2_lr2e-4",
  "model": "Qwen/Qwen2.5-7B-Instruct",
  "adapter": null or "path/to/adapter",
  "eval_set": "arch1_2025",
  "num_total": 60,
  "num_correct": 33,
  "accuracy": 0.55,
  "per_question": [
    {"id": "arch1_2025_q001", "pred": "2", "gold": "2", "correct": true, "raw": "2"},
    ...
  ],
  "config": {
    "temperature": 0.0,
    "max_new_tokens": 8,
    "seed": 42
  },
  "timestamp": "2026-04-23T14:00:00+09:00"
}
```

---

## 8. この仕様書を変更する場合

1. `WORK_LOG.md` に変更理由を明記
2. 影響範囲を列挙（ベースライン再取得が必要か等）
3. ベースライン再取得が必要なら必ず取り直す
4. この仕様書の「最終更新」日付を更新
5. git commit のメッセージに `freeze-spec: ` プレフィックスを付ける

---

## 9. 未決定事項（PoC中に決める）

- [ ] 学習データの instruction 文言の微調整（現行: 「...番号を1つだけ半角数字で答えよ」）
- [ ] eval セットの総問題数（年度に依存、確定は Phase 2-4 以降）
- [ ] 「選択肢が4つでない問題」（例: 記述式、5択）の扱い → 原則 eval から除外、train にも含めない
- [ ] 図表を含む問題の扱い → PoC では図表なし問題のみ採用、Phase 2-4 の PDF 抽出時に判断
