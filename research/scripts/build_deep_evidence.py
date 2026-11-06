"""建立八課的人工核讀成果。只整理已取得來源；不以入口數量判定充分性。"""
import csv, hashlib, json, re
from pathlib import Path
import acquire as a

E = a.R / 'evidence' / 'deep-2026-11-06'
LESSONS = ['00','01','02','03','04','05','18','31']

def write(name, rows):
    path = E / name; path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def pages(key, ocr=False):
    return json.loads((a.PRIVATE / ('deep_'+key+('_ocr_pages.json' if ocr else '_pages.json'))).read_text(encoding='utf-8'))

# 各欄為人工核讀的摘要，不從摘要頁推測樣本或結果。
PAPERS = [
dict(id='Xa03c07055',key='coase_university',authors='R. H. Coase',year='1937',title='The Nature of the Firm',journal='Economica',doi='10.1111/j.1468-0335.1937.tb00002.x',version='original journal scan; OCR',lessons='00;01;03;04',question='價格機制可以協調生產，為何仍有企業，其邊界如何決定？',mechanism='發現價格、逐筆協商及訂約有成本；企業家指揮可替代部分市場交易，但內部組織成本也隨規模增加。',sample='不適用：理論論文，無實證樣本。',period='不適用：沒有估計期間；1937為出版年。',variables='概念：市場交易成本、內部組織成本、企業家協調的交易數量；不是已估計迴歸變數。',method='邊際比較與概念推導。',results='企業擴張至內部多組織一筆交易的成本，與市場或其他企業組織該交易的成本相當；不是最大規模永遠最有效率。',limitations='交易異質性、空間與企業家差異使比較複雜；不是量化因果檢驗。',locator='印刷 pp.388–394,403；PDF pp.4–10,19（封面後起算）；OCR p.391已視覺核對。',status='original_pdf_core_sections_reviewed',gap='未提供產業集中度或市場規模的測量方法。'),
dict(id='P003',key='barney_1991',authors='Jay Barney',year='1991',title='Firm Resources and Sustained Competitive Advantage',journal='Journal of Management',doi='10.1177/014920639101700108',version='original journal scan; OCR',lessons='00;03;04;05;18;31',question='何種企業資源可能產生持續競爭優勢？',mechanism='資源異質性與不完全移動性，使有價值、稀少、難模仿且不存在可行策略等價替代的資源可能維持優勢；歷史條件、因果模糊及社會複雜性限制模仿。',sample='不適用：理論建構；策略規劃、資訊系統與聲譽為討論例子，非抽樣資料。',period='不適用：沒有實證觀察窗。',variables='概念性 VRIN；value/rareness/imperfect imitability/non-substitutability。原文並非 VRIO 操作量表。',method='在異質性與不完全移動假設下推導，再討論候選資源。',results='具備單一資源屬性不足以推出持續優勢；購買同樣設備通常不足。持續係競爭者無法複製利益，並非固定年數或永久。',limitations='價值取決於環境；結構衝擊可使原資源失去價值；替代性需另行檢驗，非成功企業事後貼標籤。',locator='印刷 pp.101–103（定義）,105–112（條件）,113–117（例示及意涵）；PDF pp.3–5,7–14,15–19；PDF p.7已視覺核對。',status='original_pdf_core_sections_reviewed',gap='未提供任何現代案例的 VRIN 實證證明。'),
dict(id='P004',key='williamson_1979',authors='Oliver E. Williamson',year='1979',title='Transaction-Cost Economics: The Governance of Contractual Relations',journal='Journal of Law and Economics',doi='10.1086/466942',version='original journal with JSTOR cover',lessons='01;03;04;05;31',question='交易屬性如何影響市場、雙邊及統一治理的配適？',mechanism='專用性投資形成雙邊依賴，在有限理性與機會主義下產生適應／議價風險；反覆交易可攤提專門治理成本。',sample='不適用：比較制度的理論分析；非公司面板或實驗。',period='不適用：出版年1979不是樣本年。',variables='交易不確定性、頻率、交易專用性投資；治理形式；皆為理論維度，非估計主效果。',method='契約法與交易成本的比較制度分析。',results='非專用交易可用市場；偶發且非標準交易可借重第三方；反覆且專用交易可能採雙邊或統一治理。不能由不確定性單獨推出內部化。',limitations='須同時衡量生產經濟、交易成本及設計；資本市場應用改以可驗證性討論；不是任何大型企業都有效率的證據。',locator='印刷 p.239（三維度）,pp.247–253（治理配適）,259–261（意涵）；PDF pp.8,16–22,28–30。',status='original_pdf_core_sections_reviewed',gap='需要情境特定的交易單位、專用性與治理成本資料。'),
dict(id='P007',key='henderson_1990',authors='Rebecca M. Henderson; Kim B. Clark',year='1990',title='Architectural Innovation: The Reconfiguration of Existing Product Technologies and the Failure of Established Firms',journal='Administrative Science Quarterly',doi='10.2307/2393549',version='original journal with JSTOR cover',lessons='03;04;18',question='為何看似小幅的技術改變也可能重挫既有企業？',mechanism='主導設計使架構知識內嵌在溝通管道、資訊過濾與解題慣例；元件仍熟悉但連結改變時，原有知識反而遮蔽新問題。',sample='光學微影對準設備產業所有產品開發專案之歷史資料；文章未在已核讀資料段報告精確專案總數。另訪談逾100人，不將人數視為獨立專案數。',period='產品專案1962–1986；訪談1987年3月至1988年5月；兩年田野研究。',variables='元件核心概念／連結的改變；研發成本、產品銷售、技術及管理歷史；Table 2為平減累積銷售占比，非當年市占。',method='歷史產業研究與半結構訪談，交叉核對內部及次級資料；無可直接移用的因果係數。',results='Kasper、Perkin-Elmer及GCA案例顯示，架構知識與組織管道可阻礙辨識及執行；不是只有資金不足或不願投入。',limitations='單一設備產業，其他因素也影響失去領導地位；Table 2各技術生命週期不完整，尤其第二代步進機；不能外推EUV或現代AI需求的因果效果。',locator='印刷 p.12 Figure 1；pp.19–20（資料）；p.24 Table 2；pp.25–28（案例及限制）；PDF pp.5,12–13,17–21。',status='original_pdf_core_sections_reviewed',gap='IC設計、記憶體及封測各自的原始研究仍待核讀。'),
dict(id='X69013d8a3',key='diamond_1983',authors='Douglas W. Diamond; Philip H. Dybvig',year='1983',title='Bank Runs, Deposit Insurance, and Liquidity',journal='Journal of Political Economy',doi='10.1086/261155',version='original journal; institutional repository',lessons='03;04;31',question='為何銀行能提供流動性保障，又同時可能遭遇擠兌？',mechanism='長期技術與私人流動性需求形成風險分攤空間；可隨時提領且先到先付的契約在特定預期下同時支持良性與擠兌均衡。',sample='不適用：三期理論模型，非銀行倒閉實證樣本。',period='不適用：t=0,1,2為模型時間，不是曆年。',variables='長期報酬R、早期需求比例t、消費c1/c2、承諾提領r1、提領比例f、政府稅；非迴歸係數。',method='最適風險分攤、納許均衡及契約比較。',results='在模型條件下存款契約提供流動性但可有壞均衡；停止兌付在需求比例隨機時有限制；以稅支應的存款保險可實現較佳配置。',limitations='保險結果依賴政府課稅能力等假設；未完整處理資產風險與道德風險，不表示現實保險永遠無成本或每次危機皆屬自我實現。',locator='印刷 pp.405–407（模型）,410–412（停止兌付）,414–415 Proposition 2（保險）,415–417（邊界）；PDF pp.5–7,10–12,14–17。',status='original_pdf_core_sections_reviewed',gap='支付、金融科技、監理資本及台灣信用風險實證仍缺。'),
dict(id='W_GVC_2003',key='gvc_author_manuscript',authors='Gary Gereffi; John Humphrey; Timothy Sturgeon',year='2003',title='The governance of global value chains',journal='Author manuscript, forthcoming RIPE',doi='',version='2003-11-04 author manuscript; NOT 2005 journal pagination',lessons='02;05;18',question='如何解釋企業間價值鏈治理的不同形式？',mechanism='交易資訊複雜度、可編碼性與供應商能力共同形成協調及權力不對稱的不同組合。',sample='概念建構搭配服飾、自行車、園藝及電子等案例；非四產業統一抽樣或因果估計。',period='不同歷史案例，無共同估計期間；稿本日期2003-11-04。',variables='三個高低維度與市場、模組、關係、俘虜、階層五種治理；不是以國家或產業為固定型別。',method='類型學與案例說明。',results='Table 1列出五種組合；低複雜、可編碼但能力不足導致排除，不是第六種治理。相同產業不同環節可有不同形式。',limitations='稿本並非最終期刊版；動態演變只獲部分解釋，不能把模組化視為不可逆必然趨勢。',locator='作者稿自身 pp.6–8（PDF pp.7–9；Table 1在PDF p.9）；作者稿 p.15（PDF p.16）動態限制。不得填2005版pp.78–104為已核對定位。',status='author_manuscript_reviewed_journal_version_pending',gap='P005正式版核心段落另已取得；完整逐字版本差異待核。'),
dict(id='D_PNAS_2020',key='pnas_contract',authors='Eva-Marie Meemken; Marc F. Bellemare',year='2020',title='Smallholder farmers and contract farming in developing countries',journal='PNAS',doi='10.1073/pnas.1909501116',version='original full HTML; issue117(1):259–264; online2019-12-13',lessons='04;05',question='契作是否普遍連結小農的較高所得、雇工與社區外溢？',mechanism='契作可改善市場與投入品取得，但也有選擇與參與障礙；所得及雇工關係須依地區檢驗。',sample='CGAP六國：Bangladesh、Côte d’Ivoire、Mozambique、Nigeria、Tanzania、Uganda；16140戶、27761人、1255叢集、661行政單位。所得分析14573戶，1567戶所得缺失。',period='2015–2016橫斷面調查；2020為卷期年，2019為線上先行年。',variables='至少一名家戶成員有銷售作物或畜產契約為參與戶；所得為現金家戶總所得的人均每日值取對數、2016USD，不含自給消費；雇工指extended period二元變數，不是雇工人數。',method='所得模型控制國家／行政／叢集位置固定效果；個人雇工模型另用家戶固定效果。橫斷面資料，不能稱所得模型為家戶FE面板或因果TWFE。',results='Table 2全國合併model 3：係數0.095、SE0.026、N14573，所得條件關聯約exp(.095)-1=9.97%；異質性明顯，社區外溢不穩健。',limitations='選擇偏誤仍可能存在；缺失所得、契約細節不足、僅六國小農；不能據此宣稱台灣契作使所得因果提高9.97%。',locator='HTML Results/Table 2、Discussion、Materials and Methods；已讀正式全文HTML，尚未取得有效PDF，精確印刷頁碼待核；259–264僅為書目頁範圍。',status='original_html_reviewed_pdf_pagination_pending',gap='PDF精確頁碼及台灣契作樣本仍待取得。'),
]

