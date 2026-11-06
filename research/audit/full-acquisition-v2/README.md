# 全50課原始來源蒐集 v2｜本輪交付

本輪不撰寫教材；所有50課仍不足以宣稱出版級完成。前八課研究、原始資料與桌面ZIP皆保留，ZIP只檢查CRC而不重複解壓匯入。

盤點614個本地檔案，其中243個具下載來源記錄的來源檔，依SHA去重238個。這些包含詮釋資料，不等於同數量的學術全文。書目DOI已核對34筆；本輪新核對3筆Crossref及1篇PMC身份。

本輪有效新下載27份：PDF11、HTML12、JSON4、CSV0；另重用6份。26份格式/文字擷取正常，MCD1份PDF內文編碼異常需OCR。新核對12筆官方數值，保存來源/資料年份/定位/範圍；不以原文可用冒稱已閱讀研究內容。

目前52個已嘗試任務：下載27、重用6、技術失敗6、失效5、受限7、容量暫緩1（衛福年報英文版；已取得中文版）。累計53次實際嘗試，包含先暫緩後成功的中文版重試。另4個待下載附件候選、3個不適用候選已停用。

入口：[50課涵蓋](../coverage_report.md)、[450列逐課九類缺口](lesson_gaps.csv)、[最新盤點](current_inventory.csv)、[去重來源檔](deduplicated_local_sources.csv)、[身份別名](identity_groups.csv)、[失敗與限制](restricted_and_failures.csv)、[品質](verification_report.md)、[續跑](../next_actions.md)。

TW12解析892列，20大類/88中類/254小類/530細類；自2026-01-01生效。TW11的878列保留歷史註記。20筆新大類跨版關係依原文拆分及遞移，不將其充當細類crosswalk。

原始檔位於被忽略的private_sources/full-v2，舊快取維持原位；公開只存書目、索引、必要事實與研究筆記。每次實際嘗試存acquisition_attempts_v2.csv，download_log.csv為latest view。來源狀態與教材完成狀態分開；HTTP200錯誤頁已降級broken，原始嘗試仍保留。

哈希樣本：

|檔案|SHA-256|
|---|---|
|private_sources/full-v2/V2_TW12_MANUAL.pdf|fd731b678b5ab3a0fcfa7cf7bb049ae3308706d3a52a5202763396eb74d7a446|
|private_sources/full-v2/V2_USGS26.pdf|595e6e66674236dea40125a03eb1ea6b347f331c0bcf3411a1e77eba53c0d391|
|private_sources/full-v2/V2_NBER_EDTECH.pdf|3e124ec08b2b60846f34632c81def2e736efc34b41b8e09097397fe6133ce19f|
|private_sources/full-v2/V2_MOHW113_A.pdf|34a9d4e51130dd02751263c3d797a082e6605f3b6030f7ff3ac996efb42c0173|
