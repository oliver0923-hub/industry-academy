# Industry Academy｜全球產業、台灣經濟與企業策略研究學院

這是 Industry Academy 的獨立網站與課程內容儲存庫，依照 **Industry Academy Master Project Instructions v2.0（2026-11-06）** 建置。

## 網站目前進度

**第一階段：首頁與課程導覽已建立。** 目前包含：
- 天藍色響應式首頁（桌面與手機版）
- 50 堂正式課程的完整目錄（00–49）
- 九個網站主題導覽群組（源自 v2.0 的九組課程章節；指令文件稱「十個模組」，後續如修訂課綱再同步）
- 課程搜尋、篩選、各課介紹佔位頁與推薦學習路徑
- 儲存在本機瀏覽器的課程介紹閱讀標記

**注意：尚未發布正式教材。** 課程頁中清楚標註正式講義、來源核對、測驗與三回合管理決策模擬仍待撰寫。「已閱讀」標記不等於正式完課。

## 網站技術與部署

第一階段採用與 M&A Academy 相近的 **純 HTML、CSS 與 JavaScript 靜態架構**，無 Node.js 建置步驟，也無 Railway 或伺服器依賴。

網站原始碼位於 `docs/`：
- `docs/index.html`：首頁骨架
- `docs/styles.css`：淺藍色視覺與 RWD
- `docs/app.js`：50 堂課目錄、搜尋、導航、進度
- `docs/.nojekyll`：GitHub Pages 靜態檔案設定

將來可在 GitHub 儲存庫 **Settings → Pages → Deploy from a branch → main → /docs** 啟用部署（須視帳號方案與儲存庫可見性是否支援 GitHub Pages）。未啟用前不代表網站已上線。

## 內容設計準則

每堂完整教材依 v2.0 規定涵蓋：產業邊界、歷史、全球市場、價值鏈、台灣環境、產業經濟學、全球及台灣企業、挑戰、決策模擬、學術研究及測驗。

這個儲存庫**完全獨立於 M&A Academy**，不修改其 GitHub 專案，也不使用 Railway。