PAPERS.extend([
dict(id='P009',key='teece_1997_copy',authors='David J. Teece; Gary Pisano; Amy Shuen',year='1997',title='Dynamic Capabilities and Strategic Management',journal='Strategic Management Journal',doi='10.1002/(sici)1097-0266(199708)18:7<509::aid-smj882>3.0.co;2-z',version='original journal scan18(7):509–533; cover plus25pages; key pages visually read',lessons='00;01;02;03;04;18',question='在技術與市場快速變化下，企業如何形成、維持及更新難以模仿的競爭優勢？',mechanism='整合、建立與重組內外部competences；組織及管理processes受資產positions與累積paths塑造，學習與重組並受複製／模仿難度影響。',sample='不適用：理論框架比較及既有研究例示，沒有本文新建的企業樣本。',period='不適用：1997為出版年，歷史企業例子非共同觀察窗。',variables='Processes（協調／整合、學習、重組）、positions（特定資產）、paths（路徑依賴及機會）；非經估計的三變數模型。',method='比較competitive forces、strategic conflict、RBV及dynamic capabilities四種策略典範，推導組織層次框架。',results='資源存量本身不保證競爭優勢，企業須能協調及重新部署；歷史選擇限制可行路徑，重組耗時且有成本；可複製性與模仿性影響優勢耐久。',limitations='作者承認框架仍在發展，不能自信給出強規範結論；成功不能反向當作能力測量；不是把後來sensing/seizing/transforming架構倒填為本篇的三構面。',locator='印刷pp.515–516（定義）,518–524（processes/positions/paths及複製）,527 Table1（典範比較）,528–529（限制與策略意涵）；PDFpp.8–9,11–17,20–22；上述掃描頁已視覺閱讀。',status='original_pdf_core_sections_reviewed',gap='各示範企業能力形成與重組的過程資料尚缺；單年研發費不能直接操作化dynamic capabilities。'),
dict(id='P005',key='gvc_journal_2005',authors='Gary Gereffi; John Humphrey; Timothy Sturgeon',year='2005',title='The governance of global value chains',journal='Review of International Political Economy',doi='10.1080/09692290500049805',version='original journal12(1):78–104; FAO-hosted copy',lessons='02;05;18',question='為何跨國價值鏈呈現不同企業間治理形式？',mechanism='資訊複雜度、可編碼性與供應商能力共同決定協調需要與依賴；形成市場、模組、關係、俘虜與階層五種分析類型。',sample='概念類型學，搭配自行車、服飾、園藝與電子四個簡短歷史案例；非四產業統一抽樣，未提供可當作迴歸樣本的N。',period='不同歷史案例，沒有共同估計期間；2005為出版年。',variables='三項高／低維度；五種治理；協調程度與權力不對稱。高低為類型化假定，不是測量後的連續效果。',method='整合TCE、生產網絡與技術能力文獻，推導類型並以案例說明。',results='Table1 p.87核對五種組合；低複雜且可編碼但能力低導致排除，不另成治理類型。同產業不同環節及時點可以不同形式。',limitations='三變數如何動態演變僅部分解釋；標準會失效或競爭，關係不必單向走向模組化；上游參數設定者、消費者與地方制度亦重要。',locator='印刷pp.83–87（類型與Table1）,96–99（動態、結論及邊界）；PDFpp.6–10,19–22；頁碼=PDF+77。',status='original_pdf_core_sections_reviewed',gap='2003與2005核心Table1及動態邊界已交叉核對，尚未做全文逐字版本差異；當代台灣產業分工仍需直接資料。'),
dict(id='P014',key='ocasio_1997',authors='William Ocasio',year='1997',title='Towards an Attention-Based View of the Firm',journal='Strategic Management Journal',doi='10.1002/(sici)1097-0266(199707)18:1+<187::aid-smj936>3.0.co;2-k',version='original journal18(S1):187–206; university teaching copy',lessons='00;01;02;03;04',question='組織如何分配決策者注意力，進而影響企業行為與調適？',mechanism='選擇性焦點、情境化注意力與注意力結構分配三原則相連；規則、參與者、位置、資源透過程序與溝通管道，使特定議題及答案進入決策。',sample='不適用：理論過程模型；文中引述他人實驗、田野及企業例子，不當作作者原始估計樣本。',period='不適用：無統一實證期間；1997為卷期年。',variables='議題與答案、程序／溝通管道、規則、players、結構位置、資源、decision-makers、organizational moves；未估計係數。',method='整合認知、社會心理、組織與策略文獻的過程模型。',results='相同個人在不同情境可能注意不同議題；注意力既可幫助執行，也可能排除其他訊號。提出組織行動不等於完成執行。',limitations='不是完整可估計的企業行為理論；結構與認知如何交互作用仍需發展；不能由會議提到某議題就證明資源已重新配置。',locator='印刷p.188（三原則）,pp.189–192（原則與模型）,196–201（結構與管道）,202–203（調適、結論）；PDFpp.2–6,10–17；頁碼=PDF+186。',status='original_pdf_core_sections_reviewed',gap='各產業注意力管道的直接過程證據仍待建立。'),
])
# 工作稿保留為歷史版本；新取得正式版後，不繼續把正式版列為存取缺口。
next(p for p in PAPERS if p['id']=='W_GVC_2003').update(status='author_manuscript_reviewed_final_core_crosschecked',gap='P005正式2005版本已取得並核對核心段落；兩版仍各保留頁碼，全文逐字差異未完成。')

