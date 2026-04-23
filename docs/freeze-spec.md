# 比較条件凍結仕様書 (FT前後比較のための固定条件)

最終更新: 2026-04-23
目的: **学習前 vs 学習後の正答率比較を成立させる**ための条件を固定する。ここに書かれた条件はPoC完了まで変更しない。変更する場合はWORK_LOG.mdに理由を明記し、ベースライン再取得。

---

## 0. 対象

- **試験**: 宅地建物取引士資格試験（宅建士）
- **主催**: 一般財団法人 不動産適正取引推進機構 (RETIO)
- **形式**: 毎年10月第3日曜実施、1回あたり**50問・四択**、試験時間2時間
- **法令基準日**: 原則4月1日現在の法令に基づき出題（年度により多少のずれあり、詳細はPhase 2-1の調査結果で確認）

---

## 1. 評価対象と分割

### 対象年度（PoC）
- **直近10年分: 2016 〜 2025 年度**
- 総問題数: 約 **500問**（50問 × 10年）
- 2020年は新型コロナ影響で**10月試験と12月試験の2回**実施。両方を「2020年度」として扱う（合計100問相当）
  - train側に含める想定（最終方針はPhase 2-1調査結果後に確定）

### train / eval 分割（時系列 holdout）
- **train**: 2016〜2024 年度（9年分、約450問、2020年を2回含む場合は約500問）
- **eval**: 2025 年度（1年分、50問）
- eval を学習データに混入させないため、`data/eval/` と `data/jsonl/train/` を物理的に分離
- スクリプトで重複ID検出を必須化

### 評価問題 ID 命名規則
- フォーマット: `<exam_code>_<year>[_<session>]_<qNNN>`
- `<exam_code>`: `takken`（固定）
- `<year>`: 西暦4桁
- `<session>`: 2020年のみ `oct` / `dec`（通常年度は省略）
- `<qNNN>`: 問題番号（ゼロ埋め3桁、1〜50）
- 例:
  - `takken_2025_q001` = 宅建士2025年度 問1
  - `takken_2020_oct_q015` = 宅建士2020年度10月実施 問15
  - `takken_2020_dec_q015` = 宅建士2020年度12月実施 問15

---

## 2. プロンプト形式（学習・推論共通）

### 学習データ形式（Alpaca風 instruction tuning）
```json
{
  "instruction": "以下は宅地建物取引士資格試験の四択問題です。最も適切な選択肢の番号(1〜4)を1つだけ半角数字で答えよ。番号以外は出力しないこと。",
  "input": "問題: {question_text}\n\n1. {choice1}\n2. {choice2}\n3. {choice3}\n4. {choice4}",
  "output": "{correct_number}"
}
```

### 推論時のプロンプト（Qwen2.5-Instruct ChatML 形式）
```
<|im_start|>system
あなたは宅地建物取引士資格試験の問題に正確に回答するアシスタントです。最も適切な選択肢の番号(1〜4)を1つだけ半角数字で答え、番号以外は出力してはいけません。
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
- 「何問中何問目」などのメタ情報を prompt に入れない

### 宅建特有の前提
- 問題本文に「正しいものはどれか」「誤っているものはどれか」「組み合わせとして妥当なもの」などのバリエーションがある。prompt 側に追加指示は入れず、問題文そのままを使う
- 法令基準日は年度に紐づく（学習時も評価時もその年度の基準で固定される想定）

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

- [ ] 同一 eval セット（2025年度50問）を使用
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
  "eval_set": "takken_2025",
  "num_total": 50,
  "num_correct": 28,
  "accuracy": 0.56,
  "per_question": [
    {"id": "takken_2025_q001", "pred": "2", "gold": "2", "correct": true, "raw": "2"},
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

- [ ] 2020年10月/12月の扱い（train に両方入れるか、片方のみか）
- [ ] 問題文に図表・統計表が含まれる問題の扱い（PDF抽出時の実態を見て判断）
- [ ] 正誤判定設問（「正しいもの」「誤っているもの」）で出題バランスが偏る場合のサンプリング
- [ ] 学習データの instruction 文言の微調整
- [ ] 2025年度eval の正解データ入手時期（RETIO の正解発表日に依存）
