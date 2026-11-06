# 第31堂｜銀行：研究證據包

研究用途，非正式教材，未通過四階段出版審查。查核日期：2026年11月6日。

以JPMorgan多前身歷史提示銀行組織演變，搭配JPM銀行與兆豐銀行本體財報、Diamond–Dybvig機制。

## 可追溯事實

- `I_O_BIS_CREDIT` BIS reporting banks worldwide：cross_border_credit_outstanding = 32600000000000 USD〔BIS cross-border bank credit；Key takeaways and Graph1〕
- `I_O_TW_BANK_ROWS` Taiwan domestic banks：reported_bank_entries = 38 entries〔金管會銀行局本國銀行主要業務；CSV filters 年=113 and 月-期底=12〕
- `I_O_FSC_MEGA` 兆豐國際商業銀行#：reported_total_assets = 4166596 TWD million〔金管會銀行局本國銀行主要業務；CSV key(113,12,兆豐國際商業銀行#) / 資產-總額-新臺幣百萬元〕
- `I_O_FSC_BOT` 臺灣銀行#：reported_total_assets = 6583680 TWD million〔金管會銀行局本國銀行主要業務；CSV key(113,12,臺灣銀行#) / 資產-總額-新臺幣百萬元〕
- `I_C_JPMBANK_net_interest_income` JPMorgan Chase Bank, National Association and subsidiaries：net_interest_income = 94620 USD million〔JPMorgan Chase Bank N.A. and subsidiaries；income printed3/PDF5; balance printed5/PDF7〕
- `I_C_JPMBANK_net_revenue` JPMorgan Chase Bank, National Association and subsidiaries：net_revenue = 161326 USD million〔JPMorgan Chase Bank N.A. and subsidiaries；income printed3/PDF5; balance printed5/PDF7〕
- `I_C_JPMBANK_net_income` JPMorgan Chase Bank, National Association and subsidiaries：net_income = 52502 USD million〔JPMorgan Chase Bank N.A. and subsidiaries；income printed3/PDF5; balance printed5/PDF7〕
- `I_C_JPMBANK_total_assets` JPMorgan Chase Bank, National Association and subsidiaries：total_assets = 3459261 USD million〔JPMorgan Chase Bank N.A. and subsidiaries；income printed3/PDF5; balance printed5/PDF7〕
- `I_C_JPMBANK_deposits` JPMorgan Chase Bank, National Association and subsidiaries：deposits = 2516998 USD million〔JPMorgan Chase Bank N.A. and subsidiaries；income printed3/PDF5; balance printed5/PDF7〕
- `I_C_MEGA_net_interest_income` Mega International Commercial Bank and subsidiaries：net_interest_income = 38283802 TWD thousand〔兆豐國際商業銀行及子公司；PDF12 balance / PDF13 income; annual PDF54–55 cross-check〕
- `I_C_MEGA_net_revenue` Mega International Commercial Bank and subsidiaries：net_revenue = 69731802 TWD thousand〔兆豐國際商業銀行及子公司；PDF12 balance / PDF13 income; annual PDF54–55 cross-check〕
- `I_C_MEGA_net_income` Mega International Commercial Bank and subsidiaries：net_income = 28369519 TWD thousand〔兆豐國際商業銀行及子公司；PDF12 balance / PDF13 income; annual PDF54–55 cross-check〕
- `I_C_MEGA_total_assets` Mega International Commercial Bank and subsidiaries：total_assets = 4192553310 TWD thousand〔兆豐國際商業銀行及子公司；PDF12 balance / PDF13 income; annual PDF54–55 cross-check〕
- `I_C_MEGA_deposits_and_remittances` Mega International Commercial Bank and subsidiaries：deposits_and_remittances = 3156535891 TWD thousand〔兆豐國際商業銀行及子公司；PDF12 balance / PDF13 income; annual PDF54–55 cross-check〕
- `I_B_JPMBANK_LOANS` JPMorgan Chase Bank N.A. group：loans_net = 1321348 USD million〔JPMorgan Chase Bank N.A. and subsidiaries；printed5/PDF7〕
- `I_B_MEGA_LOANS` Mega Bank group：discounts_and_loans_net = 2294640812 TWD thousand〔兆豐國際商業銀行及子公司；PDF12; auditor KAM PDF6〕
- `N_JPM_ORIGINS` JPMorganChase把其歷史追溯至1799年紐約水公司，現今組織整合眾多前身機構。〔Our history；Looking to the past investing in the future / founding paragraph〕

## 歷史與企業故事的證據界線

BIS跨境信用非全球銀行總資產；銀行本體、金控與監理列範圍不同。

年代事件見[時間線](../timelines.csv)，每項以claim_id回查[主張表](../claims.csv)。本課沒有事件列的時期仍是缺口，不以推測補齊。既有六家企業財報查核見[前批研究包](../../deep-2026-11-06/README.md)。

## 原文核讀與適用範圍

- Jay Barney (1991)，original journal scan; OCR。核讀：印刷 pp.101–103（定義）,105–112（條件）,113–117（例示及意涵）；PDF pp.3–5,7–14,15–19；PDF p.7已視覺核對。。限制：價值取決於環境；結構衝擊可使原資源失去價值；替代性需另行檢驗，非成功企業事後貼標籤。。來源`S_barney_1991`。
- Oliver E. Williamson (1979)，original journal with JSTOR cover。核讀：印刷 p.239（三維度）,pp.247–253（治理配適）,259–261（意涵）；PDF pp.8,16–22,28–30。。限制：須同時衡量生產經濟、交易成本及設計；資本市場應用改以可驗證性討論；不是任何大型企業都有效率的證據。。來源`S_williamson_1979`。
- Douglas W. Diamond; Philip H. Dybvig (1983)，original journal; institutional repository。核讀：印刷 pp.405–407（模型）,410–412（停止兌付）,414–415 Proposition 2（保險）,415–417（邊界）；PDF pp.5–7,10–12,14–17。。限制：保險結果依賴政府課稅能力等假設；未完整處理資產風險與道德風險，不表示現實保險永遠無成本或每次危機皆屬自我實現。。來源`S_diamond_1983`。

## 價值鏈、商業模式與競爭機制

存款及資本 → 授信與證券資產 → 支付／清算與費用；期限及風險管理跨越全鏈。這是研究者的概念化整理，不是經估計的市場流量。支撐入口：N_JPM_ORIGINS;I_C_JPMBANK_deposits;I_C_MEGA_deposits_and_remittances;I_O_BIS_CREDIT；未有逐環節直接證據的部分列為待驗證，不將示意圖冒充已觀察到的產業結構。

BIS跨境信用非全球銀行總資產；銀行本體、金控與監理列範圍不同。

## 待驗證主張與缺口

還缺中央銀行與存保制度歷史、銀行監理與資本風險、兆豐合併前後原始史料，以及全球銀行總量一致系列。

產業成長是否由特定企業、政策或技術造成，尚須比較研究或原始過程資料；年度報告的管理階層解釋不可直接當作因果識別。

## 圖像方案

自行繪製上述概念流程圖，明標「概念示意、非比例圖」，附claim IDs。數據圖只可取用已核對同口徑值，不複製PDF圖版。照片逐張授權尚未取得，不能使用公司網站圖片當作免授權素材。

[本課撰寫準備度](teaching_readiness_report.md)
