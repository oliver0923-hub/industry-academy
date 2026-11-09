# 第 37 課｜易讀修訂與網站整合紀錄

**日期**：2026-11-09  
**正式課次**：37（出版、新聞、影視、音樂、串流與內容平台）  
**版本狀態**：可閱讀候選稿／編輯審查中，非正式出版。

## 依據與來源

- 原始草稿：`codex/lesson-37-prep-drive-bridge-20261109:editorial/lessons/lesson-37/draft.md`，在此分支原檔直接修訂，並選取單一最新版手動移交 `main:editorial/lessons/lesson-37/draft.md`。
- Google Drive `research/notes/lessons/lesson-37/index.md`：確認出版、新聞、影視、音樂及串流的子領域、官方資料入口與研究邊界。此索引的來源狀態為 metadata，不能取代正式數值核查。
- Google Drive `research/notes/lessons/lesson-37/acquisition-v2.md`：作為既有原始來源盤點；部分來源仍 identified／restricted／broken／fulltext_available_unreviewed。該檔的「原始文件可用 11、已核讀研究 0、已定位數值 0」是**先前批次**，不代表日後的草稿或本次編輯沒有引用。
- 原稿附 13 筆學術、官方與企業原始來源（包括 DGBAS、Waldfogel、Rochet-Tirole、Gentzkow、IFPI、Netflix 10-K、文策院、華研國際年報等）；本文這次**不新增推定數據**，只做可讀性修訂。

## 使用者需求及完成內容

使用者希望第 37 堂「更順暢」，並要求根據 `editorial/lessons/lesson-37/draft.md` 和雲端 Drive 資料。實施：

1. 保留原課的導讀→內容產製→出版／新聞／影視／音樂→媒介歷史→串流→獲利與談判→全球／台灣→AI→結語。沒有改寫成只談 Netflix 的課程。
2. 第一輪逐段修訂 **72 處**（章節題名、段落開頭、長句、轉場及部分重複名詞），第二輪額外處理 5 處相鄰段落重複及排版。
3. 主標題改為「一本書、一首歌、一部影集：內容產業如何運作？」；主要章節標題改採容易直接理解的提問句，仍保留 14 段正文、課後問題、實務情境、術語與參考文獻。
4. 保留原有的正文引用與來源連結，不改寫 Netflix、IFPI、華研等已在原稿列出的主要數字和會計單位。以數據本身建立解釋，避免把公司營收等同市場規模。
5. 將修訂版複製至 `main:editorial/lessons/lesson-37/draft.md`（母稿），生成 `main:docs/lesson-37-reading.html`（網站來源內容）。這是**選取檔案移交**，不是把整個研究／草稿分支的舊網站合併到 main。
6. 更新 `docs/lesson-reader.js` 中的 `sourceFiles[37]`，以及 `docs/lesson.html` 的可讀課次守門、`docs/app.js` 的課程候選稿狀態與舊 `#lesson/37` 轉向，保留「總目錄→下一頁課文」架構。

## 品質與限制

- 文字：經過兩輪編輯，未新增未查核的統計數值或企業事實；仍有出版級語言精修空間。
- 完整性：16 個二級章節標題（含導讀及文獻）、13 筆參考來源；網站由共用課文閱讀器載入。
- 來源：原檔共有 13 筆文末參考資料，並有 17 處正文來源標記（全文共 30 個含文末書目編號的 [序號]）；本輪主要核對引用**仍保留**，不是逐份重新查核所有 PDF 的完整出版審查。
- 出版四關：原件事實與資料口徑 **部分／待獨立稽核**；學術機制 **已保留、待獨立審讀**；零基礎語言 **完成本輪編修**；獨立第二輪 **未完成**。
- 技術：需區分「HTML 結構與 JavaScript 語法檢查」與「公開 GitHub Pages 端到端桌機／手機測試」。沒有實際跑過的檢查不得標註通過。
- 若未來追加經驗數據或改寫數值，須先從對應原始官方表格、公司年報及期刊原文重新核對；不可只從舊來源盤點推定。

## 下一次啟動

「以 `main:editorial/lessons/lesson-37/draft.md` 為最新母稿，檢查 `docs/lesson-37-reading.html` 與 `lesson.html?lesson=37`。若要正式發布，完成四階段內容審查、台灣不同內容子領域量值補證及實際 Pages 端到端測試，不再重做網站底層。」