SOURCES = [
('teece_1997_copy','原始期刊掃描','Teece/Pisano/Shuen1997','1997 journal18(7):509–533; cover page offset','academic-hosted research copy; no redistribution assumed'),
('gvc_journal_2005','原始期刊／FAO保存副本','Gereffi et al.2005','2005 formal journal12(1):78–104','institution-hosted readable copy; no redistribution'),
('ocasio_1997','原始期刊','Ocasio1997','1997 original journal18(S1):187–206','university teaching copy; no redistribution'),
('mof_2024_release','官方初步貿易統計原表','財政部113年12月海關進出口統計','released2025-01-09; calendar2024 observations','official aggregate facts; preliminary snapshot'),
('coase_university','原始期刊','Coase 1937','1937 original scan','personal research; university teaching copy; no redistribution'),
('barney_1991','原始期刊','Barney 1991','1991 original scan','personal research; university teaching copy; no redistribution'),
('williamson_1979','原始期刊','Williamson 1979','1979 journal/JSTOR cover','personal noncommercial research; no redistribution'),
('henderson_1990','原始期刊','Henderson & Clark 1990','1990 journal/JSTOR cover','personal noncommercial research; no redistribution'),
('diamond_1983','原始期刊／機構典藏','Diamond & Dybvig 1983','1983 original','repository availability permission; no redistribution assumed'),
('gvc_author_manuscript','作者工作稿','Gereffi et al.','2003-11-04; NOT 2005 final','author-hosted; no redistribution assumed'),
('pnas_contract','原始期刊HTML','Meemken & Bellemare','2020 issue; 2019 online','PMC readable; copyright retained; no fulltext redistribution'),
('fao_production','官方統計發布','FAO agricultural production','2024 observations; 2025-12-31 release','official aggregate facts; raw kept private'),
('moa_2024','官方年報統計','農業部113年施政年報','2024; preliminary figures in narrative','official aggregate facts'),
('moa_scope','官方統計及定義','農業部名目生產總額','2024; dynamic page snapshot','official aggregate facts'),
('oecd_semiconductor_pdf','官方研究報告／UN Comtrade運算','OECD semiconductor value chain','2025 report; 2022 trade observations','OECD report; no PDF redistribution'),
('mof_ic_cbc','官方次級轉載','CBC引財政部IC出口','2024; rounded figures','official reproduced aggregate; primary MOF table still needed'),
('bis_2024','官方統計發布','BIS cross-border bank credit','end2024; 2025-04-30 release','official aggregate facts'),
('bank_csv','官方逐行統計CSV','金管會銀行局本國銀行主要業務','ROC113 December; downloaded snapshot','Taiwan Open Government Data License 1.0'),
('fsc_bank_data','官方資料集定義','政府資料開放平台28781','monthly; IFRS9 changes from2018','Taiwan Open Government Data License 1.0'),
('tyson_10k_2024','企業原始10-K','Tyson Foods Inc.','FY ended2024-09-28; USGAAP','issuer report; no PDF redistribution'),
('dachan_2024','企業原始年報','大成長城企業','2024 consolidated and separate tables','issuer report; no PDF redistribution'),
('dachan_audited_2024','企業完整查核財報','大成長城企業及子公司','2024 consolidated; Taiwan-endorsed IFRS','issuer report; no PDF redistribution'),
('intel_2024','企業原始10-K','Intel Corporation','FY ended2024-12-28; USGAAP','issuer report; no PDF redistribution'),
('jpm_bank_official','銀行本體原始財報','JPMorgan Chase Bank N.A. and subsidiaries','2024 consolidated; USGAAP; NOT holding company','issuer report; no PDF redistribution'),
('mega_2024','銀行本體原始年報','兆豐國際商業銀行','2024 consolidated/standalone columns separate','issuer report; no PDF redistribution'),
('mega_audited_2024','銀行本體完整查核財報','兆豐國際商業銀行及子公司','2024 consolidated; Taiwan reporting framework','issuer report; no PDF redistribution'),
('tsmc_20f_2024','企業原始20-F','TSMC and subsidiaries','2024 IFRS as issued by IASB; financial statement audit PDF92','issuer report; no PDF redistribution'),
]

