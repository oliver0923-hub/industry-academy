# 18｜半導體I：IC設計、晶圓代工、記憶體、封裝測試

這是來源盤點，不是教材。狀態：claim_checked_partial。

原始文件可用（SHA去重）19；已核讀研究5；已定位數值20。

## 已有來源與下載層級

- C_TW_SIC_11｜官方分類 11｜identified｜https://www.stat.gov.tw/StandardIndustrialClassification.aspx?RID=11&n=3144&sms=11195
- C_TW_SIC_FILES_11｜官方分類 11｜identified｜https://www.stat.gov.tw/News_Content.aspx?n=3144&s=90015
- C_NAICS_2022｜官方分類 2022｜fulltext_downloaded｜https://www.census.gov/naics/
- C_SIC_1987｜官方分類 1987｜restricted｜https://www.osha.gov/data/sic-manual
- C_TWSE_accessed_2026-11-06｜官方分類 accessed_2026-11-06｜identified｜https://twse-regulation.twse.com.tw/TW/law/DOC01.aspx?FLCODE=FL007104&FLNO=2
- C_ISIC_5｜官方分類 5｜identified｜https://unstats.un.org/unsd/classifications/Econ/isic
- C_ISIC_4｜官方分類 4｜fulltext_downloaded｜https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/ISIC_Rev_4_english_structure.Txt
- G_TIVA｜Trade in Value Added｜restricted｜https://www.oecd.org/en/topics/sub-issues/trade-in-value-added.html
- G_COMTRADE｜UN Comtrade｜identified｜https://comtradeplus.un.org/
- G_UNIDO｜Industrial Statistics Databases｜restricted｜https://stat.unido.org/
- G_STAN｜Structural Analysis Database｜restricted｜https://www.oecd.org/en/data/datasets/structural-analysis-database.html
- T_MOEA｜產業經濟統計｜identified｜https://www.moea.gov.tw/Mns/dos/home/Home.aspx
- T_TRADE｜海關進出口統計｜identified｜https://portal.sw.nat.gov.tw/APGA/GA30
- T_MOEA_IP｜工業生產指數開放CSV（資料集6607）｜fulltext_downloaded｜https://service.moea.gov.tw/EE520/opendata/d.csv
- V2_TW12_META｜行業統計分類XML詮釋資料｜failed｜https://data.gov.tw/dataset/14321
- V2_TW12_MANUAL｜行業統計分類第12次修正｜fulltext_downloaded｜https://ws.dgbas.gov.tw/001/Upload/463/ebook/ebook_356166/pdf/full.pdf
- V2_SMITHSONIAN_CHIP｜Integrated circuits｜restricted｜https://americanhistory.si.edu/collections/object/nmah_334900
- V2_TWSE_FILINGS｜上市公司每月營業收入 openAPI｜fulltext_downloaded｜https://openapi.twse.com.tw/v1/opendata/t187ap05_L
- D_6fad5a97cd76｜NAICS Update Process Fact Sheet｜fulltext_downloaded｜https://www.census.gov/naics/reference_files_tools/NAICS_Update_Process_Fact_Sheet.pdf
- D_1cb5b0c805ae｜2022 NAICS Manual｜fulltext_downloaded｜https://www.census.gov/naics/reference_files_tools/2022_NAICS_Manual.pdf
- T_TSMC_1998｜1998 annual report introduction｜fulltext_downloaded｜https://investor.tsmc.com/static/annualReports/1998/html/intro.htm
- P003｜Firm Resources and Sustained Competitive Advantage｜fulltext_verified｜https://doi.org/10.1177/014920639101700108
- P009｜Dynamic Capabilities and Strategic Management｜fulltext_verified｜https://doi.org/10.1002/(SICI)1097-0266(199708)18:7<509::AID-SMJ882>3.0.CO;2-Z
- Xdac2a4a6b｜The dynamics of product innovation and firm competences｜metadata_verified｜https://doi.org/10.1002/smj.275
- Xc64db7c78｜Supply Chain Decoupling: Geopolitical Debates and Economic Dynamism in East Asia｜metadata_verified｜https://doi.org/10.1111/aepr.12439
- W_GVC_2003｜The governance of global value chains｜fulltext_verified｜
- F012｜Intel｜identified｜https://www.intc.com/filings-reports/annual-report
- F047｜台積電｜identified｜https://investor.tsmc.com/english/annual-reports
- D_F047｜台積電｜fulltext_downloaded｜https://investor.tsmc.com/sites/ir/annual-report/2024/2024-Annual%20Report-E.pdf
- DEEP_INTEL｜Intel Corporation｜fulltext_downloaded｜https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-25-000052/a2024arsform10-k.pdf
- S_teece_1997_copy｜Teece/Pisano/Shuen1997｜fulltext_verified｜https://www.edegan.com/pdfs/Teece%20Pisano%20Shuen%20%281997%29%20-%20Dynamic%20capabilities%20and%20strategic%20management.pdf
- S_gvc_journal_2005｜Gereffi et al.2005｜fulltext_verified｜https://www.fao.org/fileadmin/user_upload/fisheries/docs/GVC_Governance.pdf
- S_mof_2024_release｜財政部113年12月海關進出口統計｜claim_verified｜https://service.mof.gov.tw/public/Data/statistic/trade/news/11312/11312_中文新聞稿(本文及附表).pdf
- S_barney_1991｜Barney 1991｜fulltext_verified｜https://josephmahoney.web.illinois.edu/BA545_Fall%202022/Barney%20%281991%29.pdf
- S_henderson_1990｜Henderson & Clark 1990｜fulltext_verified｜https://josephmahoney.web.illinois.edu/BA549_Fall%202018/Session%206/6_Henderson_Clark%20%281990%29.pdf
- S_gvc_author_manuscript｜Gereffi et al.｜fulltext_verified｜https://www.soc.duke.edu/sloan_2004/Papers/governance_of_gvcs_final.pdf
- S_oecd_semiconductor_pdf｜OECD semiconductor value chain｜claim_verified｜https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/06/mapping-the-semiconductor-value-chain_5ba52971/4154cdbf-en.pdf
- S_mof_ic_cbc｜CBC引財政部IC出口｜claim_verified｜https://www.cbc.gov.tw/tw/dl-214361-52675b5be9054196a29b247c7fc775a9.html
- S_intel_2024｜Intel Corporation｜claim_verified｜https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-25-000052/a2024arsform10-k.pdf
- S_tsmc_20f_2024｜TSMC and subsidiaries｜claim_verified｜https://investor.tsmc.com/sites/ir/sec-filings/2024%2020-F.pdf
- S_tsmc_annual｜TSMC 2024 annual report｜claim_verified｜https://investor.tsmc.com/sites/ir/annual-report/2024/2024-Annual%20Report-E.pdf

## 尚缺

設計/代工/記憶體/封測同年統計；TSMC會計差異調節；歷史/圖像權利/跨產業主張仍須逐項核對。所有課均不足以宣稱已完成10,000–15,000字出版級教材。

研究問題、子產業與學習範圍沿用本課index.md；本輪不補寫沒有來源的歷史或研究發現。
