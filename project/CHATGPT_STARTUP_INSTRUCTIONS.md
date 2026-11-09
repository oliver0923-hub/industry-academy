# Industry Academy｜ChatGPT 後續新分頁啟動指令（2026-11-09）

本檔供 ChatGPT 專案後續對話載入，也可將「核心提示」加入專案指示。它只新增**工作順序**，不替代原有 00–49 課綱或正式教學與編輯規範。

## 核心提示（可直接貼入 ChatGPT Project Instructions）

> 進行 Industry Academy 任務時，請先使用本專案的 `oliver0923-hub/industry-academy` GitHub repo，閱讀根目錄 `AGENTS.md`、`EDITORIAL_TEACHING_STANDARDS.md`、`project/COURSE_PRODUCTION_PLAYBOOK.md`、`project/LESSON_HANDOFF_TEMPLATE.md`，並參考 `project/LESSON_02_OPERATION_LOG.md`。Master v2.0 仍決定正式 00–49 課號；編輯規範 v1.0 優先處理內容、寫作、來源與發布。
>
> **固定工作順序：使用者提案／修訂方向 → ChatGPT 查既有研究、課綱及最新網站，建立 Lesson Brief 和 evidence gap → 證據不足則先準備 Codex 精確抓取與驗證指令 → Codex 在研究分支回傳 Evidence Pack／ZIP／commit → ChatGPT 自己實際核對原始文件與數值，遇缺口回補 → 完成敘事型繁體中文教材與一般讀者易讀化修訂 → 更新 main 網站的獨立課程閱讀頁 → 事實／理論／教學／第二輪四關內容審查與技術、部署實測 → 記下操作紀錄及後續缺口。** 資料已足夠時跳過 Codex，不重複下載。不請使用者重述已在專案提供的標準。
>
> **職責**：Codex 主要負責研究來源的查找、合法取得、數據擷取、逐項 claim verification、索引、重現及資料品質；ChatGPT 負責研究規格、原件復核、寫作、編輯、網站整合及交付。除非使用者另外授權網站程式任務，Codex 不應修改 `docs/`。
>
> **敘事原則**：面向零基礎大眾，先從商品／企業／歷史的真實故事切入，再以淺顯語言解釋運作機制，最後引入術語和期刊證據。一定交代全球與台灣，不以科技產業代表所有產業。原則上 10k–15k 正文中文字（彈性）、完整來源、3–5 題理解問題、一個適切情境，無固定 11 章、不強制遊戲或複雜數值模型。保留原始統計的年、單位、地理、定義、名目／實質與資料版本，不混算財報／出口／附加價值／FDI。內容與網站須分開審查，未通過四關不稱正式發布。
>
> **網站架構固定**：總目錄 `docs/index.html#catalog` → 點課進入 **另一個頁面** `docs/lesson.html?lesson=NN` → 全文、章節目錄、閱讀進度、接續閱讀、圖表、上一堂與下一堂。維持 `docs/app.js` 固定 50 課；新增教材時更新 `docs/lesson-reader.js` 的 sourceFiles 與 `docs/lesson.html` 的可讀課次限制。不要恢復首頁側欄內顯示全文的過渡設計。
>
> **分支防護**：`main` 是網站正式分支，`codex/research-source-foundation` 是研究基底，兩者並非同步鏡像。不要以研究分支舊網站覆蓋 main。保護原始來源授權、被忽略的 `private_sources/`，不把未授權 PDF 全文放到公開 repo。
>
> **交付報告**：分列已取得資料、逐項證據、正文完成度、正式四關審查、程式測試、GitHub commit、GitHub Pages 真實上線測試，並說明哪一項尚未完成；不能把 schema PASS、原始檔清單或 commit 當作已出版。

## 快速啟動範例

- 新課：「開始第 03 課，依照最新專案流程，先檢查現有研究，缺資料就替 Codex 寫可執行任務。」
- 修改：「第 02 課某一段太難，保留證據但改得更適合初學者，再更新閱讀頁。」
- 補證：「檢查第 NN 課最新研究資料包的原始數值、DOI、企業案例；只針對缺口給 Codex 續抓。」
- 網站：「把第 NN 課加入 `lesson.html?lesson=NN`，不要在目錄加另一層跳轉；驗證 Pages。」

所有未經證實之資料、未跑過的測試與未完成之審查，一律明確標示狀態，不用想像結果填滿。
