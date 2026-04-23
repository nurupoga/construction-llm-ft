# 過去問入手元まとめ

最終更新: 2026-04-23
調査者: Mac Mini 側 Claude（サブエージェント）

## 概要

建設ドメイン LLM ファインチューニング用の学習・評価データとして、施工管理系国家資格の過去問（四肢択一／五肢択一が中心の第一次検定）を最新5年分（令和3〜令和7年度 = 2021〜2025年度）収集することを目的に、入手元を調査した。

結論サマリ:

- **建築・電気工事**（建設業振興基金 / fcip-shiken.jp）: 公式サイトに令和3〜7年度の全PDFが直接ホスティングされており、命名規則も規則的。最も扱いやすい。**PoC優先の「1級建築施工管理技士」はここから全年度取得可能**。
- **土木・管工事・造園・電気通信**（全国建設研修センター / jctc.jp）: 公式サイトには令和7年度しか残っていない（過年度は自動削除）。ただし JCTC から**正式に許諾を受けて過去10年分以上を公開している「どぼくじら.com」**が実質的な一次ソースとして機能する。
- **建設機械施工**（日本建設機械施工協会 / jcmanet-shiken.jp）: 公式サイトは「試験翌日から1年間」の掲載方針で、令和7年度のみ取得可能。過年度はアーカイブ探索が必要（優先度低く、スコープ外も検討可）。
- **建築士**（建築技術教育普及センター / jaeic.or.jp）: 調査対象6種には含まないが、参考として1級建築士の過去問URLが規則的に取得可能。データ多様化を検討する際の補助ソースになる。

直リンクがあるものは全て実際に `curl -I` で HTTP 200 を確認済み（fcip-shiken の全50URL）。dobokujira.com のURLはページ本文から機械抽出。

---

## 1. 1級建築施工管理技士（PoC優先、最重要）

- **主催団体**: 一般財団法人 建設業振興基金（試験研修本部）
- **公式サイト（試験情報トップ）**: https://www.fcip-shiken.jp/
- **過去問一覧ページ**: https://www.fcip-shiken.jp/about/
- **過去問公開状況**:
  - **問題PDF**: あり（公式）
  - **正答**: 「正答肢」が問題PDF末尾に含まれる構成（マークシート式は正答表あり、記述式は「正答を公表しません」と明記）
  - **解説**: なし（公式は解説非公開。解説は非公式サイトまたは自作要約が必要）
- **命名規則**: `https://www.fcip-shiken.jp/pdf/{r03|r04|r05|r06|r07}_1{kg|kj}_mondai.pdf`
  - `kg` = 第一次検定（学科／マーク）、`kj` = 第二次検定（記述）
- **直リンク（HTTP 200 確認済み）**:

  | 年度 | 第一次検定（kg） | 第二次検定（kj） |
  |---|---|---|
  | 令和7年度（2025） | https://www.fcip-shiken.jp/pdf/r07_1kg_mondai.pdf | https://www.fcip-shiken.jp/pdf/r07_1kj_mondai.pdf |
  | 令和6年度（2024） | https://www.fcip-shiken.jp/pdf/r06_1kg_mondai.pdf | https://www.fcip-shiken.jp/pdf/r06_1kj_mondai.pdf |
  | 令和5年度（2023） | https://www.fcip-shiken.jp/pdf/r05_1kg_mondai.pdf | https://www.fcip-shiken.jp/pdf/r05_1kj_mondai.pdf |
  | 令和4年度（2022） | https://www.fcip-shiken.jp/pdf/r04_1kg_mondai.pdf | https://www.fcip-shiken.jp/pdf/r04_1kj_mondai.pdf |
  | 令和3年度（2021） | https://www.fcip-shiken.jp/pdf/r03_1kg_mondai.pdf | https://www.fcip-shiken.jp/pdf/r03_1kj_mondai.pdf |

- **令和7年度 第二次検定（臨時試験）**: https://www.fcip-shiken.jp/pdf/r07_1kj_mondai_rinji.pdf
- **備考**:
  - 第一次検定は**四肢択一（+ 五肢択二の「応用能力問題」）**中心で QA 整形しやすい。PoC の主戦場はこれ。
  - 第二次検定は記述式・施工経験記述が中心で、単純な QA データ化は難しいので PoC では除外を推奨。
  - PDFはテキスト埋め込み型（WebFetch でバイナリ取得できメタデータに試験名が埋まっていることを確認）。`pdfminer` / `pypdf` 等で抽出可能とみられる。
  - 最新1年（令和7 = 2025）を評価用、古い4年（令和3〜6 = 2021〜2024）を学習用に使う時系列holdoutが素直。

