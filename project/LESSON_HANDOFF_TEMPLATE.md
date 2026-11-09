# Industry Academy｜下一堂課交接模板（ChatGPT × Codex）

**版本**：v1.0｜2026-11-09  
**用法**：以本模板生成「針對某一堂課」的可執行工作書，**不是讓 Codex 一次亂抓 50 堂**。執行決策以 [製課總流程](COURSE_PRODUCTION_PLAYBOOK.md) 與 [正式教學規範](../EDITORIAL_TEACHING_STANDARDS.md) 為準。

## A｜使用者最簡單的提案方式

使用者可以只寫：

> 「開始製作第 NN 堂。希望加入＿＿產業／事件／企業／台灣案例。照 Industry Academy 標準，先查現有研究資料與 GitHub：資料足夠就寫教材並整理網站；不足就先給 Codex 精確抓取指令。」

或：

> 「針對第 NN 堂，再把＿＿段寫得更容易懂；保留引用、數字、圖表與網站閱讀方式。」

這兩句已足夠啟動，不要求重複貼上先前的完整規範。對新課先盤點、再判定 GO/FETCH；對已有課則先檢視現有最新主稿。

## B｜ChatGPT 必須填寫的 Lesson Brief

```yaml
lesson_id: "NN"
official_title: "Master v2.0 對應正式課名"
request_type: "new | revise | evidence_topup | site_fix"
user_focus: "本次希望處理的具體問題"
target_reader: "一般零基礎讀者"
one_sentence_hook: "一個具體生活／企業情境"
core_questions:
  - "這個產業實際在做什麼？"
  - "它為何形成這種全球與台灣分工？"
  - "誰創造哪些價值、負擔哪些成本與風險？"
key_global_cases: []
key_taiwan_cases: []
necessary_historical_turns: []
core_statistics:
  - "來源／實際指標／年份／單位／地理／官方分類"
academic_mechanisms:
  - "具體經驗問題，而不是只列管理理論縮寫"
existing_assets:
  branch: ""
  evidence_pack_paths: []
  available_originals: []
  verified_claims: []
critical_gaps:
  - "缺口／阻礙章節／需要的原始證據"
readiness: "GO | FETCH"
decision_reason: ""
```

**GO**：關鍵主張可連至已取得、已核對的原始來源，可直接進入 D（寫作）。  
**FETCH**：無法核實重要數字、歷史、技術、企業決策或研究主張，先產出以下 Codex 任務；允許對其他已有證據的章節先寫初稿，但不得假裝未解主張已證實。

## C｜給 Codex 的可複製完整指令骨架

> 請在 GitHub `oliver0923-hub/industry-academy` 為第 `NN` 堂〈`課名`〉完成**原始來源取得、逐項核對、研究證據包整理**。本次**不撰寫完整公開教材，不修改 `docs/`、不發布網站**。
>
> **先讀指令**：根目錄 `AGENTS.md`、`EDITORIAL_TEACHING_STANDARDS.md`、`project/COURSE_PRODUCTION_PLAYBOOK.md`、`project/LESSON_HANDOFF_TEMPLATE.md`；研究分支另讀 `research/README.md`、對應課的 `research/notes/lessons/lesson-NN/index.md`、相關 Evidence Packs 與 `research/audit/full-acquisition-v2/`。若檔案或分支不存在，先記錄，不能虛構。
>
> **分支邊界**：研究基底為 `codex/research-source-foundation`，先檢查 status、最新 SHA、既有工作和快取，再建立 `codex/lesson-NN-evidence-YYYYMMDD`。保留已核讀版本，不強制覆蓋或重新下載；禁止直接修改 `main` 與網站。不得操作其他 Academy 或 Railway。
>
> **本課問題與研究需求**（由 ChatGPT 必須填完才能交 Codex）：
>
> 1. `P0｜資料與定義：官方來源網址 + 真正需要的表／系列 / 年份 / 地理 / 單位 / 分類及成功驗收條件`
> 2. `P0｜台灣對照：主管機關、原始統計表、國別/活動/公司口徑、特定年份`
> 3. `P0｜歷史/技術/政策：事件日與公告日、原始紀錄、機制及限制`
> 4. `P1｜期刊：完整 DOI、正式版本、核心主張、全文核讀／只取摘要的區別`
> 5. `P1｜企業：正式年報/10-K/20-F/主管機關，具體可核對的決策、財報與製造/服務狀態`
> 6. `P2｜圖與跨課連結：真實數據的可重製圖，概念示意需明確標記；素材授權`
>
> **方法**：先 source inventory、DOI/官方穩定 ID/SHA 去重；使用研究庫既有 `full_acquisition.py`、`validate*.py` 時，先檢查 `--help` 與實際檔案，必要時用 `--dry-run`、`--lessons NN`、`--resume --skip-verified` 限量續跑。取得實際文件後才可標示 downloaded；逐頁/逐表讀到支持主張的證據後才可標示 claim_verified。官方首頁或 HTTP 200 不能取代原表。下載不應繞過權限、驗證碼、robots 或付費牆。
>
> **必要資料欄位**：來源 ID、文件身分與版本、出版日和資料期間、下載或取用網址、合法權利、實際原檔路徑與 SHA、數據定義／觀察值／單位／名目或實質／地理、引用精確定位、是否核讀、衝突與反例。論文要保留理論／實證區別、樣本與識別限制；企業要保留公司宣稱／客觀觀察／推論區別。
>
> **目錄成果**：`research/evidence/lesson-NN-YYYY-MM-DD/` 下至少輸出 `README.md`、`source_inventory.csv`、`claims_evidence.csv`、`indicator_series.csv`、`literature_reviews.md`、`company_cases.md`、`history_timeline.csv`、`figure_spec.md`、`gaps.csv`、`quality_review.md`。對不適用項可空表加說明，但不可捏造觀察。受限全文放 Git 忽略的 `private_sources/`；公開 Git 只提交合法公開原創成果。
>
> **最後驗收**：列出本次真實抓取、重用、逐項核驗、失敗、受限的數量；提供工作分支與 commit、資料表與原文件的可重現路徑、執行過的測試結果、阻礙發布的缺口。GitHub 結果不等於所有原檔已自動出現在下一個執行環境。請提供可移交給 ChatGPT 的 ZIP 或 repository 明確路徑及 manifest。**只交研究材料，不自行宣布網站已發布。**

