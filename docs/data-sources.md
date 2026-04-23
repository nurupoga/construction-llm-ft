# 宅建士 過去問入手元まとめ

最終更新: 2026-04-23
対象: 宅地建物取引士資格試験（宅建士）
PoC期間: 直近10年分（2016 / H28 〜 2025 / R7）

---

## 1. 主催団体と公式公開

### 一般財団法人 不動産適正取引推進機構 (RETIO)

- **公式サイト**: https://www.retio.or.jp/
- **宅建試験トップ**: https://www.retio.or.jp/exam/
- **過去問掲載URL**: https://www.retio.or.jp/exam/past_ques_ans/other/
  - ページタイトル: 「宅建試験の問題及び正解番号表」
- **公開範囲**: 昭和63年度（1988）〜 令和7年度（2025） の **全年度** が公開済み
  - 各年度ごとに 「試験問題」と「正解番号表」が **1つのPDFに統合** されて配布（ファイル名パターン例: `R4-q_a.pdf` = Reiwa 4 / question & answer）
  - 令和2年度（2020）と令和3年度（2021）は 10月試験 と 12月試験 の2PDF構成（後述）
  - 平成16年度（2004）以降は 「登録講習修了者向け 45問版」 が別途存在するが、通常受験は50問
- **正解（正答番号）**: 公開あり（同一PDFの末尾または正解番号表として同梱）
- **解説**: 公式解説は **なし**（問題と正答番号のみ）
- **著作権表示**（サイトフッター）: `Copyright (C) 2009-2026 Real Estate Transaction Improvement Organization. All Rights Reserved.`
- **利用規約（ https://www.retio.or.jp/copyright/ ）の要点**:
  - 「当サイトのコンテンツ（文字、イラストなど）は著作権保護対象」
  - 「私的使用または引用等著作権法上認められた行為を除き、無断で転載等を行うことはできません」
  - **学術研究利用・AI学習用途に関する明示的記述は無し**（＝ 個別の明文許諾がないため、データセット公開時は原文転載を避けて「出典URLと該当年度・問番号」のみ記録する方針を推奨。学習目的の私的ダウンロード・モデルパラメータへの埋め込みはグレーだがセーフと見なす運用が一般的）

---

## 2. 直リンク（RETIO公式・直近10年分）

以下は `curl -I` で HTTP 200 を確認済み（確認日: 2026-04-23, JST）。

### PoC 評価対象（holdout）

| 西暦 | 和暦 | 試験日 | PDF URL | 備考 |
|---|---|---|---|---|
| 2025 | 令和7年度 | 2025-10-19(日) | https://www.retio.or.jp/wp-content/uploads/2025/12/R7_question_answer.pdf | 時系列holdout候補 |

### PoC 学習用（2016-2024）

| 西暦 | 和暦 | 試験日 | PDF URL | 備考 |
|---|---|---|---|---|
| 2024 | 令和6年度 | 2024-10-20(日) | https://www.retio.or.jp/wp-content/uploads/2025/03/R6_question_answer.pdf | |
| 2023 | 令和5年度 | 2023-10-15(日) | https://www.retio.or.jp/wp-content/uploads/2025/03/R5_qestion_answer%E3%80%80.pdf | **ファイル名末尾に全角スペース（%E3%80%80）注意**。`qestion` とtypoもあり |
| 2022 | 令和4年度 | 2022-10-16(日) | https://www.retio.or.jp/wp-content/uploads/2024/10/R4-q_a.pdf | |
| 2021 | 令和3年度(10月) | 2021-10-17(日) | https://www.retio.or.jp/wp-content/uploads/2024/12/R3-question.pdf | R3は10月/12月の2回実施 |
| 2021 | 令和3年度(12月) | 2021-12-19(日) | https://www.retio.or.jp/wp-content/uploads/2024/12/R3-question_002.pdf | 会場都合で一部受験者が12月に回された（R2の名残） |
| 2020 | 令和2年度(10月) | 2020-10-18(日) | https://www.retio.or.jp/wp-content/uploads/2024/10/R2-question.pdf | コロナで分割実施 |
| 2020 | 令和2年度(12月) | 2020-12-27(日) | https://www.retio.or.jp/wp-content/uploads/2024/10/R2-question_002.pdf | 同上 |
| 2019 | 令和元年度 | 2019-10-20(日) | https://www.retio.or.jp/wp-content/uploads/2024/10/R1-q_a.pdf | |
| 2018 | 平成30年度 | 2018-10-21(日) | https://www.retio.or.jp/wp-content/uploads/2024/10/H30-q_a.pdf | |
| 2017 | 平成29年度 | 2017-10-15(日) | https://www.retio.or.jp/wp-content/uploads/2024/10/H29-q_a.pdf | |
| 2016 | 平成28年度 | 2016-10-16(日) | https://www.retio.or.jp/wp-content/uploads/2024/10/H28-q_a.pdf | PoC学習期間の開始年 |

### （参考）それより古い年度（H27以前）