---

## 2. 2級建築施工管理技士

- **主催団体**: 一般財団法人 建設業振興基金
- **公式サイト**: https://www.fcip-shiken.jp/
- **過去問公開状況**: 公式PDFあり。2級は**前期（第一次検定のみ）と後期（第一次＋第二次）**で分かれる。
- **命名規則**:
  - 後期 第一次: `r{XX}_2kg_mondai.pdf`
  - 後期 第二次: `r{XX}_2kj_mondai.pdf`
  - 前期 第一次: `r{XX}_2kgz_mondai.pdf`（`z` = 前期）
- **直リンク（HTTP 200 確認済み、r03〜r07 すべて）**:

  | 年度 | 後期 第一次 | 後期 第二次 | 前期 第一次 |
  |---|---|---|---|
  | R7 | https://www.fcip-shiken.jp/pdf/r07_2kg_mondai.pdf | https://www.fcip-shiken.jp/pdf/r07_2kj_mondai.pdf | https://www.fcip-shiken.jp/pdf/r07_2kgz_mondai.pdf |
  | R6 | https://www.fcip-shiken.jp/pdf/r06_2kg_mondai.pdf | https://www.fcip-shiken.jp/pdf/r06_2kj_mondai.pdf | https://www.fcip-shiken.jp/pdf/r06_2kgz_mondai.pdf |
  | R5 | https://www.fcip-shiken.jp/pdf/r05_2kg_mondai.pdf | https://www.fcip-shiken.jp/pdf/r05_2kj_mondai.pdf | https://www.fcip-shiken.jp/pdf/r05_2kgz_mondai.pdf |
  | R4 | https://www.fcip-shiken.jp/pdf/r04_2kg_mondai.pdf | https://www.fcip-shiken.jp/pdf/r04_2kj_mondai.pdf | https://www.fcip-shiken.jp/pdf/r04_2kgz_mondai.pdf |
  | R3 | https://www.fcip-shiken.jp/pdf/r03_2kg_mondai.pdf | https://www.fcip-shiken.jp/pdf/r03_2kj_mondai.pdf | https://www.fcip-shiken.jp/pdf/r03_2kgz_mondai.pdf |

- **備考**: 前期は1年に2回受験機会があるぶんデータ量が増える。後期は受検種別（建築／躯体／仕上げ）ごとの分岐がある可能性があり、PDF内部を見て整形ルールを決める必要あり。

---

## 3. 1級・2級 土木施工管理技士

- **主催団体**: 一般財団法人 全国建設研修センター（JCTC）
- **公式サイト**: https://www.jctc.jp/
- **過去問一覧ページ**: https://www.jctc.jp/mondai/
- **各試験ページ**:
  - 1級: https://www.jctc.jp/exam/doboku-1/
  - 2級: https://www.jctc.jp/exam/doboku-2/
- **過去問公開状況（公式）**:
  - 公式ページには**令和7年度のみ**掲載。過年度PDFはサイトから削除されるとみられる（過年度URLは 404 を確認）。
  - 問題PDFと正答肢PDFが分かれている（第一次検定の正答のみ公開、第二次は公表なし）。
- **公式直リンク（令和7年度のみ、HTTP 200 確認済み）**:
  - 1級 第一次検定 問題A: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/07/20250707d_mondaia.pdf
  - 1級 第一次検定 問題B: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/07/20250707d_mondaib.pdf
  - 1級 第一次検定 正答肢: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/07/20250707d_seitou.pdf
  - 1級 第二次検定 問題: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/10/20251006d_mondai.pdf
  - 2級 第一次検定（後期）問題: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/10/20251027d_mondaia1.pdf（土木種別）
    - 鋼構造物塗装: `20251027d_mondaia2.pdf` / 薬液注入: `20251027d_mondaia3.pdf`
  - 2級 第一次検定（前期）問題: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/06/20250602d_mondai.pdf
  - 2級 第一次検定（前期）正答: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/06/20250602d_seitou.pdf
