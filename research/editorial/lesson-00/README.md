# Lesson 00 教科書候選稿

從這裡開始：[完整教材候選稿](candidate.md)。原課綱保留，使用10個敘事單元，包含世界與台灣、企業故事、原創圖、5題理解問題、1個假設情境、術語與原始來源。

這是研究分支中的候選稿，**尚未達到正式發布或網站實作放行條件**。未修改公開網站，未合併main。

- [敘事大綱](outline.md)：問題推進、每節需要的證據與取捨。
- [逐主張來源對應](claim_to_source.csv)：37項來源支持的事實／理論陳述，以及8項明示假設或條件推導；二者不能合併稱45項經驗事實。
- [來源及核讀範圍](sources.csv)：21個實際核讀來源記錄，包含既有原件。fulltext_read限所列範圍，不代表逐行讀完全書。
- [數值與缺值](observations.csv)：世界銀行原始值、美國null與台灣同版兩年數值；不把null當0，不混版本。
- [圖表方案與授權](figure_plan.csv)：3張已繪製SVG，區分概念、假設、官方數值重繪，沒有第三方照片或期刊原圖。
- [出版審查報告](publication_review.md)、[逐節四關紀錄](section_reviews.csv)、[未解問題](unresolved_issues.csv)。
- [可重現品質檢查](validation.json)：檢查通過不等於出版審查通過；獨立審閱尚未完成。

本輪只定向補00課：既有下載器的`L00_*`任務及一個獨立GDP metadata補充請求，原件與QA快照仍在被忽略的private_sources。EU入口下載失敗未採為正文證據；其餘限制見acquisition紀錄。沒有以下載數量設定充分性門檻。

重建來源及圖表，不覆寫人工正文：

```powershell
python research/scripts/fetch_lesson00_gdp_definition.py
python research/scripts/prepare_lesson00_publication.py
python research/scripts/validate_lesson00_publication.py
python research/scripts/validate_deep_evidence.py
python research/scripts/validate.py
```

修改正文後，必須實際再審讀受影響段落，再更新section_reviews.csv的判斷與候選稿SHA，不可只為通過檢查而自動改SHA。既有全庫下載器與validate_full_acquisition.py會寫共用狀態，須序列執行。

下一輪最小續跑指令：接續本分支的Lesson00 candidate.md，先處理P002的世界部門加總口徑（補一項明確原始方法證據或縮減該表），再安排未參與撰寫的獨立審閱者完成P001；逐項修訂與複核後才判斷是否可網站實作。不必擴張七堂課，不以更多PDF代替審稿。
