# Industry Academy｜全球產業、台灣經濟與企業策略研究學院

> **注意：這個研究分支中的網站敘述是歷史快照，不代表現行 GitHub Pages。** 最新網站原始碼與課程閱讀器位於 `main:/docs`，目錄點選後進入 `lesson.html?lesson=NN`。研究分支不可覆寫主站。最新跨工具流程見 [製課 SOP](project/COURSE_PRODUCTION_PLAYBOOK.md)、[Codex 交接模板](project/LESSON_HANDOFF_TEMPLATE.md)、[ChatGPT 啟動指令](project/CHATGPT_STARTUP_INSTRUCTIONS.md)、[第 02 課實作紀錄](project/LESSON_02_OPERATION_LOG.md)。兩分支的 `AGENTS.md` 已同步；出版決策仍以 [編輯規範](EDITORIAL_TEACHING_STANDARDS.md) 為準。

這是 Industry Academy 的獨立網站與課程內容儲存庫。教材編輯依據為[正式教學與編輯規範 v1.0](EDITORIAL_TEACHING_STANDARDS.md)；原 **Industry Academy Master Project Instructions v2.0（2026-11-06）** 的課程目錄、課程邊界及未被取代的基本研究原則繼續適用。

執行 repository 任務前，請先閱讀 [AGENTS.md](AGENTS.md) 及完整編輯規範。

## 網站目前進度

**第一階段：首頁與課程導覽已建立。** 目前包含：
- 天藍色響應式首頁（桌面與手機版）
- 50 堂正式課程的完整目錄（00–49）
- 九個網站主題導覽群組（源自 v2.0 的九組課程章節；指令文件稱「十個模組」，後續如修訂課綱再同步）
- 課程搜尋、篩選、各課介紹佔位頁與推薦學習路徑
- 儲存在本機瀏覽器的課程介紹閱讀標記

**注意：尚未發布正式教材。** 現有課程頁仍有早期模板的測驗與三回合模擬佔位說明；新編輯規範已取消這些強制要求，網站需另行依授權修訂。本次規範落檔不修改網站。「已閱讀」標記不等於正式完課。

## 網站技術與部署

第一階段採用與 M&A Academy 相近的 **純 HTML、CSS 與 JavaScript 靜態架構**，無 Node.js 建置步驟，也無 Railway 或伺服器依賴。

網站原始碼位於 `docs/`：
- `docs/index.html`：首頁骨架
- `docs/styles.css`：淺藍色視覺與 RWD
- `docs/app.js`：50 堂課目錄、搜尋、導航、進度
- `docs/.nojekyll`：GitHub Pages 靜態檔案設定

將來可在 GitHub 儲存庫 **Settings → Pages → Deploy from a branch → main → /docs** 啟用部署（須視帳號方案與儲存庫可見性是否支援 GitHub Pages）。未啟用前不代表網站已上線。

## 內容設計準則

完整教材以零基礎讀者可理解的產業敘事為主，涵蓋產業邊界、歷史、運作機制、全球與台灣位置、價值鏈、競爭及代表企業。章節與案例配置依產業調整；不強制固定 11 章、數值工具或三回合模擬。課末原則上有 3–5 個理解問題、一個產業情境、術語表與完整來源；正式發布須有四階段審查紀錄。完整 20 項決策及執行要求見[編輯規範](EDITORIAL_TEACHING_STANDARDS.md)。

這個儲存庫**完全獨立於 M&A Academy**，不修改其 GitHub 專案，也不使用 Railway。