- **過年度の実質的な一次ソース: どぼくじら.com**
  - JCTCから「正式に許諾を受けて公開している」と明記あり
  - 1級: https://dobokujira.com/1doboku-pastproblems/
  - 2級: https://dobokujira.com/2doboku-pastproblems/
- **どぼくじら.com 直リンク（1級土木、R3〜R7）**:

  | 年度 | 1次A | 1次B | 1次解答 | 2次問題 |
  |---|---|---|---|---|
  | R7 | https://dobokujira.com/wp-content/uploads/2025/07/R7_1doboku_01_mondaiA.pdf | https://dobokujira.com/wp-content/uploads/2025/07/R7_1doboku_01_mondaiB.pdf | https://dobokujira.com/wp-content/uploads/2025/07/R7_1doboku_01_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2025/10/R7_1doboku_02_mondai.pdf |
  | R6 | https://dobokujira.com/wp-content/uploads/2024/07/20240708d_mondaia.pdf | https://dobokujira.com/wp-content/uploads/2024/07/20240708d_mondaib.pdf | https://dobokujira.com/wp-content/uploads/2024/07/20240708d_seitou.pdf | https://dobokujira.com/wp-content/uploads/2024/10/R6_1doboku_02_mondai.pdf |
  | R5 | https://dobokujira.com/wp-content/uploads/2023/07/20230703d_mondaia.pdf | https://dobokujira.com/wp-content/uploads/2023/07/20230703d_mondaib.pdf | https://dobokujira.com/wp-content/uploads/2023/07/20230703d_seitou.pdf | https://dobokujira.com/wp-content/uploads/2023/10/20231002d_mondai.pdf |
  | R4 | https://dobokujira.com/wp-content/uploads/2022/07/doboku01.pdf | https://dobokujira.com/wp-content/uploads/2022/07/doboku02.pdf | https://dobokujira.com/wp-content/uploads/2022/07/220704d.pdf | https://dobokujira.com/wp-content/uploads/2022/10/221003d_mondai.pdf |
  | R3 | https://dobokujira.com/wp-content/uploads/2021/10/r3_1dobokuA_gakka_doboku.pdf | https://dobokujira.com/wp-content/uploads/2021/10/r3_1dobokuB_gakka_doboku.pdf | https://dobokujira.com/wp-content/uploads/2021/10/r3_1doboku_gakka_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2021/10/r3_1doboku_jitti_doboku.pdf |

- **どぼくじら.com 直リンク（2級土木、主要分のみ抜粋）**:

  | 年度 | 後期 1次問題 | 後期 1次解答 | 前期 1次問題 | 前期 1次解答 |
  |---|---|---|---|---|
  | R7 | https://dobokujira.com/wp-content/uploads/2025/10/R7_2doboku_01_late_mondai.pdf | https://dobokujira.com/wp-content/uploads/2025/10/R7_2doboku_01_late_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2025/06/R7_2doboku_01_early_mondai.pdf | https://dobokujira.com/wp-content/uploads/2025/06/R7_2doboku_01_early_kaitou.pdf |
  | R6 | https://dobokujira.com/wp-content/uploads/2024/10/R6_2doboku_01_late_mondai.pdf | https://dobokujira.com/wp-content/uploads/2024/10/R6_2doboku_01_late_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2024/06/20240603d_mondai.pdf | https://dobokujira.com/wp-content/uploads/2024/06/20240603d_seitou.pdf |
  | R5 | https://dobokujira.com/wp-content/uploads/2023/12/20231023d_mondaia1.pdf | https://dobokujira.com/wp-content/uploads/2023/12/20231023d_seitou.pdf | https://dobokujira.com/wp-content/uploads/2023/06/20230605d_mondaia.pdf | https://dobokujira.com/wp-content/uploads/2023/06/20230605d_seitou.pdf |

  ※ R4・R3 も同ページに掲載あり（ページから随時取得可）。2次試験問題は後期分のみ。

- **備考**:
  - JCTCから正式許諾を得ている旨がページ内に明記されているため、データ取得ソースとして一次に準じて扱って良い。
  - 第一次検定の正答は公式で公開、第二次検定の正答は公式では非公表（記述式のため）。
  - 1級の第一次は午前A・午後Bの2部制でPDFが別。

---

## 4. 1級・2級 管工事施工管理技士