- H27〜H01 および S63 も全て公開あり。パターンは `/wp-content/uploads/2024/10/H<NN>-q_a.pdf`（2桁ゼロ埋め）
  - 例: H27 → https://www.retio.or.jp/wp-content/uploads/2024/10/H27-q_a.pdf
  - 例: S63 → https://www.retio.or.jp/wp-content/uploads/2024/10/S63-q_a.pdf
- PoCでは使わないが、データ拡張したい場合に利用可能。
- **注意**: 古い年度は法改正前の内容を含む（RETIO自身が「現在の法律と一致しない場合があります」と明記）。学習に使うと古い知識を強化してしまうリスクあり。

---

## 3. 2020年（令和2年）の特殊事情

- コロナ禍の影響で、通常10月の1回開催だった試験が **10月試験 + 12月試験の2回実施** に分割された。
- 受験者は居住地・申込順により10月組／12月組のいずれかに割り振られ、 **問題内容は別物**（同じ年度でも異なる試験）。
- 2021年（令和3年）も同様に10月/12月の2回実施（2021は都道府県別の会場都合）。
- **データ収集時の扱い**: 本プロジェクトでは **「2020-10」「2020-12」「2021-10」「2021-12」を別データソースとして扱う** のを推奨。
  - 年度単位の時系列holdoutで2020全体を評価用にするなら、10月と12月の両PDFをまとめて1年分扱いにする手もあり。
  - どちらにせよ、学習/評価が同じ試験回（例: 2020-10 の問題）に跨らないよう分離することが必須。

---

## 4. PDF の技術的注意点

RETIOが配布するPDFは **Flate圧縮 + PDF暗号化(R=4/V=4) + 画像ベース（CCITT Fax画像を埋め込み）** の組み合わせで、素の `pdftotext` では本文が抽出できない可能性が高い。

- 確認事項（R4-q_a.pdf を取得して確認）:
  - `%PDF-1.7` / Linearized / `Encrypt 137 0 R` あり
  - 本文はCCITT Faxストリーム（= スキャン画像をPDFに埋め込んだ形式）
- **推奨前処理パイプライン**:
  1. `pdftoppm` または `pdftocairo` でページごとにPNG化
  2. Google Document AI / Azure Document Intelligence / Tesseract(jpn) でOCR
  3. 問1〜問50 の区切りを正規表現で抽出、4択（1〜4）の選択肢を構造化
  4. 末尾の「正解番号表」から正答 (問番号 → 1-4) を抽出
  5. `{instruction, input, output}` 形式に整形（問題文＋選択肢を input、正答番号を output）
- コピー制限がある場合、OCR→テキスト化の過程で手元に「再入力されたテキスト」が生成されるため、転載ではなく 「自分で作ったデータセット」 として扱う余地あり。ただし **公開データセットとしてHuggingFaceに本文を上げるのは著作権リスク** 。公開するなら「問題IDと出典URLと正答のみ」とするのが安全。

---

## 5. 補助ソース（公式でない / 参考程度）

本プロジェクトでは原則RETIOの公式PDFのみを使う。以下はあくまで年号や問題番号のクロスチェック用。

- **TAC**: https://www.tac-school.co.jp/kouza_takken/takken_contents_kakomon_guide.html
  - 過去問題の出題傾向解説あり。問題文そのものはPDFで公開していない場合が多い。
- **LEC**: 各試験直後に速報解説PDF。正答チェック用。
- **日建学院 / 大原 / アガルート** 等: ブログ形式で解説。著作権上、問題文を転載している場合があるため、学習データソースとしては使わない（公式のみ）。
- **一般財団法人 住宅金融普及協会**: 旧試験機関としての言及があるが、**現在の試験実施は RETIO 単独**。過去問PDFは同協会では公開されていない（2026-04-23時点で確認できず）。
- **国土交通省**: 試験制度・合格発表のアナウンスはあるが、問題PDFの公開は行っていない（RETIOに委任）。

---

## 6. 取得できない / 要確認

- なし（直近10年分 H28〜R7 は全て公式サイトから取得可能）
- ただし R5 の URL に **全角スペース** が含まれるため、wget/curl では URL エンコード（`%E3%80%80`）が必須。
- R3/R2 の12月試験版は `_002.pdf` サフィックスで配布（10月版と別ファイル）。

---

## 7. 推奨取得手順

### ディレクトリ命名規則

```
data/raw/takken/
├── 2016/  # H28
│   └── H28-q_a.pdf
├── 2017/  # H29
│   └── H29-q_a.pdf
├── ...
├── 2020/  # R2（10月/12月の2回実施）
│   ├── R2-question.pdf         # 10月
│   └── R2-question_002.pdf     # 12月
├── 2021/  # R3（10月/12月の2回実施）
│   ├── R3-question.pdf         # 10月
│   └── R3-question_002.pdf     # 12月
├── 2022/  # R4
│   └── R4-q_a.pdf
├── 2023/  # R5
│   └── R5-q_a.pdf              # ローカル保存時は全角スペースを削除したファイル名に
├── 2024/  # R6
│   └── R6_question_answer.pdf
└── 2025/  # R7（評価用holdout）
    └── R7_question_answer.pdf
```

