# 正式教材證據研究包｜2026年11月6日

以9a5f648為基礎，優先00、01、05、18、25、30、31。這是研究成果，七課均尚未具備完整10,000–15,000字初稿所需證據，也未完成出版審查。

- [逐主張證據](claims.csv)：new_original_read與inherited_verified_observation分開；supporting_content為研究者中文釋義，不是原文逐字引文。
- [來源與閱讀範圍](sources.csv)：fulltext_read只代表所列核心章節實際核讀，不表示逐行讀完全篇。claim_verified只放在逐主張表，不把文件全面升級。
- [核讀卡](literature_readings.csv)：新增JPE2020期刊排版未編頁copy與Basker2007作者稿；正式JEP PDF受限，作者稿不冒充正式版。前批已核讀文獻保留血緣。
- [450舊缺口映射](gap_reclassification.csv)：450列全保留，多重分類，沒有因重分類而結案。分類資料不能替代產品技術資料。
- [七課63項需求](priority_requirements.csv)、[準備度](readiness.csv)、[時間線](timelines.csv)、[圖像方案](figure_plans.csv)。

閱讀狀態：bibliography_only=只識別；abstract_verified=僅摘要；fulltext_downloaded=取得全文未完成核讀；fulltext_read=指定範圍已核讀；claim_verified=逐項有定位且未超出來源支持。這些不是自動隨下載器推進的同義詞。來源表保留失敗與受限的bibliography_only記錄，取得全文仍須查read_scope。

複現：先執行既有full_acquisition.py fetch --lessons all --resume --skip-verified；本包可由python research/scripts/build_teaching_foundation.py重建（原始查核內容固定於程式，原件不公開）。再跑validate_teaching_foundation.py、validate_full_acquisition.py、validate_deep_evidence.py、validate.py。來源的公開可讀不等於可重散布，原始PDF/HTML全部留在忽略的private_sources。

後續逐課進入lesson-NN/teaching_readiness_report.md；先補阻斷缺口，不以候選來源數量當完成率。