- **主催団体**: 一般財団法人 全国建設研修センター（JCTC）
- **各試験ページ**:
  - 1級: https://www.jctc.jp/exam/kankouji-1/
  - 2級: https://www.jctc.jp/exam/kankouji-2/
- **過去問公開状況（公式）**: 令和7年度のみ
- **公式直リンク（R7）**:
  - 1級 第一次 問題A: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/09/20250908k_mondaia.pdf
  - 1級 第一次 問題B: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/09/20250908k_mondaib.pdf
  - 1級 第一次 正答肢: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/09/20250908k_seitou.pdf
  - 1級 第二次 問題: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/12/20251208k_mondai.pdf
  - 2級 第一次（後期）問題: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/11/20251117k_mondaia.pdf
  - 2級 第二次（後期）問題: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/11/20251117k_mondaib.pdf
  - 2級 第一次（後期）正答肢: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/11/20251117k_seitou.pdf
  - 2級 第一次（前期）問題: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/06/20250602k_mondai.pdf
  - 2級 第一次（前期）正答: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/06/20250602k_seitou.pdf
- **過年度（どぼくじら.com、1級管工事 R3〜R7）**:

  | 年度 | 1次A | 1次B | 1次解答 | 2次問題 |
  |---|---|---|---|---|
  | R7 | https://dobokujira.com/wp-content/uploads/2025/12/R7_1kan_01_mondaiA.pdf | https://dobokujira.com/wp-content/uploads/2025/12/R7_1kan_01_mondaiB.pdf | https://dobokujira.com/wp-content/uploads/2025/12/R7_1kan_01_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2025/12/R7_1kan_02_mondai.pdf |
  | R6 | https://dobokujira.com/wp-content/uploads/2024/09/R6_1kan_01_mondaiA.pdf | https://dobokujira.com/wp-content/uploads/2024/09/R6_1kan_01_mondaiB.pdf | https://dobokujira.com/wp-content/uploads/2024/09/R6_1kan_01_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2025/01/R6_1kan_02_mondai.pdf |
  | R5 | https://dobokujira.com/wp-content/uploads/2024/08/R5_1kan_01_mondaiA.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R5_1kan_01_mondaiB.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R5_1kan_01_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R5_1kan_02_mondai.pdf |
  | R4 | https://dobokujira.com/wp-content/uploads/2024/08/R4_1kan_01_mondaiA.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R4_1kan_01_mondaiB.pdf | https://dobokujira.com/wp-content/uploads/2024/09/R4_1kan_01_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R4_1kan_02_mondai.pdf |
  | R3 | https://dobokujira.com/wp-content/uploads/2024/08/R3_1kan_01_mondaiA.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R3_1kan_01_mondaiB.pdf | https://dobokujira.com/wp-content/uploads/2024/09/R3_1kan_01_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R3_1kan_02_mondai.pdf |

- **過年度（どぼくじら.com、2級管工事 R3〜R7）**:
  - 一覧ページ: https://dobokujira.com/2kan-pastproblems/
  - 前期/後期別に全年度掲載あり（URLはページ参照、ファイル名規則 `R{X}_2kan_01_{early|late}_{mondai|kaitou}.pdf`）。
- **備考**: 1級管工事の第一次は A/B 2部制。2級は前期は第一次のみ、後期は1次+2次。

---

## 5. 1級・2級 電気工事施工管理技士

- **主催団体**: 一般財団法人 建設業振興基金（**建築と同じ主催・同じサーバー**）
- **公式サイト**: https://www.fcip-shiken.jp/
- **過去問公開状況**: 建築と同じく r03〜r07 全年度あり（HTTP 200 確認済み）
- **命名規則**:
  - 1級 第一次: `r{XX}_1dg_mondai.pdf`
  - 1級 第二次: `r{XX}_1dj_mondai.pdf`
  - 2級 後期 第一次: `r{XX}_2dg_mondai.pdf`
  - 2級 後期 第二次: `r{XX}_2dj_mondai.pdf`
  - 2級 前期 第一次: `r{XX}_2dgz_mondai.pdf`
