# Lesson 00 網站先行閱讀版本

使用者在5870f05之後明確指示「先放上」，授權將候選稿提供網站先行閱讀。這項授權覆蓋先前「本輪不改網站、不合併main」的操作限制，但不把P001、P002變成已解決，也不宣稱出版四關已全部通過。

沿用GitHub Pages main/docs。網站頁首顯示「教材候選稿・審閱中」，說明獨立審讀與世界統計加總口徑仍待核對，保留正文待核對註記。此次部署狀態為public_candidate_preview，不是formal_publication。

部署前已讀遠端main d58c86b，發現已有舊00與01閱讀頁；以該main為部署基底，只更新00頁、00專用CSS/JS、三張SVG及app.js中00入口文字。保留既有Lesson01、首頁與共用樣式。研究分支同步保留main已有01原件以便完整本機預覽，不將整條研究分支合併至main。

build_lesson00_site.py從候選稿產生靜態HTML及圖片副本，HTML內保留candidate SHA供核對；依賴見research/requirements-site.txt。閱讀器支援桌機固定／手機折疊目錄、捲動位置、恢復上次位置、獨立自行標記及原生dialog圖表放大。標記僅此瀏覽器使用，不視為測驗或審稿通過，也不覆寫既有課程導覽標記。

本機實測：1440×1000桌機、390×844手機無頁面水平溢出；11個二級標題、27個來源註記、3張圖；圖表放大及ESC、閱讀恢復、自行標記、00入口、01入口均通過，無pageerror；六個閱讀資源HTTP200。另比對main的Lesson01、index.html及styles.css，除平台行尾外完全相同。重現工具：check_lesson00_site.py --url http://127.0.0.1:8876。

網址：https://oliver0923-hub.github.io/industry-academy/lesson-00.html 。部署後另核對公開HTTP內容與同一候選稿SHA。

未改M&A Academy，未使用Railway，沒有公開原始第三方全文或private_sources。舊研究驗證器中「網站完全未改」是過去研究批次的保全斷言，不用它否定本次明確授權的網頁變更；研究事實與四關紀錄維持原狀。
