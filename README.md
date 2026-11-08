# Industry Academy｜全球產業與台灣經濟的開放教材

這是一套以繁體中文撰寫、適合零基礎讀者的產業教科書網站，涵蓋 00–49 共 50 堂課。課程製作遵循《Industry Academy Master Project Instructions v2.0》之課綱及《正式教學與編輯規範 v1.0》之寫作、引用及發布品質規定。

## 網站與閱讀動線

- [首頁／課程目錄](https://oliver0923-hub.github.io/industry-academy/index.html#catalog)：搜尋、篩選及點選 50 堂課
- [第 00 堂：產業分類](https://oliver0923-hub.github.io/industry-academy/lesson.html?lesson=00)
- [第 01 堂：產業如何賺錢](https://oliver0923-hub.github.io/industry-academy/lesson.html?lesson=01)
- [第 02 堂：全球產業分工](https://oliver0923-hub.github.io/industry-academy/lesson.html?lesson=02)

所有目錄項目均導向 **獨立的課程閱讀頁** `lesson.html?lesson=NN`，不在首頁邊欄中直接插入長篇教材。00–02 為可閱讀、仍待正式審查的教材候選稿；03–49 尚未有完整講義，顯示「編寫中」而不冒充已發布。從舊連結 `index.html#lesson/NN` 進入時，會跳轉至新閱讀頁。

閱讀頁使用 `lesson-reader.js` 與 `lesson-reader.css`，提供章節目錄、進度條、接續閱讀、字級切換、自行標記完成、圖表放大，以及上一堂／下一堂導航；位置和標記僅存在讀者當前瀏覽器。

第 02 堂於 2026-11-09 完成易讀語氣修訂：保留原始來源與經核對的數值，調整較密集的定義及研究敘事，採用鞋業、台灣企業與歷史故事帶出概念。仍不得標記為「正式發布」，直到事實與資料、推論、教學及獨立第二輪審讀完成。

## 程式結構

```text
docs/
  index.html            # 學院首頁及目錄
  app.js                # 50 堂目錄與導覽
  styles.css            # 首頁視覺
  lesson.html           # 50 堂共用的獨立閱讀入口
  lesson-reader.js      # 讀取、目錄、進度與圖片
  lesson-reader.css     # 專用閱讀版面
  lesson-00-reading-v2.html
  lesson-01.html
  lesson-02-reading.html
```

舊有三份完整 HTML 教材保留為資料來源，以便歷史版本與內部核對。研究原始文件與未授權散布的全文不可加入公開 GitHub 儲存庫。

部署方式：GitHub Pages 使用 `main` 分支的 `/docs` 目錄；網站純 HTML／CSS／JavaScript，無額外建置程序。此專案獨立於 M&A Academy。
