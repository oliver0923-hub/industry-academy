# 第05堂｜農業：研究證據包

研究用途，非正式教材，未通過四階段出版審查。查核日期：2026年11月6日。

以Tyson雞肉整合鏈與大成飼料／食品經營對照，補出農戶在價值鏈的位置。

## 可追溯事實

- `I_O_FAO_CEREALS` World：cereal_production = 3100000000 tonnes〔FAO agricultural production；release Key findings: cereals reached3.1 billion tonnes〕
- `I_O_FAO_MEAT` World：meat_production = 374000000 tonnes〔FAO agricultural production；release Key findings:374 million tonnes〕
- `I_O_TW_AG_NARROW` Taiwan：agricultural_product_value = 582848000000 TWD〔農業部113年施政年報；二、國內農業發展情勢 first paragraph〕
- `I_O_TW_AG_BROAD` Taiwan：gross_agricultural_output = 709800000000 TWD〔農業部名目生產總額；113年農林漁牧業生產總額; 指標說明一、二〕
- `I_C_TYSON_sales` Tyson Foods Inc.：sales = 53309 USD million〔Tyson Foods Inc.；printed44 / PDF45〕
- `I_C_TYSON_cost_of_sales` Tyson Foods Inc.：cost_of_sales = 49682 USD million〔Tyson Foods Inc.；printed44 / PDF45〕
- `I_C_TYSON_gross_profit` Tyson Foods Inc.：gross_profit = 3627 USD million〔Tyson Foods Inc.；printed44 / PDF45〕
- `I_C_TYSON_operating_income` Tyson Foods Inc.：operating_income = 1409 USD million〔Tyson Foods Inc.；printed44 / PDF45〕
- `I_C_TYSON_net_income` Tyson Foods Inc.：net_income = 822 USD million〔Tyson Foods Inc.；printed44 / PDF45〕
- `I_C_TYSON_net_income_parent` Tyson Foods Inc.：net_income_parent = 800 USD million〔Tyson Foods Inc.；printed44 / PDF45〕
- `I_C_DACHAN_sales` Great Wall Enterprise Co. Ltd. / 大成長城企業1210：sales = 102749063 TWD thousand〔大成長城企業及子公司；PDF8 / printed6; annual PDF144 cross-check〕
- `I_C_DACHAN_cost_of_sales` Great Wall Enterprise Co. Ltd. / 大成長城企業1210：cost_of_sales = 87948997 TWD thousand〔大成長城企業及子公司；PDF8 / printed6; annual PDF144 cross-check〕
- `I_C_DACHAN_gross_profit` Great Wall Enterprise Co. Ltd. / 大成長城企業1210：gross_profit = 14800066 TWD thousand〔大成長城企業及子公司；PDF8 / printed6; annual PDF144 cross-check〕
- `I_C_DACHAN_operating_income` Great Wall Enterprise Co. Ltd. / 大成長城企業1210：operating_income = 5336706 TWD thousand〔大成長城企業及子公司；PDF8 / printed6; annual PDF144 cross-check〕
- `I_C_DACHAN_net_income` Great Wall Enterprise Co. Ltd. / 大成長城企業1210：net_income = 4416069 TWD thousand〔大成長城企業及子公司；PDF8 / printed6; annual PDF144 cross-check〕
- `I_C_DACHAN_net_income_parent` Great Wall Enterprise Co. Ltd. / 大成長城企業1210：net_income_parent = 3529389 TWD thousand〔大成長城企業及子公司；PDF8 / printed6; annual PDF144 cross-check〕
- `I_B_TYSON_CHICKEN` Tyson Foods：chicken_segment_sales = 16425 USD million〔Tyson Foods Inc.；printed28/PDF29; Note17 printed78/PDF79〕
- `I_B_DACHAN_FEED` Great Wall Enterprise group：feed_product_revenue = 53300579 TWD thousand〔大成長城企業及子公司；PDF67/printed64 Note6(26)〕
- `I_B_DACHAN_TONNES` Great Wall Enterprise Company：company_feed_sales_volume = 1370000 tonnes〔大成長城企業；PDF127/printed122 Feed products〕
- `N_TYSON_HISTORY` Tyson於1935年由John W. Tyson創立。〔Tyson Foods Inc.；PDF4 / printed3 Item1 Business / General〕
- `N_TYSON_CHAIN` Tyson雞肉業務涵蓋育種、契約農戶、飼料、加工、行銷與運輸。〔Tyson Foods Inc.；PDF4 / printed3 Item1 Business / General〕

