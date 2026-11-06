# 本輪執行回報

基礎：9a5f648；研究分支codex/research-source-foundation。查核日期2026年11月6日。

實際新增下載16個不同SHA原件（{'.pdf': 9, '.html': 7}），原始檔全私存。這含摘要頁、官方報告與年報，不能稱16篇已讀論文。新增39筆逐主張核對，承接55筆既有查核，共94筆。新讀1篇JPE2020期刊格式原文的核心章節、1篇Basker2007作者稿核心章節；都記錄閱讀範圍，沒有宣稱全文逐行核讀。

新增資料：ILO WESO2025全文及摘要、Census NAICS更新流程、Walmart官方史、LOC Ford廠史、TSMC1998原始年報、JPE機器人論文、MOEA零售2024表、IEA EV2025章節、JPM官方史、FTC附負擔、NYU作者稿、裕隆2024年報、TTVMA汽車統計、MOEA電動車政策；另有AEA摘要頁。

| 課號 | 本包查核主張 | 本輪新增 | 完整初稿 | 主要阻斷缺口 |
|---|---:|---:|---|---|
| 00 | 11 | 5 | 尚未充分 | 還缺分類制度完整國際沿革、產品市場與行業差異的對照案例、一般讀者術語表證據。 |
| 01 | 47 | 6 | 尚未充分 | 還缺一致年度與分類之世界各產業附加價值、地區就業及跨國比較時間序列。 |
| 05 | 21 | 2 | 尚未充分 | 還缺台灣農地、農戶、勞動與作物長期史；糧食政策與風險；大成轉型歷程的逐年原證。 |
| 18 | 24 | 4 | 尚未充分 | 還缺電晶體與IC發明原始史料、設備材料／EDA／先進封裝技術、製程政策及全球產銷同口徑資料。 |
| 25 | 15 | 15 | 尚未充分 | 還缺台灣車廠完整財報核讀、整車與零組件統計、ICE／BEV技術、經銷與售後、關稅及在地化政策。 |
| 30 | 16 | 16 | 尚未充分 | 還缺世界一致定義零售統計、台灣代表企業經營及財報、百貨／超商／電商長期轉型史、期刊正式版及原始實證。 |
| 31 | 17 | 1 | 尚未充分 | 還缺中央銀行與存保制度歷史、銀行監理與資本風險、兆豐合併前後原始史料，以及全球銀行總量一致系列。 |

各課共享主張不加總為獨立主張。450列缺口全數映射到使用者九類，另建七課63項具體需求；沒有因重分類而關閉缺口。

失敗／受限：本輪Ford企業歷史頁restricted、Basker2005 PDF broken、AEA正式期刊PDF restricted；替代原件分別為LOC廠史、無替代2005原文、NYU2007作者稿。舊有限制及MCD文字編碼問題保留。完整狀態見run_summary.json及既有failures報告。

圖像：七課具體自行重繪方案，未複製照片或期刊圖版，也未宣稱任何照片授權已取得。

下一批請接續同分支：先看七課teaching_readiness_report.md；優先補05農業長期制度與農戶資料、31銀行與存保歷史、18設備材料原證、25交通部原表及汽車企業查核意見、30台灣零售企業財報及全球同口徑數據。沿用claims.csv逐主張證據欄位；不得靠候選或PDF筆數結案。

續跑命令（PowerShell、repository根目錄）：
```powershell
python research/scripts/full_acquisition.py fetch --lessons 00,01,05,18,25,30,31 --resume --skip-verified --max-files-per-run 20
python research/scripts/validate_full_acquisition.py
python research/scripts/build_teaching_foundation.py
python research/scripts/validate_teaching_foundation.py
python research/scripts/validate_deep_evidence.py
python research/scripts/validate.py
```

下載器與驗證器會寫入同一狀態檔，必須依序執行。build_teaching_foundation.py保存的是本批固定人工核讀；新人工核讀應追加到新批次或更新生成來源，避免只改生成CSV後被重建覆蓋。

未修改公開網站、M&A Academy或部署設定；未使用Railway；未將全文或快取加入公開Git。驗證結果見validation.json及既有三組verification_report。自動驗證不能代替四階段出版審查。

本輪實際驗證：新證據包197/197、完整蒐集流程127/127、既有深度證據49/49、研究結構40/40；git diff --check通過。未將上述結果等同四階段出版審查。