若某來源無法取得，Codex 應提交「已嘗試方法、失敗原因、官方替代來源、缺口對教材的影響」，而非以其他年度或不同指標代填。

## D｜Codex 完成後，交給 ChatGPT 的接續指令

> 「第 NN 堂的研究資料已抓取，見附加 ZIP／GitHub branch＋commit：＿＿。請實際盤點和讀取原始來源、統計原表及 literature review，區分可用、不可比、尚待補充；必要時只讓 Codex 補最重要缺口。資料足夠時，依編輯規範完成 10,000–15,000 中文字正文為參考的繁體中文敘事教材。優先讓沒有專業背景的人理解，並將真實歷史、全球與台灣多元企業放進故事。保留逐項來源、年份、單位、統計口徑、反例、術語和 3–5 個理解問題；不得為了寫完整而杜撰。」
>
> 「文章完成後，請更新 `main:/docs` 的教材內容與共用閱讀器，使課程從 `index.html#catalog` 點選後進入 `lesson.html?lesson=NN` **下一個頁面**完整顯示；調整 `lesson-reader.js`、`lesson.html` 的可讀課次及目錄狀態；驗證手機／桌機、章節、進度、圖表和真實 Pages 部署，完成四階段審查紀錄。未完成審查仍標記教材候選稿。」

**ChatGPT 自行完成 D–H** 是預設安排；只有明確被授權的獨立網站程式任務，才另交 Codex 修改 `docs/`。

## E｜每次最後必附的交付清單

```text
[ ] 課號、正式課名、當輪修改需求已確認
[ ] 採用的研究包／研究分支及 commit 可重現
[ ] 重要原始文件與表格已實際閱讀，不只看 metadata
[ ] 主張／年份／幣別／單位／國別／分類有可追溯來源
[ ] 文獻版本、方法與推論限制正確
[ ] 台灣與全球代表活動均交代，不只列公司名
[ ] 故事→機制→證據的敘事合理；術語首次有白話解釋
[ ] 參考資料、概念示意與資料圖授權正確
[ ] 網站目錄→獨立閱讀頁→上/下一堂動線正確
[ ] 章節、圖表、按鈕、桌機與手機可用
[ ] 四關審查明列已做、未做及阻擋原因
[ ] GitHub branch/commit 與 GitHub Pages 實際上線狀態分開回報
[ ] 內部操作日誌與下一次啟動指令已更新
```

**下一堂課不需複製上一次 02 課特有的 Nike、TiVA 或 FDI 任務**；應沿用工作格式，但依新產業真正需要的來源、學術與公司材料改寫。
