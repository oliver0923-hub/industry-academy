# 第31堂 Evidence Pack｜銀行、存放款與信用

核對批次2026-11-06。評估：**存放款基礎可寫；全課不足**。本包支援限定主題撰稿，未標記整課完成或teaching-ready。

## 講義論證順序

銀行原始流動性模型，加上全球跨境信用與台灣逐行資產；兩家銀行本體財報對照，金控資料不代替銀行。

## 已核對原文與適用邊界

- [Douglas W. Diamond; Philip H. Dybvig（1983）](papers/X69013d8a3.md)：長期技術與私人流動性需求形成風險分攤空間；可隨時提領且先到先付的契約在特定預期下同時支持良性與擠兌均衡。 定位：印刷 pp.405–407（模型）,410–412（停止兌付）,414–415 Proposition 2（保險）,415–417（邊界）；PDF pp.5–7,10–12,14–17。 邊界：保險結果依賴政府課稅能力等假設；未完整處理資產風險與道德風險，不表示現實保險永遠無成本或每次危機皆屬自我實現。
- [Oliver E. Williamson（1979）](papers/P004.md)：專用性投資形成雙邊依賴，在有限理性與機會主義下產生適應／議價風險；反覆交易可攤提專門治理成本。 定位：印刷 p.239（三維度）,pp.247–253（治理配適）,259–261（意涵）；PDF pp.8,16–22,28–30。 邊界：須同時衡量生產經濟、交易成本及設計；資本市場應用改以可驗證性討論；不是任何大型企業都有效率的證據。

## 已核對統計或財報觀察

|ID|觀察|數值與單位|期間|定位與口徑限制|
|---|---|---|---|---|
|O_BIS_CREDIT|BIS reporting banks worldwide cross_border_credit_outstanding|32600000000000 USD|2024-12-31|Key takeaways and Graph1；rounded0.1trillion；End-period stock; not bank revenue or global market size; quarter changes adjusted for FX/breaks.|
|O_TW_BANK_ROWS|Taiwan domestic banks reported_bank_entries|38 entries|2024-12-31|CSV filters 年=113 and 月-期底=12；as_published；38 rows are reporting entries, not a bank holding-company count.|
|O_FSC_MEGA|兆豐國際商業銀行# reported_total_assets|4166596 TWD million|2024-12-31|CSV key(113,12,兆豐國際商業銀行#) / 資產-總額-新臺幣百萬元；as_published；Do not silently strip # or treat as audited group consolidation; Mega differs from company financial statement.|
|O_FSC_BOT|臺灣銀行# reported_total_assets|6583680 TWD million|2024-12-31|CSV key(113,12,臺灣銀行#) / 資產-總額-新臺幣百萬元；as_published；Do not silently strip # or treat as audited group consolidation; Mega differs from company financial statement.|

完整來源URL、身份及SHA見[sources.csv](sources.csv)；觀察值及定義見[observations.csv](observations.csv)。

## 企業案例

- [JPMBANK](cases/JPMBANK.md)：已讀年度財務表，尚不代表完整產業個案或機制識別。
- [MEGA](cases/MEGA.md)：已讀年度財務表，尚不代表完整產業個案或機制識別。

## 尚待驗證主張與資料缺口

全球與台灣同口徑總資產序列；#註記定義；FSC與銀行合併範圍 reconciliation；支付與金融科技核心期刊研究。

## 不可直接寫入講義的推論

不能由企業一年營收推算全球市場；不能混用商品、產業、企業與金控；不能由概念模型填入虛構樣本；不能將統計關聯改寫為因果效果。候選索引仍是待查來源，只有上述具定位的內容可作目前證據。

## 撰稿前檢查

逐項對照[衝突清單](conflicts.csv)及[充分性評估](sufficiency.csv)。每個引用保留版次與原文定位；工作稿頁碼和HTML定位不能偽裝為正式期刊PDF頁碼。
