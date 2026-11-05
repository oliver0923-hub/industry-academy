# Industry Academy — Codex Research Acquisition Plan v1.0

本文件為 Codex 建置研究來源庫的起點。詳細可執行指令另以 `Industry_Academy_Codex_Acquisition_Prompt_v1.txt` 提供使用者直接貼入 Codex。

## 目標
針對課程 00–49（不改課號），建立全球→台灣→企業→管理與學術研究之可追溯資料庫；不可將空白課程頁視為已完成正式講義。

## Phase 1（最高優先）
1. 官方分類：台灣主計總處第11次行業分類、美國 2022 NAICS、美國 1987 SIC、證交所上市產業分類；保留版次、代碼、定義、來源與核對時間。
2. 核心理論文獻：IO/SCP、Porter 五力、RBV、TCE、全球價值鏈、創新收益、吸收能力、動態能力、模組化、平台經濟、生態系、關係治理與 ABV。
3. 全球＋台灣可比較統計：DGBAS、經濟部、財政部、主計官方資料及 UN Comtrade、OECD TiVA、World Bank、IMF、IEA、UNIDO、WHO、ILO、FAOSTAT 等。分開衡量營收、產值、附加價值、GDP、出口、產能及市場規模。
4. 為每堂建立 lesson_id × source_id × role 的索引骨架；不假造來源。

## Phase 2–4
- 每堂收集全球及台灣官方來源、全球/台灣公司年報、一篇核心學術研究及 1–3 篇補充研究。
- 覆蓋農林漁牧、資源、製造、科技、運輸、金融、專業服務、文化、餐旅、醫療、教育與公共行政，不能僅集中半導體。
- 保存 DOI、官方來源網址、抓取日期、出版資訊、樣本/方法核對狀態、license、download status、checksum。
- 僅下載合法開放或使用者明確授權的原始電子檔。付費/校園授權 PDF 不提交公開 repo；絕不繞過付費牆、登入或 DRM。

## Repository 目錄
```
research/
  registries/{source_registry,literature_master,industry_lesson_matrix,company_filings,classification_master,classification_crosswalk,indicator_dictionary}.csv
  notes/theory_cards/
  notes/lessons/lesson-00 ... lesson-49/
  audit/{download_log.csv,coverage_report.md,verification_report.md,restricted_access_queue.md}
  schemas/
private_sources/  # ignored, not for public GitHub
```

## 作業安全
- 絕不修改 M&A Academy 或 railway。
- 不覆蓋現有 docs 首頁和課程程式。
- 研究工作使用獨立 branch，保留 git status 及提交紀錄。
- 每個來源標示 verified/unverified/restricted 和日期；沒有全文就不填寫虛構樣本或效果。
- 優先交付能讀取的 CSV、真實查證結果、每課覆蓋矩陣、學術研究卡和失敗清單。

## 起動
閱讀 README、專案 v2.0 指令與現有 docs/app.js，執行 Phase 1；完成後報告實際新增/可取得/受限/待核查的來源數，繼續 Phase 2。
