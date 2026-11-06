# 第18堂 Evidence Pack｜IC設計、代工、記憶體與封測

核對批次2026-11-06。評估：**部分環節充分；四環節全課不足**。本包支援限定主題撰稿，未標記整課完成或teaching-ready。

## 講義論證順序

原始微影設備研究說明架構知識；Intel與TSMC提供不同企業邊界的財報例子，貿易資料另列商品範圍。

## 已核對原文與適用邊界

- [Rebecca M. Henderson; Kim B. Clark（1990）](papers/P007.md)：主導設計使架構知識內嵌在溝通管道、資訊過濾與解題慣例；元件仍熟悉但連結改變時，原有知識反而遮蔽新問題。 定位：印刷 p.12 Figure 1；pp.19–20（資料）；p.24 Table 2；pp.25–28（案例及限制）；PDF pp.5,12–13,17–21。 邊界：單一設備產業，其他因素也影響失去領導地位；Table 2各技術生命週期不完整，尤其第二代步進機；不能外推EUV或現代AI需求的因果效果。
- [Jay Barney（1991）](papers/P003.md)：資源異質性與不完全移動性，使有價值、稀少、難模仿且不存在可行策略等價替代的資源可能維持優勢；歷史條件、因果模糊及社會複雜性限制模仿。 定位：印刷 pp.101–103（定義）,105–112（條件）,113–117（例示及意涵）；PDF pp.3–5,7–14,15–19；PDF p.7已視覺核對。 邊界：價值取決於環境；結構衝擊可使原資源失去價值；替代性需另行檢驗，非成功企業事後貼標籤。
- [Gary Gereffi; John Humphrey; Timothy Sturgeon（2005）](papers/P005.md)：資訊複雜度、可編碼性與供應商能力共同決定協調需要與依賴；形成市場、模組、關係、俘虜與階層五種分析類型。 定位：印刷pp.83–87（類型與Table1）,96–99（動態、結論及邊界）；PDFpp.6–10,19–22；頁碼=PDF+77。 邊界：三變數如何動態演變僅部分解釋；標準會失效或競爭，關係不必單向走向模組化；上游參數設定者、消費者與地方制度亦重要。
- [David J. Teece; Gary Pisano; Amy Shuen（1997）](papers/P009.md)：整合、建立與重組內外部competences；組織及管理processes受資產positions與累積paths塑造，學習與重組並受複製／模仿難度影響。 定位：印刷pp.515–516（定義）,518–524（processes/positions/paths及複製）,527 Table1（典範比較）,528–529（限制與策略意涵）；PDFpp.8–9,11–17,20–22；上述掃描頁已視覺閱讀。 邊界：作者承認框架仍在發展，不能自信給出強規範結論；成功不能反向當作能力測量；不是把後來sensing/seizing/transforming架構倒填為本篇的三構面。

## 已核對統計或財報觀察

|ID|觀察|數值與單位|期間|定位與口徑限制|
|---|---|---|---|---|
|O_GLOBAL_CHIPS|World chips_exports_lower_bound|1300000000000 USD|2022|PDF29 / report29; Appendix D TableD.6 PDF58；strict lower bound > value；Published as MORE THAN1.3trillion, not exact. Re-exports/cross-border double counting; not global sales.|
|O_TW_CHIPS_SHARE|Chinese Taipei share_of_world_basket_exports|28.1 percent|2022|PDF30 Figure3.12；as_published；Not a foundry market share; do not combine with2024 IC amount.|
|O_TW_IC_PRIMARY|Taiwan IC_exports|165042 USD million|2024|printed3/PDF3 Table2; printed17/PDF17 Table4 first column113年；rounded USD million；2025-01-09 preliminary publication, not latest revised2024 series. Taxonomy remains different from broad OECD basket.|

完整來源URL、身份及SHA見[sources.csv](sources.csv)；觀察值及定義見[observations.csv](observations.csv)。

## 企業案例

- [INTEL](cases/INTEL.md)：已讀年度財務表，尚不代表完整產業個案或機制識別。
- [TSMC](cases/TSMC.md)：已讀年度財務表，尚不代表完整產業個案或機制識別。

## 尚待驗證主張與資料缺口

官方IC純商品全球總額與台灣同年同HS表；IC設計／記憶體／封測分項及原始研究；TSMC兩套會計淨利差異明細待核。

## 不可直接寫入講義的推論

不能由企業一年營收推算全球市場；不能混用商品、產業、企業與金控；不能由概念模型填入虛構樣本；不能將統計關聯改寫為因果效果。候選索引仍是待查來源，只有上述具定位的內容可作目前證據。

## 撰稿前檢查

逐項對照[衝突清單](conflicts.csv)及[充分性評估](sufficiency.csv)。每個引用保留版次與原文定位；工作稿頁碼和HTML定位不能偽裝為正式期刊PDF頁碼。
