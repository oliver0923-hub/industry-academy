# Phase 4

已執行合法原始檔、官方報告、分類與樣本資料下載；每次成功或失敗均記錄 audit/download_log.csv。詳見 sources/artifact_inventory.csv、coverage_report.md 及 counts.json。

分類 crosswalk 發現官方台灣第11次對照 XLSX 英文表頭仍寫Rev.10,2016，中文寫第11次；保留為版本衝突，禁止直接合併。NAICS2022–2017 官方對照另存，不推導 SIC–NAICS 或台灣–NAICS 字面映射。

限制：部分 HTTP 403/429、動態頁面、全文授權與機構會話未可用；不把入口頁當成資料或正式財報。研究卡多數為書目與候選機制，實質全文閱讀完成者才另補頁碼、方法與發現。