- **直リンク（抜粋、R3〜R7 全40URLアクセス可）**:
  - R7 1級1次: https://www.fcip-shiken.jp/pdf/r07_1dg_mondai.pdf
  - R7 1級2次: https://www.fcip-shiken.jp/pdf/r07_1dj_mondai.pdf
  - R6 1級1次: https://www.fcip-shiken.jp/pdf/r06_1dg_mondai.pdf
  - R5 1級1次: https://www.fcip-shiken.jp/pdf/r05_1dg_mondai.pdf
  - R4 1級1次: https://www.fcip-shiken.jp/pdf/r04_1dg_mondai.pdf
  - R3 1級1次: https://www.fcip-shiken.jp/pdf/r03_1dg_mondai.pdf
  - （2級・2次も r{03〜07}_{1dg,1dj,2dg,2dj,2dgz} の形で全存在を `curl -I` で確認済）
- **備考**: 建築と同じスキャフォールドなので、建築用の整形パイプラインをそのまま使い回せる。

---

## 6. 1級・2級 造園施工管理技士

- **主催団体**: 一般財団法人 全国建設研修センター（JCTC）
- **試験ページ**:
  - 1級: https://www.jctc.jp/exam/zouen-1/
  - 2級: https://www.jctc.jp/exam/zouen-2/
- **公式直リンク（R7）**:
  - 1級 第一次 問題A: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/09/20250908z_mondaia.pdf
  - 1級 第一次 問題B: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/09/20250908z_mondaib.pdf
  - 1級 第一次 正答肢: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/09/20250908z_seitou-2.pdf
  - 1級 第二次 問題: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/12/20251208z_mondai.pdf
  - 2級 第一次（後期）問題: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/11/20251117z_mondaia.pdf
  - 2級 第二次（後期）問題: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/11/20251117z_mondaib.pdf
  - 2級 第一次（後期）正答肢: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/11/20251117z_seitou.pdf
  - 2級 第一次（前期）問題: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/06/20250602z_mondai.pdf
  - 2級 第一次（前期）正答: https://www.jctc.jp/wjctcp/wp-content/uploads/2025/06/20250602z_seitou.pdf
- **過年度（どぼくじら.com、1級造園 R3〜R7）**:

  | 年度 | 1次A | 1次B | 1次解答 | 2次問題 |
  |---|---|---|---|---|
  | R7 | https://dobokujira.com/wp-content/uploads/2025/12/R7_1zouen_01_mondaiA.pdf | https://dobokujira.com/wp-content/uploads/2025/12/R7_1zouen_01_mondaiB.pdf | https://dobokujira.com/wp-content/uploads/2025/12/R7_1zouen_01_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2025/12/R7_1zouen_02_mondai.pdf |
  | R6 | https://dobokujira.com/wp-content/uploads/2024/09/R6_1zouen_01_mondaiA.pdf | https://dobokujira.com/wp-content/uploads/2024/09/R6_1zouen_01_mondaiB.pdf | https://dobokujira.com/wp-content/uploads/2024/09/R6_1zouen_01_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2025/01/R6_1zouen_02_mondai.pdf |
  | R5 | https://dobokujira.com/wp-content/uploads/2024/08/R5_1zouen_01_mondaiA.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R5_1zouen_01_mondaiB.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R5_1zouen_01_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R5_1zouen_02_mondai.pdf |
  | R4 | https://dobokujira.com/wp-content/uploads/2024/08/R4_1zouen_01_mondaiA.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R4_1zouen_01_mondaiB.pdf | https://dobokujira.com/wp-content/uploads/2024/09/R4_1zouen_01_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R4_1zouen_02_mondai.pdf |
  | R3 | https://dobokujira.com/wp-content/uploads/2024/08/R3_1zouen_01_mondaiA.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R3_1zouen_01_mondaiB.pdf | https://dobokujira.com/wp-content/uploads/2024/09/R3_1zouen_01_kaitou.pdf | https://dobokujira.com/wp-content/uploads/2024/08/R3_1zouen_02_mondai.pdf |

- **過年度（どぼくじら.com、2級造園 R3〜R7）**:
  - 一覧: https://dobokujira.com/2zouen-pastproblems/
  - 前期/後期全年度掲載あり、ファイル名規則 `R{X}_2zouen_01_{early|late}_{mondai|kaitou}.pdf`

---

## 7. 1級・2級 建設機械施工技士

- **主催団体**: 一般社団法人 日本建設機械施工協会（JCMA）
- **公式サイト（試験）**: https://jcmanet-shiken.jp/
- **過去問ページ**: https://jcmanet-shiken.jp/kako-shiken-mondai/
- **過去問公開状況**:
  - **公式方針として「試験翌日から1年間」のみ掲載**。令和7年度のみアクセス可能。令和6年度以前は公式からは消えている。
  - 問題PDFと正答PDF（「正解」と呼称）は別ファイルで公開。ただし1級第二次検定（記述式）は「正答は公表しない」と明記。
