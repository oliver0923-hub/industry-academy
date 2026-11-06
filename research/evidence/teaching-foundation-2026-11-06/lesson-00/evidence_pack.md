# 第00堂｜產業邊界與分類：研究證據包

研究用途，非正式教材，未通過四階段出版審查。查核日期：2026年11月6日。

以台積電專業代工及銀行法律實體展示企業、場所與產品市場的差別。

## 可追溯事實

- `I_O_TW_AG_NARROW` Taiwan：agricultural_product_value = 582848000000 TWD〔農業部113年施政年報；二、國內農業發展情勢 first paragraph〕
- `I_O_TW_AG_BROAD` Taiwan：gross_agricultural_output = 709800000000 TWD〔農業部名目生產總額；113年農林漁牧業生產總額; 指標說明一、二〕
- `I_O_GLOBAL_CHIPS` World：chips_exports_lower_bound = 1300000000000 USD〔OECD semiconductor value chain；PDF29 / report29; Appendix D TableD.6 PDF58〕
- `I_O_TW_BANK_ROWS` Taiwan domestic banks：reported_bank_entries = 38 entries〔金管會銀行局本國銀行主要業務；CSV filters 年=113 and 月-期底=12〕
- `I_O_FSC_MEGA` 兆豐國際商業銀行#：reported_total_assets = 4166596 TWD million〔金管會銀行局本國銀行主要業務；CSV key(113,12,兆豐國際商業銀行#) / 資產-總額-新臺幣百萬元〕
- `I_O_FSC_BOT` 臺灣銀行#：reported_total_assets = 6583680 TWD million〔金管會銀行局本國銀行主要業務；CSV key(113,12,臺灣銀行#) / 資產-總額-新臺幣百萬元〕
- `N_TW12_DATE` 第12次行業統計分類於2026年1月1日生效；舊統計不能事後當作新制編製。〔行業統計分類第12次修正；PDF4 公告〕
- `N_CLASS_UNIT` 行業分類須區分場所單位與企業單位。〔行業統計分類第12次修正；PDF8 統計單位〕
- `N_RETAIL_MARGIN` 判斷批零業主要經濟活動時，毛利額可作為附加價值的替代判準。〔行業統計分類第12次修正；PDF9 主要經濟活動〕
- `N_TSMC_1987` 台積電1987年在新竹成立，以專業積體電路製造服務為定位。〔1998 annual report introduction；Company Profile opening paragraph〕
- `N_TSMC_BOUNDARY` 台積電1998年年報稱章程禁止設計製造自有品牌IC，以成為客戶合作夥伴為定位。〔1998 annual report introduction；Company Profile / corporate charter paragraph〕

## 歷史與企業故事的證據界線

Coase與TW12支持邊界，不能把TCE當分類規則。

年代事件見[時間線](../timelines.csv)，每項以claim_id回查[主張表](../claims.csv)。本課沒有事件列的時期仍是缺口，不以推測補齊。既有六家企業財報查核見[前批研究包](../../deep-2026-11-06/README.md)。

## 原文核讀與適用範圍

- R. H. Coase (1937)，original journal scan; OCR。核讀：印刷 pp.388–394,403；PDF pp.4–10,19（封面後起算）；OCR p.391已視覺核對。。限制：交易異質性、空間與企業家差異使比較複雜；不是量化因果檢驗。。來源`S_coase_university`。
- Jay Barney (1991)，original journal scan; OCR。核讀：印刷 pp.101–103（定義）,105–112（條件）,113–117（例示及意涵）；PDF pp.3–5,7–14,15–19；PDF p.7已視覺核對。。限制：價值取決於環境；結構衝擊可使原資源失去價值；替代性需另行檢驗，非成功企業事後貼標籤。。來源`S_barney_1991`。
- David J. Teece; Gary Pisano; Amy Shuen (1997)，original journal scan18(7):509–533; cover plus25pages; key pages visually read。核讀：印刷pp.515–516（定義）,518–524（processes/positions/paths及複製）,527 Table1（典範比較）,528–529（限制與策略意涵）；PDFpp.8–9,11–17,20–22；上述掃描頁已視覺閱讀。。限制：作者承認框架仍在發展，不能自信給出強規範結論；成功不能反向當作能力測量；不是把後來sensing/seizing/transforming架構倒填為本篇的三構面。。來源`S_teece_1997_copy`。
- William Ocasio (1997)，original journal18(S1):187–206; university teaching copy。核讀：印刷p.188（三原則）,pp.189–192（原則與模型）,196–201（結構與管道）,202–203（調適、結論）；PDFpp.2–6,10–17；頁碼=PDF+186。。限制：不是完整可估計的企業行為理論；結構與認知如何交互作用仍需發展；不能由會議提到某議題就證明資源已重新配置。。來源`S_ocasio_1997`。

## 價值鏈、商業模式與競爭機制

場所單位 → 主要經濟活動 → 分類碼 → 統計範圍；企業另有多業與跨國邊界。這是研究者的概念化整理，不是經估計的市場流量。支撐入口：N_CLASS_UNIT;N_TSMC_BOUNDARY；未有逐環節直接證據的部分列為待驗證，不將示意圖冒充已觀察到的產業結構。

Coase與TW12支持邊界，不能把TCE當分類規則。

## 待驗證主張與缺口

還缺分類制度完整國際沿革、產品市場與行業差異的對照案例、一般讀者術語表證據。

產業成長是否由特定企業、政策或技術造成，尚須比較研究或原始過程資料；年度報告的管理階層解釋不可直接當作因果識別。

## 圖像方案

自行繪製上述概念流程圖，明標「概念示意、非比例圖」，附claim IDs。數據圖只可取用已核對同口徑值，不複製PDF圖版。照片逐張授權尚未取得，不能使用公司網站圖片當作免授權素材。

[本課撰寫準備度](teaching_readiness_report.md)