def build():
    E.mkdir(parents=True,exist_ok=True)
    logs={r['resource_id']:r for r in a.read_csv('audit/download_log.csv') if r['status'] in ['downloaded','cached_download']}
    sources=[]
    for key,identity,title,version,rights in SOURCES:
        l=logs['deep_'+key];p=a.ROOT/l['local_path']
        sources.append(dict(source_id='S_'+key,identity=identity,title=title,version=version,url=l['url'],local_private_path=l['local_path'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,rights=rights,accessed_at='2026-11-06',status='content_located_not_blanket_teaching_ready'))
    # 舊台積電年報的兩個URL為同一出版物；異SHA不刪原件及下載紀錄。
    filings=a.read_csv('registries/company_filings.csv');old=[r for r in filings if r['filing_id']=='A_tsmc_2024']
    archive=E/'archived_duplicate_filings.csv'
    if old and not archive.exists():write('archived_duplicate_filings.csv',old)
    filings=[r for r in filings if r['filing_id']!='A_tsmc_2024']
    for r in filings:
        if r['filing_id']=='D_F047':
            r.update(reporting_currency='TWD thousand',status='annual_financial_tables_reviewed',notes='Canonical publication identity for both 2024 annual-report URLs; PDF64/printed124–125 consolidated revenue/cost/profit read. IASB20-F profit differs; do not merge profit observations. Audit report in distinct 20-F, not inferred for this annual table.')
    a.write_csv('registries/company_filings.csv',filings)
    matrix=a.read_csv('registries/industry_lesson_matrix.csv')
    for r in matrix:
        if r['reference_id']=='A_tsmc_2024':r['reference_id']='D_F047'
    unique={tuple(r[k] for k in ['lesson_id','reference_id','source_role']):r for r in matrix}
    a.write_csv('registries/industry_lesson_matrix.csv',list(unique.values()))
    write('source_aliases.csv',[dict(alias='A_tsmc_2024',canonical='D_F047',reason='same issuer/publication/year; cover and financial table PDF64 match; SHA variants retained in download log',action='remove redundant active index row; archive full old row; canonicalize matrix keys; retain raw files')])
    # 一手年報加進新 evidence 層；原本的入口索引仍保留其候選身份。
    old_tsmc=next(r for r in filings if r['filing_id']=='D_F047')
    l=next(r for r in a.read_csv('audit/download_log.csv') if r['resource_id']=='D_F047' and r['status'] in ['downloaded','cached_download'])
    p=a.ROOT/l['local_path'];sources.append(dict(source_id='S_tsmc_annual',identity='企業原始年報',title='TSMC 2024 annual report',version='Taiwan annual report; PDF64 financial table; not identical profit to IASB20-F',url=old_tsmc['source_url'],local_private_path=l['local_path'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,rights='issuer report; no PDF redistribution',accessed_at='2026-11-06',status='financial_tables_reviewed'))
    write('sources.csv',sources)
    reviews=[]
    for p in PAPERS:
        row={k:v for k,v in p.items() if k!='key'};row['source_id']='S_'+p['key'];reviews.append(row)
        folder=E/'papers';folder.mkdir(exist_ok=True)
        text=f'# {p["authors"]} ({p["year"]})\n\n{p["title"]} — {p["journal"]}\n\n'
        text+=f'身份：{p["version"]}。狀態：{p["status"]}。來源：[{p["key"]}]({next(s["url"] for s in sources if s["source_id"]==row["source_id"])})。\n\n'
        labels={'question':'研究問題','mechanism':'理論機制','sample':'樣本','period':'研究期間','variables':'主要變數與操作','method':'研究方法與識別','results':'主要結果與可用主張','limitations':'限制與不能支持的主張','locator':'原文定位','gap':'仍待取得'}
        for k,label in labels.items():text+=f'## {label}\n\n{p[k]}\n\n'
        text+='頁碼以文件自身為準；PDF頁為1起算。未以摘要或書目頁範圍補寫尚未核對的精確頁碼。全文留在private_sources，不隨筆記公開。\n'
        (folder/(p['id']+'.md')).write_text(text,encoding='utf-8')
    write('paper_reviews.csv',reviews)
    # 主文獻索引只提升實際讀到的版本。保留既有卡，在末尾加核讀卡連結。
    lit=a.read_csv('registries/literature_master.csv');ids={r['paper_id'] for r in lit}
    for p in PAPERS:
        if p['id'] not in ids:
            r={k:'' for k in lit[0]};r.update(paper_id=p['id'],authors=p['authors'],year=p['year'],title=p['title'],journal_or_publisher=p['journal'],publication_type='working-paper' if p['id']=='W_GVC_2003' else 'journal-article',peer_reviewed='false' if p['id']=='W_GVC_2003' else 'true',doi=p['doi'],landing_url='https://doi.org/'+p['doi'] if p['doi'] else '',lesson_ids=p['lessons'],bibliographic_verified='true');lit.append(r)
        r=next(r for r in lit if r['paper_id']==p['id']);r.update(access_status=p['status'],review_status=p['status'],fulltext_verified='true',oa_url=next(s['url'] for s in sources if s['source_id']=='S_'+p['key']),license='readable research copy; no redistribution permission assumed',notes='核讀摘要與原文定位：research/evidence/deep-2026-11-06/papers/'+p['id']+'.md；fulltext_verified只指本列版本可讀，不代表所有主張或教學完成。')
        r.update(title=p['title'],authors=p['authors'],year=p['year'])
        if p['id']=='P007':r['pages']='9-30'
        if p['id']=='D_PNAS_2020':r.update(volume='117',issue='1',pages='259-264',online_first_year='2019')
        card=a.R/'notes/theory_cards'/f'{p["id"]}.md'
        base=card.read_text(encoding='utf-8') if card.exists() else f'# {p["title"]}\n'
        marker='## 2026-11-06 原文核讀增補'
        if marker not in base:base+='\n'+marker+'\n\n既有文字為較早候選階段紀錄；本次版本、研究內容、定位與限制以[核讀研究卡](../../evidence/deep-2026-11-06/papers/'+p['id']+'.md)為準。\n'
        card.write_text(base,encoding='utf-8')
    a.write_csv('registries/literature_master.csv',lit)
    build_observations(sources)
    integrate_filings(sources)
    build_packs()

def integrate_filings(sources):
    """以文件URL為身份，將新案例年度文件接回主索引，既有入口仍屬候選。"""
    src={r['source_id']:r for r in sources}
    cases=list(csv.DictReader((E/'company_cases.csv').open(encoding='utf-8')))
    filings=a.read_csv('registries/company_filings.csv')
    matrix=a.read_csv('registries/industry_lesson_matrix.csv')
    for case in cases:
        url=src[case['source_id']]['url']
        matches=[r for r in filings if r['source_url']==url]
        if matches:r=matches[0]
        else:
            r={k:'' for k in filings[0]};r.update(filing_id='DEEP_'+case['case_id'],issuer=case['issuer'],source_url=url);filings.append(r)
        r.update(fiscal_year='2024',reporting_currency=case['unit'],audited='true' if case['case_id']!='TSMC' else '',geography='Taiwan' if case['case_id'] in ['DACHAN','TSMC','MEGA'] else 'Global',status='financial_tables_and_scope_reviewed',notes=case['locator']+'; '+case['scope']+'; original evidence/cases/'+case['case_id']+'.md; audit evidence see audit_opinions.csv (TSMC audit source is distinct IASB20-F).')
        lesson_ids=sorted(set(filter(None,r['lesson_ids'].split(';')))|{case['lesson_id'],'01','04'});r['lesson_ids']=';'.join(lesson_ids)
        for lesson in [case['lesson_id'],'01','04']:
            if not any(x['lesson_id']==lesson and x['reference_id']==r['filing_id'] and x['source_role']=='firm' for x in matrix):
                matrix.append(dict(lesson_id=lesson,reference_id=r['filing_id'],reference_type='filing',source_role='firm',confidence='source_scoped',verified_at='2026-11-06',status='specific_financial_tables_reviewed_not_whole_lesson'))
    a.write_csv('registries/company_filings.csv',filings)
    a.write_csv('registries/industry_lesson_matrix.csv',matrix)

def build_observations(sources):
    obs=[]
    def add(id,lesson,src,entity,metric,value,unit,period,scope,locator,caution,kind='official_statistic',precision='as_published',status='verified_with_stated_scope'):
        obs.append(dict(observation_id=id,lesson_ids=lesson,source_id='S_'+src,entity=entity,metric=metric,value=value,unit=unit,period=period,stock_flow='stock' if any(x in metric for x in ['assets','deposits','credit_outstanding','loans_net']) else 'flow',nominal_real='nominal' if 'USD' in unit or 'TWD' in unit else 'not_applicable',scope=scope,locator=locator,precision=precision,kind=kind,status=status,caution=caution))
    add('O_FAO_CEREALS','01;04;05','fao_production','World','cereal_production',3100000000,'tonnes','2024','all cereals; primary production','release Key findings: cereals reached3.1 billion tonnes','Rounded quantity, not USD market size; do not aggregate with meat/milk.',precision='rounded to0.1 billion tonnes')
    add('O_FAO_MEAT','05','fao_production','World','meat_production',374000000,'tonnes','2024','FAO world meat aggregate','release Key findings:374 million tonnes','Not livestock sales; different commodity coverage from Taiwan all-agriculture output.',precision='rounded million tonnes')
    add('O_TW_AG_NARROW','00;01;04;05','moa_2024','Taiwan','agricultural_product_value',582848000000,'TWD','2024','agricultural products incl crops/forestry/fisheries/livestock','二、國內農業發展情勢 first paragraph','Annual narrative includes preliminary components; not presumed latest revised yearbook; not agricultural GDP.')
    add('O_TW_AG_BROAD','00;01;04;05','moa_scope','Taiwan','gross_agricultural_output',709800000000,'TWD','2024','producer-price broad agriculture output incl services/byproducts/self-consumption and specified SNA items','113年農林漁牧業生產總額; 指標說明一、二','Broader than agricultural product value; not value added/GDP. Difference cannot be called measurement error.',precision='rounded 億元')
    add('O_GLOBAL_CHIPS','00;01;02;04;18','oecd_semiconductor_pdf','World','chips_exports_lower_bound',1300000000000,'USD','2022','OECD 16 HS2017 product basket; incl some passives/media','PDF29 / report29; Appendix D TableD.6 PDF58','Published as MORE THAN1.3trillion, not exact. Re-exports/cross-border double counting; not global sales.',precision='strict lower bound > value')
    add('O_TW_CHIPS_SHARE','02;18','oecd_semiconductor_pdf','Chinese Taipei','share_of_world_basket_exports',28.1,'percent','2022','same OECD16-HS basket; not pure8542','PDF30 Figure3.12','Not a foundry market share; do not combine with2024 IC amount.')
    add('O_TW_IC_EXPORT','01;02;04;18','mof_ic_cbc','Taiwan','IC_exports',165000000000,'USD','2024','MOF IC export series, reproduced by Central Bank','printed42 / PDF43','Official secondary reproduction; rounded1650億. Need direct MOF code table before precise cross-country comparison.',precision='rounded 億USD',status='verified_official_secondary')
    add('O_TW_IC_PRIMARY','01;02;04;18','mof_2024_release','Taiwan','IC_exports',165042,'USD million','2024','MOF export goods classification IC row; not OECD16-HS basket','printed3/PDF3 Table2; printed17/PDF17 Table4 first column113年','2025-01-09 preliminary publication, not latest revised2024 series. Taxonomy remains different from broad OECD basket.',precision='rounded USD million')
    add('O_BIS_CREDIT','01;04;31','bis_2024','BIS reporting banks worldwide','cross_border_credit_outstanding',32600000000000,'USD','2024-12-31','cross-border loans and debt securities in BIS LBS; not all bank assets','Key takeaways and Graph1','End-period stock; not bank revenue or global market size; quarter changes adjusted for FX/breaks.',precision='rounded0.1trillion')
    banks=list(csv.DictReader((a.PRIVATE/'deep_bank_csv.csv').open(encoding='utf-8-sig',newline='')))
    selected=[r for r in banks if r['年']=='113' and r['月-期底']=='12']
    write('taiwan_banks_2024_12.csv',selected)
    add('O_TW_BANK_ROWS','00;04;31','bank_csv','Taiwan domestic banks','reported_bank_entries',len(selected),'entries','2024-12-31','banking55 dataset28781; distinct reporting rows','CSV filters 年=113 and 月-期底=12','38 rows are reporting entries, not a bank holding-company count.')
    for issuer,id in [('兆豐國際商業銀行#','MEGA'),('臺灣銀行#','BOT')]:
        row=next(r for r in selected if r['銀行別']==issuer)
        add('O_FSC_'+id,'00;04;31','bank_csv',issuer,'reported_total_assets',row['資產-總額-新臺幣百萬元'],'TWD million','2024-12-31','regulatory bank row; # meaning not defined in retrieved metadata','CSV key(113,12,'+issuer+') / 資產-總額-新臺幣百萬元','Do not silently strip # or treat as audited group consolidation; Mega differs from company financial statement.')
    # 六企業以一份具體年度文件作案例，不把入口算案例。
    specs=[
    ('TYSON','05','tyson_10k_2024','Tyson Foods Inc.','2024-09-28','USD million','USGAAP consolidated; meat/prepared foods integrated group','printed44 / PDF45',[('sales',53309),('cost_of_sales',49682),('gross_profit',3627),('operating_income',1409),('net_income',822),('net_income_parent',800)],'Global firm, not global agriculture; FY not calendar year; segment eliminations required.'),
    ('DACHAN','05','dachan_audited_2024','Great Wall Enterprise Co. Ltd. / 大成長城企業1210','2024-12-31','TWD thousand','audited consolidated; Taiwan-endorsed IFRS; not parent-only','PDF8 / printed6; annual PDF144 cross-check',[('sales',102749063),('cost_of_sales',87948997),('gross_profit',14800066),('operating_income',5336706),('net_income',4416069),('net_income_parent',3529389)],'Feed/livestock/food group, not primary-farming market. Auditor opinion PDF4 read; annual figures agree.'),
    ('INTEL','18','intel_2024','Intel Corporation','2024-12-28','USD million','USGAAP consolidated','printed57 / PDF65',[('sales',53101),('cost_of_sales',35756),('gross_profit',17345),('operating_income',-11678),('net_income',-19233),('net_income_parent',-18756)],'Consolidated net loss differs from loss attributable to Intel. Foundry segment includes intersegment sales; do not add to consolidated revenue.'),
    ('TSMC','18','tsmc_annual','TSMC2330','2024-12-31','TWD thousand','Taiwan annual report consolidated performance','printed124–125 / PDF64',[('sales',2894307699),('cost_of_sales',1269954135),('gross_profit',1624353564),('operating_income',1322053050),('net_income',1172431759),('net_income_parent',1173267703)],'Annual-report profit differs from IASB20-F. Keep separate accounting/version scope; do not merge profit figures.'),
    ('JPMBANK','31','jpm_bank_official','JPMorgan Chase Bank, National Association and subsidiaries','2024-12-31','USD million','bank consolidated USGAAP; not JPMorgan Chase & Co. holding group','income printed3/PDF5; balance printed5/PDF7',[('net_interest_income',94620),('net_revenue',161326),('net_income',52502),('total_assets',3459261),('deposits',2516998)],'Net revenue already deducts interest expense; compare to Mega net revenue only after GAAP/scope review, not gross interest income.'),
    ('MEGA','31','mega_audited_2024','Mega International Commercial Bank and subsidiaries','2024-12-31','TWD thousand','bank consolidated; Taiwan reporting framework; not MegaFHC','PDF12 balance / PDF13 income; annual PDF54–55 cross-check',[('net_interest_income',38283802),('net_revenue',69731802),('net_income',28369519),('total_assets',4192553310),('deposits_and_remittances',3156535891)],'Different from FSC bank row4166596 million. Deposits/remittances label retained; audit text scanned, audit OCR separately documented.'),
    ]
    cases=[]
    for tag,lesson,src,issuer,end,unit,scope,loc,figures,caution in specs:
        for metric,value in figures:add('C_'+tag+'_'+metric,lesson+';01;04',src,issuer,metric,value,unit,'FY ended '+end if metric not in ['total_assets','deposits','deposits_and_remittances'] else end,scope,loc,caution,kind='company_financial')
        rows=[r for r in obs if r['observation_id'].startswith('C_'+tag+'_')]
        (E/'cases').mkdir(exist_ok=True)
        body=f'# {issuer}｜第{lesson}堂\n\n身份與範圍：{scope}。期間截至{end}；單位{unit}。\n\n來源：[{src}]({next(s["url"] for s in sources if s["source_id"]=="S_"+src)})；{loc}。\n\n|指標|數值|\n|---|---:|\n'+''.join(f'|{r["metric"]}|{int(r["value"]):,}|\n' for r in rows)
        body+='\n## 可用與不可用\n\n可用於說明企業收入、成本或資產負債的會計結構。'+caution+'\n\n這些是企業披露的描述資料，不能證明TCE、RBV或創新機制的因果效果，也不能以集團營收充當產業市場規模。\n\n## 延伸核對\n\n尚需分部外部收入、實體產能／產銷量與多年趨勢，才能完成競爭位置分析；本卡不宣稱已覆蓋全部營運資料。\n'
        (E/'cases'/f'{tag}.md').write_text(body,encoding='utf-8')
        cases.append(dict(case_id=tag,lesson_id=lesson,issuer=issuer,source_id='S_'+src,period_end=end,unit=unit,scope=scope,locator=loc,financial_observations=len(rows),status='financial_tables_reviewed_operating_detail_incomplete',remaining='segment volumes/capacity and multi-year trends; see conflicts.csv for scope differences'))
    add('O_TSMC_IASB_PROFIT','04;18','tsmc_20f_2024','TSMC and subsidiaries','net_income',1157523.9,'TWD million','FY ended2024-12-31','IFRS Accounting Standards as issued by IASB','PDF96 / F-6','Different from Taiwan annual report1172431759 thousand; do not treat as OCR error or same-basis restatement.',kind='company_financial')
    add('O_TSMC_IASB_SALES','04;18','tsmc_20f_2024','TSMC and subsidiaries','sales',2894307.7,'TWD million','FY ended2024-12-31','IFRS as issued by IASB','PDF96 / F-6','Sales matches Taiwan annual report after unit conversion/rounding; profit does not.',kind='company_financial',precision='rounded0.1million')
    extra=[
    ('B_TYSON_CHICKEN','05','tyson_10k_2024','Tyson Foods','chicken_segment_sales',16425,'USD million','FY ended2024-09-28','segment reported sales; intersegment eliminations not allocated here','printed28/PDF29; Note17 printed78/PDF79','Do not sum segments without elimination.'),
    ('B_DACHAN_FEED','05','dachan_audited_2024','Great Wall Enterprise group','feed_product_revenue',53300579,'TWD thousand','2024','product-line revenue; group consolidated','PDF67/printed64 Note6(26)','Product-line feed revenue is not only Taiwan parent feed sales.'),
    ('B_DACHAN_TONNES','05','dachan_2024','Great Wall Enterprise Company','company_feed_sales_volume',1370000,'tonnes','2024','company feed sales narrative; do not assume full consolidated group physical volume','PDF127/printed122 Feed products','Rounded1.37m; company statement. PDF146 2.8m tonnes is2025 FORECAST, not2024 actual.'),
    ('B_INTEL_RD','18','intel_2024','Intel group','research_development_expense',16546,'USD million','FY ended2024-12-28','consolidated USGAAP expense','printed57/PDF65','Spending is not proof of innovation productivity or VRIN.'),
    ('B_TSMC_CUSTOMERA','18','tsmc_annual','TSMC group','largest_reported_customer_revenue_share',22,'percent','2024','anonymous customerA; annual consolidated net revenue share','PDF57 customer table','Do not identify customer by speculation; customerB12%; not foundry global market share.'),
    ('B_JPMBANK_LOANS','31','jpm_bank_official','JPMorgan Chase Bank N.A. group','loans_net',1321348,'USD million','2024-12-31','bank consolidated loans after allowance','printed5/PDF7','Not holding-company loans or gross loan face amount.'),
    ('B_MEGA_LOANS','31','mega_audited_2024','Mega Bank group','discounts_and_loans_net',2294640812,'TWD thousand','2024-12-31','bank consolidated after allowance','PDF12; auditor KAM PDF6','Discounts and loans retain original label; not all identical USGAAP loan definitions.'),
    ]
    for values in extra:add(*values,kind='company_operating_or_segment')
    for case in cases:
        subset=[r for r in obs if r['observation_id'].startswith('B_'+case['case_id']+'_')]
        card=E/'cases'/f'{case["case_id"]}.md'
        with card.open('a',encoding='utf-8') as f:
            f.write('\n## 已核對分部或營運指標\n\n')
            for r in subset:f.write(f'- {r["metric"]}：{r["value"]} {r["unit"]}（{r["period"]}；{r["locator"]}）。{r["caution"]}\n')
    audit=[
    dict(case_id='TYSON',source_id='S_tyson_10k_2024',locator='PDF86/printed85',opinion='present fairly; USGAAP',status='opinion_text_read'),
    dict(case_id='DACHAN',source_id='S_dachan_audited_2024',locator='PDF4',opinion='present fairly; Taiwan-endorsed IFRS and securities issuer regulations',status='opinion_text_read'),
    dict(case_id='INTEL',source_id='S_intel_2024',locator='PDF62/printed54; PDF64 cross-reference',opinion='unqualified financial statement opinion; USGAAP',status='opinion_text_read'),
    dict(case_id='TSMC',source_id='S_tsmc_20f_2024',locator='PDF92/F-2',opinion='present fairly; IFRS as issued by IASB; not annual Taiwan profit basis',status='opinion_text_read'),
    dict(case_id='JPMBANK',source_id='S_jpm_bank_official',locator='PDF3/printed1; dated2025-02-14 PDF4',opinion='present fairly; USGAAP; bank subsidiaries',status='opinion_text_read'),
    dict(case_id='MEGA',source_id='S_mega_audited_2024',locator='PDF5,11; OCR scan',opinion='present fairly; Taiwan-endorsed IFRS and public bank financial regulations; dated2025-02-24',status='opinion_OCR_read'),
    ]
    write('audit_opinions.csv',audit)
    write('observations.csv',obs);write('company_cases.csv',cases)

def build_packs():
    mapping={
    '00':('產業分類與企業邊界',['Xa03c07055','P003','P009','P014'],['O_TW_AG_NARROW','O_TW_AG_BROAD','O_TW_BANK_ROWS'],[], '既有TW11/NAICS2022/ISIC4與5版本區別，加上企業邊界與統計單位。分類碼只是觀察單位，不是策略相關市場。','證交所上市公司分類與生產活動分類的逐碼例證；TW12與課程TW11對照。','限定範圍可寫初稿'),
    '01':('收入、成本、附加價值與市場規模',['Xa03c07055','P004','P009','P014'],['O_TW_AG_NARROW','O_TW_AG_BROAD','O_GLOBAL_CHIPS','O_BIS_CREDIT'],['TYSON','DACHAN','INTEL','TSMC','JPMBANK','MEGA'],'由六企業對比營收、成本、淨利、淨收入及資產，辨識flow/stock；再用農業兩種產值說明口徑。','國民帳附加價值的實際產出－中間投入同表數值尚缺；各業完整成本／定價模型不足。','限定範圍可寫初稿'),
    '02':('全球分工與價值鏈',['P005','P009','P014'],['O_GLOBAL_CHIPS','O_TW_CHIPS_SHARE','O_TW_IC_PRIMARY'],['INTEL','TSMC'],'三個治理條件與五種類型；OECD商品籃子及重複跨境計數作統計練習。','TiVA增加值貿易與FDI實際序列仍缺；2022及2024不同比例不可混用。','核心文獻已核讀；關鍵序列待補'),
    '03':('競爭、資源與治理',['P003','P004','Xa03c07055','P007','X69013d8a3','P014','P009'],['O_TW_CHIPS_SHARE'],['INTEL','TSMC'],'對照RBV資源條件、TCE交易配適、架構創新、注意力管道與銀行流動性模型，說明不同理論的分析單位。','IO/SCP、Porter、網絡效果與定價的原始研究尚未逐篇核讀；貿易HHI不是企業市場集中度。','部分理論可寫；全課不足'),
    '04':('研究方法與證據核對', ['P004','P007','P009','P014','D_PNAS_2020','X69013d8a3'],['O_TW_AG_NARROW','O_TW_AG_BROAD','O_FSC_MEGA','O_TSMC_IASB_PROFIT'],['TSMC','JPMBANK','MEGA'],'用原文理論／實證區分、家戶所得關聯與銀行模型、財報版本衝突做可重現核對示範。','PNAS PDF精確印刷頁碼未得；跨分類映射衝突未消除；不得把檢查程式通過視為研究識別有效。','限定範圍可寫初稿'),
    '05':('農業、畜牧與原料',['P004','D_PNAS_2020','P005','P003'],['O_FAO_CEREALS','O_FAO_MEAT','O_TW_AG_NARROW','O_TW_AG_BROAD'],['TYSON','DACHAN'],'區分生產實物量、產品價值、廣義產出與加工集團營收；契作論文提供六國小農條件關聯，企業作會計例子。','台灣契作原始研究；農業年報初估值與2025-09修訂年鑑逐項校準；企業產能／產量；PNAS精確頁碼。','已有雙邊統計及案例；深度仍待補'),
    '18':('IC設計、代工、記憶體與封測',['P007','P003','P005','P009'],['O_GLOBAL_CHIPS','O_TW_CHIPS_SHARE','O_TW_IC_PRIMARY'],['INTEL','TSMC'],'原始微影設備研究說明架構知識；Intel與TSMC提供不同企業邊界的財報例子，貿易資料另列商品範圍。','官方IC純商品全球總額與台灣同年同HS表；IC設計／記憶體／封測分項及原始研究；TSMC兩套會計淨利差異明細待核。','部分環節充分；四環節全課不足'),
    '31':('銀行、存放款與信用',['X69013d8a3','P004'],['O_BIS_CREDIT','O_TW_BANK_ROWS','O_FSC_MEGA','O_FSC_BOT'],['JPMBANK','MEGA'],'銀行原始流動性模型，加上全球跨境信用與台灣逐行資產；兩家銀行本體財報對照，金控資料不代替銀行。','全球與台灣同口徑總資產序列；#註記定義；FSC與銀行合併範圍 reconciliation；支付與金融科技核心期刊研究。','存放款基礎可寫；全課不足'),
    }
    observations=list(csv.DictReader((E/'observations.csv').open(encoding='utf-8')))
    suff=[];claims=[];gaps=[]
    for lesson,(title,papers,oids,cases,outline,gap,rating) in mapping.items():
        content=f'# 第{lesson}堂 Evidence Pack｜{title}\n\n核對批次2026-11-06。評估：**{rating}**。本包支援限定主題撰稿，未標記整課完成或teaching-ready。\n\n## 講義論證順序\n\n{outline}\n\n## 已核對原文與適用邊界\n\n'
        for pid in papers:
            p=next(p for p in PAPERS if p['id']==pid)
            content+=f'- [{p["authors"]}（{p["year"]}）](papers/{pid}.md)：{p["mechanism"]} 定位：{p["locator"]} 邊界：{p["limitations"]}\n'
        content+='\n## 已核對統計或財報觀察\n\n|ID|觀察|數值與單位|期間|定位與口徑限制|\n|---|---|---|---|---|\n'
        for oid in oids:
            o=next(o for o in observations if o['observation_id']==oid)
            content+=f'|{oid}|{o["entity"]} {o["metric"]}|{o["value"]} {o["unit"]}|{o["period"]}|{o["locator"]}；{o["precision"]}；{o["caution"]}|\n'
        content+='\n完整來源URL、身份及SHA見[sources.csv](sources.csv)；觀察值及定義見[observations.csv](observations.csv)。\n\n## 企業案例\n\n'
        content+='\n'.join(f'- [{cid}](cases/{cid}.md)：已讀年度財務表，尚不代表完整產業個案或機制識別。' for cid in cases) if cases else '本課不把公司入口計作已完成個案；參考後續三產業的六張案例卡。'
        content+=f'\n\n## 尚待驗證主張與資料缺口\n\n{gap}\n\n## 不可直接寫入講義的推論\n\n不能由企業一年營收推算全球市場；不能混用商品、產業、企業與金控；不能由概念模型填入虛構樣本；不能將統計關聯改寫為因果效果。候選索引仍是待查來源，只有上述具定位的內容可作目前證據。\n\n## 撰稿前檢查\n\n逐項對照[衝突清單](conflicts.csv)及[充分性評估](sufficiency.csv)。每個引用保留版次與原文定位；工作稿頁碼和HTML定位不能偽裝為正式期刊PDF頁碼。\n'
        (E/f'lesson-{lesson}.md').write_text(content,encoding='utf-8')
        legacy=a.R/f'notes/lessons/lesson-{lesson}/index.md';text=legacy.read_text(encoding='utf-8');mark='## 八課深度驗證增補（2026-11-06）'
        if mark not in text:text+='\n'+mark+f'\n\n前文保留為初期候選來源紀錄；本次可用證據、頁碼及未補缺口見[Evidence Pack](../../../evidence/deep-2026-11-06/lesson-{lesson}.md)。評估：{rating}；並非整課完成。\n'
        legacy.write_text(text,encoding='utf-8')
        suff.append(dict(lesson_id=lesson,reviewed_original_journal_pdfs=sum(next(p for p in PAPERS if p['id']==pid)['status']=='original_pdf_core_sections_reviewed' for pid in papers),reviewed_original_html=sum(pid=='D_PNAS_2020' for pid in papers),reviewed_manuscripts=sum(pid=='W_GVC_2003' for pid in papers),selected_observations=len(oids),company_cases=len(cases),assessment=rating,whole_lesson_sufficient='false',gap=gap))
        gaps.append(dict(gap_id='G_'+lesson,lesson_id=lesson,missing=gap,impact='Blocks claim of complete lesson; limited verified sections may be drafted',status='open'))
        for pid in papers:
            p=next(p for p in PAPERS if p['id']==pid);claims.append(dict(claim_id=f'L{lesson}_{pid}',lesson_id=lesson,status='verified_with_scope' if p['status']=='original_pdf_core_sections_reviewed' else 'verified_limited_version_or_locator',claim=p['mechanism'],source_id='S_'+p['key'],locator=p['locator'],unsupported=p['limitations']))
        claims.append(dict(claim_id='L'+lesson+'_pending',lesson_id=lesson,status='pending',claim=gap,source_id='',locator='',unsupported='尚無足夠定位，不可當作已驗證內容'))
    write('sufficiency.csv',suff);write('gaps.csv',gaps);write('claims.csv',claims)
    conflicts=[
    ('K01','00;04','TW11 / TW12 / ISIC source versions','既有TW11是歷史分類；2026TW12不可靜默替換；658筆TW/ISIC版次衝突仍隔離。','retain historical versions; no verified crosswalk inferred'),
    ('K02','02;05;18','GVC2003 vs2005','作者稿與正式版各自核對核心段落及Table1；正式版頁87，稿本自身頁8。','both acquired; distinct page locators; no full-text identity or verbatim diff claimed'),
    ('K03','01;04;05','MOA582848m vs709800m TWD','產品產值與含服務／副產品等的廣義總產出不同；年報部分初估。','scope conflict explained; revised yearbook reconciliation open'),
    ('K04','01;02;18','OECD broad16-HS vs Taiwan IC','2022全球廣籃子與2024IC不同年不同範圍；進出口可重複跨境。','no direct denominator/share calculation'),
    ('K05','04;31','FSC Mega4166596m vs consolidated4192553.310m TWD','銀行監理列與銀行子公司合併財報有不同範圍；#定義未取得。','both retained; exact bridge unresolved'),
    ('K06','31','JPMorgan bank vs holding company','本包使用JPMorgan Chase Bank N.A.；JPMorgan Chase & Co.母集團177556m收入不取代銀行161326m。','identities separated; no double-count company case'),
    ('K07','05','Tyson FY vs Dachan calendar2024','Tyson年度截至2024-09-28，大成截至12-31，幣別及集團業務範圍不同。','no unqualified same-year revenue ranking'),
    ('K08','04;18','Intel consolidated net loss vs attributable','-19233m與-18756m USD為不同損益歸屬。','separate metrics'),
    ('K09','04;18','TSMC Taiwan annual vs IASB20-F','年報淨利1172431759千TWD；IASB20-F1157523.9百萬TWD，營收近乎一致。','different accounting/version basis; exact profit bridge not yet verified; no overwrite'),
    ('K10','04;05','PNAS online2019 vs issue2020; HTML vs PDF','正式卷期2020；原文HTML已讀，PDF精確頁碼未取得。','retain publication/online years and locator gap'),
    ('K11','01;31','BIS cross-border credit vs total bank assets','信用為貸款加債券；跨境存量不是全球銀行總資產或產業收入。','do not compute Taiwan/global asset share'),
    ]
    write('conflicts.csv',[dict(conflict_id=i,lesson_ids=l,identities=s,issue=t,handling=h) for i,l,s,t,h in conflicts])
    report='# 八課深度驗證交付\n\n本批只處理00–05、18、31中的指定八課（00–04共五課，加三產業），沒有擴張產業。原始候選索引保留，不計為已完成知識庫。\n\n'
    report+=f'核讀：8篇正式期刊PDF核心段落、1篇正式HTML全文（精確PDF頁碼待補）、1份2003作者稿（2005正式版已另取得）；不是10份閱讀紀錄全部正式PDF已完成。6家企業有具數值及定位的年度財務卡；營運分部與多年資料仍有缺口。\n\n'
    report+='|堂號|充分性|剩餘核心缺口|\n|---|---|---|\n'+''.join(f'|[{r["lesson_id"]}](lesson-{r["lesson_id"]}.md)|{r["assessment"]}|{r["gap"]}|\n' for r in suff)
    report+='\n## 判定規則\n\n限定初稿＝已有可定位來源支援明確子題，不代表全課充分。全課充分須所有標題核心議題具原文證據、必要統計同口徑、案例及衝突已解；本批八課皆未達此門檻。結構通過、來源HTTP成功與候選覆蓋率不取代內容門檻。\n\n## 可公開與本機資料\n\nCSV與原創研究卡公開；PDF、原始HTML、OCR全文與銀行原CSV在忽略的private_sources。公開只摘錄必要事實，不上傳全文或校園授權檔案；也不將大學課程網站可讀性誤認為開放重散布授權。\n\n## 保留及去重\n\n公司索引刪除1筆TSMC同年度出版物的重複入口，完整舊列存archived_duplicate_filings.csv；矩陣合併重複引用鍵，原下載及SHA均保留。其他來源主鍵及DOI重複由驗證程序檢查，沒有以同標題把工作稿與正式版混為一筆。\n\n## 重現\n\n`python research/scripts/build_deep_evidence.py`整理人工核讀成果；不重抓網路。`python research/scripts/validate_deep_evidence.py`核對原始快取及內容約束；`python research/scripts/validate.py`執行既有結構與保全檢查並更新manifest。新下載以deep_acquire.get記錄URL與SHA。OCR另需pymupdf、rapidocr_onnxruntime及numpy。不要重跑finalize覆寫本批人工內容。\n'
    (E/'README.md').write_text(report,encoding='utf-8')

if __name__=='__main__':build()