- **公式直リンク（R7、日本語ファイル名はURLエンコード必要 / `①②` などの丸数字を含む）**:
  - 1級 第一次 試験問題: `https://jcmanet-shiken.jp/gijutsu-kentei-shiken/wp-content/uploads/2025/06/①１級第一次検定（択一式）試験問題.pdf`
  - 1級 第一次 正解: `https://jcmanet-shiken.jp/gijutsu-kentei-shiken/wp-content/uploads/2025/06/⑰１級第一次検定（択一式）正解.pdf`
  - 2級 共通 試験問題: `https://jcmanet-shiken.jp/gijutsu-kentei-shiken/wp-content/uploads/2025/06/②２級第一次検定（択一式共通）試験問題.pdf`
  - 2級 種別（1〜6種）試験問題: `③〜⑧２級第一次検定（択一式種別第{1..6}種）試験問題.pdf`
  - 2級 共通 正解: `⑱２級第一次検定（択一式共通）正解.pdf`
  - 2級 種別 正解: `⑲２級第一次検定（択一式種別）正解.pdf`
  - 1級 第二次 試験問題: `⑳１級第二次検定（記述式）試験問題.pdf`（正答は非公表）
  - 2級 第二次 試験問題: `㉑２級第二次検定（択一式）試験問題.pdf`
- **過年度**:
  - どぼくじら.com には建設機械施工技士の専用ページなし（確認済み）。
  - 非公式サイト `nekomaru.site` が令和6年度を含む過去問まとめを公開しているが、一次許諾の有無は不明。
  - Wayback Machine（`https://web.archive.org/web/*/jcmanet-shiken.jp/*`）でスナップショット確認が必要。
- **備考**:
  - 2級に「6種別」があり試験構造が複雑。データ整形コストが他より高く、PoC範囲に入れるメリットは薄い。
  - Mac Mini側CLAUDEの設計書（NEXT_TASK）との整合では、**PoC段階ではスコープ外**が自然。汎化検証用にR7の一次だけ評価に混ぜるのは選択肢。

---

## 8. （参考）1級建築士・2級建築士

- **主催団体**: 公益財団法人 建築技術教育普及センター（JAEIC）
- **過去問ページ**:
  - 1級建築士: https://www.jaeic.or.jp/shiken/1k/1k-mondai.html
  - 2級建築士: https://www.jaeic.or.jp/shiken/2k/2k-mondai.html
- **1級建築士 学科試験 直リンク（R3〜R7、確認済みの規則）**:

  | 年度 | 学科I・II | 学科III | 学科IV・V | 合格基準 |
  |---|---|---|---|---|
  | R7 | https://www.jaeic.or.jp/assets/pdf/shiken/1k/1k-mondai/1k-2025-1st-gakka1_2.pdf | https://www.jaeic.or.jp/assets/pdf/shiken/1k/1k-mondai/1k-2025-1st-gakka3.pdf | https://www.jaeic.or.jp/assets/pdf/shiken/1k/1k-mondai/1k-2025-1st-gakka4_5.pdf | https://www.jaeic.or.jp/assets/pdf/shiken/1k/1k-mondai/1k-2025-1st-gokakukijun.pdf |
  | R6 | .../1k-2024-1st-gakka1_2.pdf | .../1k-2024-1st-gakka3.pdf | .../1k-2024-1st-gakka4_5.pdf | .../1k-2024-1st-gokakukijun.pdf |
  | R5 | .../1k-2023-1st-gakka1_2.pdf | .../1k-2023-1st-gakka3.pdf | .../1k-2023-1st-gakka4_5.pdf | .../1k-2023-1st-gokakukijun.pdf |
  | R4 | .../1k-2022-1st-gakka1_2.pdf | .../1k-2022-1st-gakka3.pdf | .../1k-2022-1st-gakka4_5.pdf | .../1k-2022-1st-gokakukijun.pdf |
  | R3 | .../1k-2021-1st-gakka1_2-r.pdf | .../1k-2021-1st-gakka3.pdf | .../1k-2021-1st-gakka4_5.pdf | .../1k-2021-1st-gokakukijun.pdf |