### ダウンロードスクリプト例

```bash
#!/usr/bin/env bash
# scripts/fetch_takken_pdfs.sh
set -euo pipefail
BASE="https://www.retio.or.jp/wp-content/uploads"
OUT="data/raw/takken"
UA="Mozilla/5.0 (compatible; construction-llm-ft/0.1; +research)"

mkdir -p "$OUT"/{2016,2017,2018,2019,2020,2021,2022,2023,2024,2025}

# 西暦  URL                                                ローカルファイル名
declare -a FILES=(
  "2016 $BASE/2024/10/H28-q_a.pdf                          H28-q_a.pdf"
  "2017 $BASE/2024/10/H29-q_a.pdf                          H29-q_a.pdf"
  "2018 $BASE/2024/10/H30-q_a.pdf                          H30-q_a.pdf"
  "2019 $BASE/2024/10/R1-q_a.pdf                           R1-q_a.pdf"
  "2020 $BASE/2024/10/R2-question.pdf                      R2-question_oct.pdf"
  "2020 $BASE/2024/10/R2-question_002.pdf                  R2-question_dec.pdf"
  "2021 $BASE/2024/12/R3-question.pdf                      R3-question_oct.pdf"
  "2021 $BASE/2024/12/R3-question_002.pdf                  R3-question_dec.pdf"
  "2022 $BASE/2024/10/R4-q_a.pdf                           R4-q_a.pdf"
  "2023 $BASE/2025/03/R5_qestion_answer%E3%80%80.pdf       R5-q_a.pdf"
  "2024 $BASE/2025/03/R6_question_answer.pdf               R6-q_a.pdf"
  "2025 $BASE/2025/12/R7_question_answer.pdf               R7-q_a.pdf"
)

for row in "${FILES[@]}"; do
  read -r year url fname <<< "$row"
  dest="$OUT/$year/$fname"
  if [[ -f "$dest" ]]; then
    echo "[skip] $dest"
    continue
  fi
  echo "[get ] $url -> $dest"
  curl -sS -A "$UA" --retry 3 --retry-delay 2 -o "$dest" "$url"
  sleep 1
done

echo "Done. Verifying file sizes:"
find "$OUT" -name "*.pdf" -print0 | xargs -0 ls -la
```

### 取得後のチェックリスト

- [ ] 各 PDF が 500KB〜5MB 程度（0 バイトでない）
- [ ] `file` コマンドで `PDF document` と認識される
- [ ] OCR前に1ページ目を `pdftoppm` で画像化して目視確認
- [ ] 2020/2021 の 10月版/12月版が別ファイルとして保存されている
- [ ] 各年度で「問題50問 + 正解番号表」が揃っているか（OCR後）

---

## 8. 年度和暦⇔西暦 対応表（クイックリファレンス）

| 和暦 | 西暦 | 試験実施 |
|---|---|---|
| S63 | 1988 | 10月 |
| H01 | 1989 | 10月 |
| H28 | 2016 | 10月 |
| H29 | 2017 | 10月 |
| H30 | 2018 | 10月 |
| R01 | 2019 | 10月 |
| R02 | 2020 | **10月 + 12月（分割）** |
| R03 | 2021 | **10月 + 12月（分割）** |
| R04 | 2022 | 10月 |
| R05 | 2023 | 10月 |
| R06 | 2024 | 10月 |
| R07 | 2025 | 10月 |

- 通常は毎年「10月第3日曜日」が試験日。

---

## 9. 次アクション

1. 上記スクリプトで直近10年分を `data/raw/takken/` に取得
2. PDF の暗号化・OCR可否を実機確認（Mac Mini 上で `pdftoppm` + `tesseract -l jpn` または GCP Document AI 試用枠）
3. OCR結果を `{instruction, input, output}` JSONL に整形するスクリプトを作成
4. 2025年（R7）は evaluation holdout とし、train からは完全に除外
5. 法改正の影響を受けやすい古い年度（H27 以前）は学習セットに含めるか別途検討

---

## Sources

- [宅建試験の問題及び正解番号表 | RETIO](https://www.retio.or.jp/exam/past_ques_ans/other/)
- [宅建試験 | RETIO](https://www.retio.or.jp/exam/)
- [不動産適正取引推進機構 公式トップ](https://www.retio.or.jp/)
- [著作権・免責 | RETIO](https://www.retio.or.jp/copyright/)
- [令和7年度宅地建物取引士資格試験結果の概要（2025-11-26公表, 試験日2025-10-19）](https://goukaku.retio.or.jp/exam/pdf_2025_1_UWbaZCx6hm/2025result.pdf)
- [宅建の過去問 | 資格の学校TAC（補助ソース・参考）](https://www.tac-school.co.jp/kouza_takken/takken_contents_kakomon_guide.html)
