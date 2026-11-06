# 第04堂 Evidence Pack｜研究方法與證據核對

核對批次2026-11-06。評估：**限定範圍可寫初稿**。本包支援限定主題撰稿，未標記整課完成或teaching-ready。

## 講義論證順序

用原文理論／實證區分、家戶所得關聯與銀行模型、財報版本衝突做可重現核對示範。

## 已核對原文與適用邊界

- [Oliver E. Williamson（1979）](papers/P004.md)：專用性投資形成雙邊依賴，在有限理性與機會主義下產生適應／議價風險；反覆交易可攤提專門治理成本。 定位：印刷 p.239（三維度）,pp.247–253（治理配適）,259–261（意涵）；PDF pp.8,16–22,28–30。 邊界：須同時衡量生產經濟、交易成本及設計；資本市場應用改以可驗證性討論；不是任何大型企業都有效率的證據。
- [Rebecca M. Henderson; Kim B. Clark（1990）](papers/P007.md)：主導設計使架構知識內嵌在溝通管道、資訊過濾與解題慣例；元件仍熟悉但連結改變時，原有知識反而遮蔽新問題。 定位：印刷 p.12 Figure 1；pp.19–20（資料）；p.24 Table 2；pp.25–28（案例及限制）；PDF pp.5,12–13,17–21。 邊界：單一設備產業，其他因素也影響失去領導地位；Table 2各技術生命週期不完整，尤其第二代步進機；不能外推EUV或現代AI需求的因果效果。
- [David J. Teece; Gary Pisano; Amy Shuen（1997）](papers/P009.md)：整合、建立與重組內外部competences；組織及管理processes受資產positions與累積paths塑造，學習與重組並受複製／模仿難度影響。 定位：印刷pp.515–516（定義）,518–524（processes/positions/paths及複製）,527 Table1（典範比較）,528–529（限制與策略意涵）；PDFpp.8–9,11–17,20–22；上述掃描頁已視覺閱讀。 邊界：作者承認框架仍在發展，不能自信給出強規範結論；成功不能反向當作能力測量；不是把後來sensing/seizing/transforming架構倒填為本篇的三構面。
- [William Ocasio（1997）](papers/P014.md)：選擇性焦點、情境化注意力與注意力結構分配三原則相連；規則、參與者、位置、資源透過程序與溝通管道，使特定議題及答案進入決策。 定位：印刷p.188（三原則）,pp.189–192（原則與模型）,196–201（結構與管道）,202–203（調適、結論）；PDFpp.2–6,10–17；頁碼=PDF+186。 邊界：不是完整可估計的企業行為理論；結構與認知如何交互作用仍需發展；不能由會議提到某議題就證明資源已重新配置。
- [Eva-Marie Meemken; Marc F. Bellemare（2020）](papers/D_PNAS_2020.md)：契作可改善市場與投入品取得，但也有選擇與參與障礙；所得及雇工關係須依地區檢驗。 定位：HTML Results/Table 2、Discussion、Materials and Methods；已讀正式全文HTML，尚未取得有效PDF，精確印刷頁碼待核；259–264僅為書目頁範圍。 邊界：選擇偏誤仍可能存在；缺失所得、契約細節不足、僅六國小農；不能據此宣稱台灣契作使所得因果提高9.97%。
- [Douglas W. Diamond; Philip H. Dybvig（1983）](papers/X69013d8a3.md)：長期技術與私人流動性需求形成風險分攤空間；可隨時提領且先到先付的契約在特定預期下同時支持良性與擠兌均衡。 定位：印刷 pp.405–407（模型）,410–412（停止兌付）,414–415 Proposition 2（保險）,415–417（邊界）；PDF pp.5–7,10–12,14–17。 邊界：保險結果依賴政府課稅能力等假設；未完整處理資產風險與道德風險，不表示現實保險永遠無成本或每次危機皆屬自我實現。

## 已核對統計或財報觀察

|ID|觀察|數值與單位|期間|定位與口徑限制|
|---|---|---|---|---|
|O_TW_AG_NARROW|Taiwan agricultural_product_value|582848000000 TWD|2024|二、國內農業發展情勢 first paragraph；as_published；Annual narrative includes preliminary components; not presumed latest revised yearbook; not agricultural GDP.|
|O_TW_AG_BROAD|Taiwan gross_agricultural_output|709800000000 TWD|2024|113年農林漁牧業生產總額; 指標說明一、二；rounded 億元；Broader than agricultural product value; not value added/GDP. Difference cannot be called measurement error.|
|O_FSC_MEGA|兆豐國際商業銀行# reported_total_assets|4166596 TWD million|2024-12-31|CSV key(113,12,兆豐國際商業銀行#) / 資產-總額-新臺幣百萬元；as_published；Do not silently strip # or treat as audited group consolidation; Mega differs from company financial statement.|
|O_TSMC_IASB_PROFIT|TSMC and subsidiaries net_income|1157523.9 TWD million|FY ended2024-12-31|PDF96 / F-6；as_published；Different from Taiwan annual report1172431759 thousand; do not treat as OCR error or same-basis restatement.|

完整來源URL、身份及SHA見[sources.csv](sources.csv)；觀察值及定義見[observations.csv](observations.csv)。

## 企業案例

- [TSMC](cases/TSMC.md)：已讀年度財務表，尚不代表完整產業個案或機制識別。
- [JPMBANK](cases/JPMBANK.md)：已讀年度財務表，尚不代表完整產業個案或機制識別。
- [MEGA](cases/MEGA.md)：已讀年度財務表，尚不代表完整產業個案或機制識別。

## 尚待驗證主張與資料缺口

PNAS PDF精確印刷頁碼未得；跨分類映射衝突未消除；不得把檢查程式通過視為研究識別有效。

## 不可直接寫入講義的推論

不能由企業一年營收推算全球市場；不能混用商品、產業、企業與金控；不能由概念模型填入虛構樣本；不能將統計關聯改寫為因果效果。候選索引仍是待查來源，只有上述具定位的內容可作目前證據。

## 撰稿前檢查

逐項對照[衝突清單](conflicts.csv)及[充分性評估](sufficiency.csv)。每個引用保留版次與原文定位；工作稿頁碼和HTML定位不能偽裝為正式期刊PDF頁碼。