- **備考**:
  - 4択・5択式中心。施工管理技士とは別試験だがドメイン近接。データ多様化案として選択肢。
  - ページ注記に「個人利用以外の無断転載・複製禁止」とある → **学習用データセットとして再配布するならライセンス扱い注意**。FTモデルの重み内に問題文が「記憶」として残る可能性まで考慮すべき。

---

## 非公式だが参考になるソース

| サイト | 用途 | 備考 |
|---|---|---|
| [どぼくじら.com](https://dobokujira.com/) | 土木・管工事・造園・建築の過去問PDFアーカイブ | **JCTCから正式に過去問公開許諾を受けている**と明記。最も信頼できる二次ソース。 |
| [nekomaru.site](https://nekomaru.site/) | 施工管理6種＋建設機械の過去問まとめ | 許諾の明示なし。出典・解説の精度を要検証。 |
| [my-s-pace.jp](https://my-s-pace.jp/kakomon.html) | 施工管理技士・建設業経理士等の問題集 | 有料商材が主。 |
| [kakomonn.com](https://kakomonn.com/) | オンラインで解ける過去問Q&A形式 | **解説付き**のテキストが取れるかもしれないが、解説の著作権は運営側にあり学習データ化NG。問題文のクロスチェック用に留める。 |
| [sekou-kyujin.com](https://sekou-kyujin.com/) | 施工管理系の無料クイズ | 学習データ化は非推奨。 |
| [CIC日本建設情報センター](https://www.cic-ct.co.jp/sohyo/) | 解答速報＋総評 | 直近1年分の解答確認用。 |
| [九州建設専門学院](https://www.touhokugiken.com/answer/) | 解答試案PDF | 実地（記述）試験の想定解答。公式ではないが評価参考用。 |

---

## 調査メモ

### 見つからなかった・アクセス不可だったもの

- **JCTC 過年度 過去問PDF（公式）**: 令和6年度以前の `20240707d_mondaia.pdf` 等は全て 404。JCTCは過去問を公式サイトに蓄積しない方針。
- **JCMA 過年度 過去問PDF（公式）**: 同様に過年度は公式から消える。公式以外のソースでも完全なアーカイブは未発見。
- **公式解説PDF**: いずれの試験も公式は解説なし。これは CLAUDE.md の方針どおり、自作要約または別LLMでの解説合成が必要。

### PoCで使うデータの推奨方針

1. **まず1級建築施工管理技士の第一次検定（`r03〜r07_1kg_mondai.pdf`）5本を fcip-shiken から取得**。
   - R3〜R6を学習、R7を評価用。
   - 四肢択一＋五肢択二の「応用能力問題」でQA整形。
2. データ量が不足する場合は **2級建築施工管理技士 + 1級電気工事施工管理技士** を追加（同じサーバー・同じ命名規則なので整形コストが極小）。
3. さらに広げる場合のみ、JCTC配下（土木・管工事・造園）を dobokujira.com 経由で追加。
4. 汎化検証のために**1試験種holdout**するなら、1級造園または1級管工事が候補（建築と傾向が離れているため）。

### 著作権・ライセンス所感

- 施工管理技士の過去問：問題文そのものには通常著作権は発生しない（公の試験問題のため）が、解答や解説には著作権が発生しうる。**公式が公開しているのは「問題＋正答肢（選択肢番号）」のみ**で、解説は各社独自。→ 学習データに解説を入れる場合は自作またはLLM合成一択。
- 成果物（Hugging Face公開予定モデル）の README に「学習データ = 各主催団体が公開する過去問（問題文＋正答）から作成した instruction-tuning データ」と明記すれば、再配布リスクは低い。**ただしデータセットそのものの公開は慎重に**（問題文をそのまま公開するとグレー）。

### データ取得スクリプトを書くなら

- `fcip-shiken.jp` 側は完全に規則的なので、`for year in r03..r07: for suffix in [1kg, 1kj, 2kg, 2kj, 2kgz, 1dg, 1dj, 2dg, 2dj, 2dgz]:` のネストでダウンロード関数が1本書ける。
- JCTC側は個別にURLリスト化が必要（日付ベースで規則性が弱い）。dobokujira.com側も同様。
- `jcmanet-shiken.jp` は日本語URLエンコードが必要で、1級/2級/種別ごとに手動マッピング。