## 歷史與企業故事的證據界線

Tyson1935只是一個歷史節點，不能代表世界農業史；飼料食品集團不是典型小農。

年代事件見[時間線](../timelines.csv)，每項以claim_id回查[主張表](../claims.csv)。本課沒有事件列的時期仍是缺口，不以推測補齊。既有六家企業財報查核見[前批研究包](../../deep-2026-11-06/README.md)。

## 原文核讀與適用範圍

- Jay Barney (1991)，original journal scan; OCR。核讀：印刷 pp.101–103（定義）,105–112（條件）,113–117（例示及意涵）；PDF pp.3–5,7–14,15–19；PDF p.7已視覺核對。。限制：價值取決於環境；結構衝擊可使原資源失去價值；替代性需另行檢驗，非成功企業事後貼標籤。。來源`S_barney_1991`。
- Oliver E. Williamson (1979)，original journal with JSTOR cover。核讀：印刷 p.239（三維度）,pp.247–253（治理配適）,259–261（意涵）；PDF pp.8,16–22,28–30。。限制：須同時衡量生產經濟、交易成本及設計；資本市場應用改以可驗證性討論；不是任何大型企業都有效率的證據。。來源`S_williamson_1979`。
- Gary Gereffi; John Humphrey; Timothy Sturgeon (2003)，2003-11-04 author manuscript; NOT 2005 journal pagination。核讀：作者稿自身 pp.6–8（PDF pp.7–9；Table 1在PDF p.9）；作者稿 p.15（PDF p.16）動態限制。不得填2005版pp.78–104為已核對定位。。限制：稿本並非最終期刊版；動態演變只獲部分解釋，不能把模組化視為不可逆必然趨勢。。來源`S_gvc_author_manuscript`。
- Eva-Marie Meemken; Marc F. Bellemare (2020)，original full HTML; issue117(1):259–264; online2019-12-13。核讀：HTML Results/Table 2、Discussion、Materials and Methods；已讀正式全文HTML，尚未取得有效PDF，精確印刷頁碼待核；259–264僅為書目頁範圍。。限制：選擇偏誤仍可能存在；缺失所得、契約細節不足、僅六國小農；不能據此宣稱台灣契作使所得因果提高9.97%。。來源`S_pnas_contract`。
- Gary Gereffi; John Humphrey; Timothy Sturgeon (2005)，original journal12(1):78–104; FAO-hosted copy。核讀：印刷pp.83–87（類型與Table1）,96–99（動態、結論及邊界）；PDFpp.6–10,19–22；頁碼=PDF+77。。限制：三變數如何動態演變僅部分解釋；標準會失效或競爭，關係不必單向走向模組化；上游參數設定者、消費者與地方制度亦重要。。來源`S_gvc_journal_2005`。

## 價值鏈、商業模式與競爭機制

種苗／飼料 → 農場及契約農戶 → 加工冷鏈 → 批零與餐飲 → 消費者。這是研究者的概念化整理，不是經估計的市場流量。支撐入口：N_TYSON_CHAIN;I_B_DACHAN_FEED；未有逐環節直接證據的部分列為待驗證，不將示意圖冒充已觀察到的產業結構。

Tyson1935只是一個歷史節點，不能代表世界農業史；飼料食品集團不是典型小農。

## 待驗證主張與缺口

還缺台灣農地、農戶、勞動與作物長期史；糧食政策與風險；大成轉型歷程的逐年原證。

產業成長是否由特定企業、政策或技術造成，尚須比較研究或原始過程資料；年度報告的管理階層解釋不可直接當作因果識別。

## 圖像方案

自行繪製上述概念流程圖，明標「概念示意、非比例圖」，附claim IDs。數據圖只可取用已核對同口徑值，不複製PDF圖版。照片逐張授權尚未取得，不能使用公司網站圖片當作免授權素材。

[本課撰寫準備度](teaching_readiness_report.md)
