"""建立研究包；不下載、不覆寫人工原文、不中斷既有研究狀態。"""
from pathlib import Path
import csv, json, hashlib

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'research/evidence/teaching-foundation-2026-11-06'
OLD = ROOT / 'research/evidence/deep-2026-11-06'
LESSONS = ['00','01','05','18','25','30','31']
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def write(name, rows):
    p=OUT/name; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
def md(name,text):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    sources={}
    for r in read(OLD/'sources.csv'):
        sources[r['source_id']]=dict(source_id=r['source_id'],title=r['title'],url=r['url'],publication_year='See version',version=r['version'],identity=r['identity'],local_private_path=r['local_private_path'],sha256=r['sha256'],rights=r['rights'],status='fulltext_downloaded',read_scope='Only inherited audited observations/cards below; no new whole-document reading asserted',acquisition='prior_batch')
    tasks={r['task_id']:r for r in read(ROOT/'research/sources/acquisition_tasks.csv')}
    for r in read(ROOT/'research/sources/acquisition_state.csv'):
        if r['task_id'].startswith('T_') or r['task_id']=='V2_TW12_MANUAL':
            t=tasks[r['task_id']]
            ok=r['status'] in ('downloaded','reused_existing')
            sources[r['source_id']]=dict(source_id=r['source_id'],title=t['title'],url=t['url'],publication_year=t['publication_date'][:4],version=t['data_period'],identity=t['issuer']+'; '+t['source_role'],local_private_path=r['local_path'] if ok else '',sha256=r['sha256'] if ok else '',rights=t['license'],status='fulltext_downloaded' if ok else 'bibliography_only',read_scope='Downloaded or identified; not automatically read',acquisition='this_batch')
    # 既有 Walmart 原件，按 SHA 回查，不再次下載。
    p=ROOT/'private_sources/D_F023.pdf'
    sources['D_F023']=dict(source_id='D_F023',title='Walmart Annual Report 2024',url='https://stock.walmart.com/_assets/_8c8425b76a1d46bbbbc16466da2a6b9c/walmart/db/950/9651/annual_report/Walmart+2024+Annual+Report.pdf',publication_year='2024',version='FY ended 2024-01-31',identity='issuer annual report; US GAAP consolidated',local_private_path='private_sources/D_F023.pdf',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rights='Public access; private original only; no image reuse granted',status='fulltext_read',read_scope='PDF43 / printed41 Results of Operations only',acquisition='reused_this_batch')
    claims=[]
    def add(cid,lesson,sid,claim,year,period,loc,support,caution='',category='industry_history',origin='new_original_read',status='claim_verified'):
        s=sources[sid]
        claims.append(dict(claim_id=cid,lesson_ids=lesson,category=category,claim=claim,source_id=sid,source_name=s['title'],original_url=s['url'],publication_year=year,data_year=period,precise_locator=loc,supporting_content=support,verification_status=status,applicability_limit=caution,origin=origin))
    # 保留逐項既有查核的血緣；不是本輪新增數，也不是由下載狀態升級。
    for r in read(OLD/'observations.csv'):
        ls=';'.join(x for x in r['lesson_ids'].split(';') if x in LESSONS)
        if not ls:continue
        kind='company_cases' if r['kind'].startswith('company') else ('taiwan_statistics' if r['entity'].startswith('Taiwan') or r['source_id'] in ('S_bank_csv','S_moa_2024','S_moa_scope','S_mof_2024_release','S_mof_ic_cbc') else 'global_statistics')
        add('I_'+r['observation_id'],ls,r['source_id'],f"{r['entity']}：{r['metric']} = {r['value']} {r['unit']}",'See original source version',r['period'],r['locator'],f"既有逐筆核對值 {r['value']} {r['unit']}；範圍：{r['scope']}；{r['stock_flow']}；{r['nominal_real']}；精度：{r['precision']}",r['caution'],kind,'inherited_verified_observation')
    add('N_TW12_DATE','00;01;30','V2_TW12_MANUAL','第12次行業統計分類於2026年1月1日生效；舊統計不能事後當作新制編製。','2026','2026','PDF4 公告','公告載明2025年12月12日修正，2026年1月1日生效。','2024零售統計仍依第11次分類。','policy_institutions')
    add('N_CLASS_UNIT','00;01','V2_TW12_MANUAL','行業分類須區分場所單位與企業單位。','2026','2026','PDF8 統計單位','原文分別說明場所單位與企業單位，分類對象不能以品牌名稱替代。','企業多業經營不等於只有單一產品市場。','technical_products')
    add('N_RETAIL_MARGIN','00;01;30','V2_TW12_MANUAL','判斷批零業主要經濟活動時，毛利額可作為附加價值的替代判準。','2026','2026','PDF9 主要經濟活動','批發零售業的商品銷售額不能直接作為與製造業產值可比的附加價值指標。','分類代理指標，不是精確國民所得估計公式。','technical_products')
    for year,desc,anchor in [('1962','首店於1962年7月2日在Rogers Arkansas開幕','1962'),('1969','1969年公司化為Wal-Mart Stores Inc.','1969'),('1983','1983年開設首家Sam’s Club，並導入電腦化銷售時點系統','1983'),('1988','1988年首家Supercenter把綜合商品與完整超市結合','1988'),('1991','1991年與Cifra合資進入墨西哥','1991')]:
        add('N_WM_'+year,'30','T_WALMART_HISTORY','Walmart：'+desc,'undated',year,'History timeline / '+anchor,'企業時間線明列該事件。','公司自述；不能由事件先後推定績效因果。')
    add('N_WM_REV','01;30','D_F023','Walmart FY2024總營收648,125百萬美元，淨銷售642,637百萬美元。','2024','FY ended 2024-01-31','PDF43 / printed41 Consolidated Results of Operations','表格分列Total revenues、Net sales與會員及其他收益。','不是曆年2024；不是世界零售市場規模。','company_cases')
    add('N_WM_OP','30','D_F023','Walmart FY2024營業利益27,012百萬美元；期末門店與會員店10,616。','2024','FY ended 2024-01-31','PDF43 / printed41 table and footnote1','Operating income及unit counts原表，門店包含期末營業據點、排除永久關閉據點。','門店不是全部物流據點；淨利不可代替營業利益。','company_cases')
    for year,event in [('1931','Richmond裝配廠啟用'),('1942','Richmond廠轉入戰時車輛生產'),('1945','Richmond廠恢復民用車輛生產'),('1955','Richmond廠關閉，灣區業務移至Milpitas較大廠址')]:
        add('N_FORD_'+year,'25','T_FORD_ARCHIVE','Ford：'+event,'2002',year,'PDF5 / printed4 Executive Summary；PDF2 site data','政府歷史工程紀錄的摘要與基本資料交叉支持此年份事件。','這是Richmond單廠，不代表Ford整家公司停產。')
    add('N_FORD_LOGISTICS','01;25','T_FORD_ARCHIVE','Ford區域裝配網絡與運輸成本有關：零件可比整車更密集裝載，Richmond同時連結港口與鐵路。','2002','1920s–1955','PDF5 / printed4 Executive Summary','摘要解釋Detroit製作零件、分廠裝配；船運及鐵路、起重機與輸送線串聯。','歷史個案的機制解釋；不是本輪估計的運費節省百分比。','value_chain')
    add('N_TSMC_1987','00;18','T_TSMC_1998','台積電1987年在新竹成立，以專業積體電路製造服務為定位。','not_stated; annual1998','1987','Company Profile opening paragraph','1998年原始年報公司簡介載成立時間、地點與dedicated foundry定位。','不把1998年市場地位當作2026年排名。')
    add('N_TSMC_BOUNDARY','00;18','T_TSMC_1998','台積電1998年年報稱章程禁止設計製造自有品牌IC，以成為客戶合作夥伴為定位。','not_stated; annual1998','1998','Company Profile / corporate charter paragraph','原文說明不與客戶以自有品牌競爭及製造服務關係。','公司策略自述；不是所有foundry的必然法律義務。','value_chain')
    add('N_TSMC_FABS','18','T_TSMC_1998','1998年底台積電有兩座六吋與三座八吋晶圓廠，年產能約160萬片八吋約當晶圓。','not_stated; annual1998','1998','Company Profile / wafer fabrication facilities','原文列廠數與1.6 million eight-inch equivalent wafers annual capacity。','產能不是實際出貨；不能與十二吋片數直接相加。','company_cases')
    add('N_TSMC_WAFERTECH','18','T_TSMC_1998','WaferTech於1998年年中開始量產。','not_stated; annual1998','1998','Company Profile / WaferTech paragraph','原文將美國合資廠量產與新加坡合資計畫分別描述。','新加坡廠2000年當時僅預定，不當作已實現。')
    add('N_TYSON_HISTORY','05','S_tyson_10k_2024','Tyson於1935年由John W. Tyson創立。','2024','1935','PDF4 / printed3 Item1 Business / General','公司年報成立沿革段載明創辦人與年份。','單一創立年份不構成完整家族史或產業史。')
    add('N_TYSON_CHAIN','05','S_tyson_10k_2024','Tyson雞肉業務涵蓋育種、契約農戶、飼料、加工、行銷與運輸。','2024','FY2024','PDF4 / printed3 Item1 Business / General','年報描述整合雞肉生產過程並明列contract farmers。','契約農戶不等於全部農場為公司所有；不得套用牛豬業務。','value_chain')
    add('N_RETAIL_TW','01;30','T_MOEA_RETAIL24','台灣2024年零售業營業額48,530億元，年增2.6%。','2025','2024','PDF2 / printed2 表2；PDF10 表2','原表總計48,530億元、2.6%，分類第11次修訂。','2025-01-23發布版本；不是最新回溯修訂值；營業額不是附加價值。','taiwan_statistics')
    add('N_RETAIL_ONLINE','30','T_MOEA_RETAIL24','台灣2024年零售業網路銷售額6,533億元，占該零售業營收13.5%。','2025','2024','PDF3 / printed3 表3','原表全年總計6,533億元；占各業營收比率13.5%。','包含有店面業者網路銷售；非僅電子購物及郵購業、非所有數位服務。','taiwan_statistics')
    add('N_RETAIL_FORMATS','30','T_MOEA_RETAIL24','2024年台灣便利商店營業額4,235億元、超級市場2,598億元、量販店2,484億元。','2025','2024','PDF2 / printed2 表2','同一年度同一發布版本的三列業態營業額。','這些業態不是完整零售業；不能當個別公司營收。','taiwan_statistics')
    add('N_EV_WORLD','25','T_IEA_EV25','2024年全球電動乘用新車銷量超過1,700萬輛，占新車銷量超過20%。','2025','2024','Electric car sales / Global electric car sales exceeded17million；figure Notes and sources','章節數字與圖註：BEV與PHEV，僅新乘用車。','不含全部商用車、機車或一般混合動力車；是2025報告實績，不是2024報告預測。','global_statistics')
    add('N_EV_MARKETS','25','T_IEA_EV25','2024年中國電動乘用車銷量超過1,100萬輛，美國約160萬輛。','2025','2024','Electric car sales / opening paragraphs','同章比較中國、美國、歐洲與其他市場。','四捨五入值；與總汽車產量不是同一分母。','global_statistics')
    add('N_FTC_TERMS','30','T_FTC_CARREFOUR','統一與家樂福結合附負擔要求關係供貨交易符合常規、不得無正當理由差別待遇。','2023','2023 decision','PDF1 附負擔1','條件比較統一企業與相當地位供貨商之整體商業條件。','條件要求不能當作業者過去已違法的證據。','policy_institutions')
    add('N_FTC_PROCURE','30','T_FTC_CARREFOUR','結合實施次日起三年內，家福與統一超商共同採購原則受限，原文另列例外。','2023','3years from implementation','PDF1–2 附負擔4','原文明列不得共同協商、決定交易條件並簽訂年度供銷合約，以及但書。','沒有實施日期與後續處分核對，不宣稱2026仍有效；不是永久全面禁止。','policy_institutions')
    add('N_JPM_ORIGINS','31','T_JPM_HISTORY','JPMorganChase把其歷史追溯至1799年紐約水公司，現今組織整合眾多前身機構。','undated','1799; history snapshot2026','Looking to the past investing in the future / founding paragraph','官方歷史說明The Manhattan Company及多個前身銀行。','公司歷史敘事，不等於今日JPMorgan Chase Bank N.A.同一法律實體自1799未曾變更。')
    add('N_ROBOTS_SAMPLE','25','T_ROBOTS_JPE2020','機器人與就業研究以美國本土722個通勤區分析地方勞動市場。','2020','1990–2007 main; extensions2014','PDF16–17 SectionIII B–C','原文明列722 commuting zones；Census與ACS，2007結果使用2006–08資料。','不是企業面板；19個IFR產業含製造與非製造；機器人採用窗不等於結果窗。','academic')
    add('N_ROBOTS_EFFECT','25','T_ROBOTS_JPE2020','主要IV估計：每千名勞工增加一台工業機器人，地方就業人口比相對下降0.39個百分點，時薪約下降0.77%。','2020','1990–2007','PDF50–51 SectionVI A–B；Table7 panelA columns3,6','正文估計及標準誤分別為-0.39(0.09)、-0.77(0.15)，以州內空間相關及異質變異穩健處理。','地方相對效果；因果解釋依賴歐洲採用工具變數識別假設。全國效果需額外模型與跨區外溢假設；不得套用台灣或生成式AI。','academic')
    add('N_BASKER_MECHANISM','30','T_BASKER_NYU','Basker以文獻綜述說明資訊技術與規模、範疇及密度經濟的互補。','2007','historical evidence through2007','PDF5–8 / manuscript printed4–7 Section2','討論物流、配銷、存貨控制、分店密度與自我蠶食間的取捨。','作者2007年4月稿；不是正式期刊177–198頁；引用的量化研究尚須追讀原始論文。','academic')
    add('N_BASKER_SELECTION','30','T_BASKER_NYU','Walmart進入地方市場是內生選擇，簡單前後比較不足以識別其影響。','2007','historical literature through2007','PDF4 / printed3 Introduction','作者明確討論需求、成本與暫時成長可能影響選址及前後比較偏誤。','方法警告及綜述，不是此稿新估計的平均處理效果。','academic')
    add('N_YULON_PARENT','25','T_YULON24','裕隆2024年個體營業收入25,910,182仟元、營業淨利744,745仟元。','2025','2024','PDF87 / printed82 個體財務績效比較分析表','同表營業收入與營業淨利列；致股東書PDF6用億元四捨五入交叉核對。','個體，不是合併；本輪核讀年報比較表，未另取完整查核財報意見。','company_cases')
    add('N_YULON_GROUP','25','T_YULON24','裕隆2024年合併營業收入85,776,046仟元、營業淨利7,269,249仟元。','2025','2024','PDF86 / printed81 合併財務績效比較分析表','原表同時列營業成本58,894,837仟元、稅後淨利6,927,727仟元。','合併含多種業務；不得當作台灣整車製造產值。','company_cases')
    add('N_YULON_OPERATING','25','T_YULON24','裕隆2024年NISSAN與LUXGEN兩品牌總提車29,122台。','2025','2024','PDF6 / printed1 致股東報告書','公司原文以總提車台數描述29,122台及成長6.4%。','公司提車不是交通部全市場領牌數；不得用公會產量當相同分母。','company_cases')
    add('N_TW_AUTO_PROD','25','T_TTVMA','台灣2024年汽車生產275,156輛。','undated','2024','台灣汽車產銷統計表 / 2024欄 / 生產台數列；表下注','公會調查整理之生產台數，與2023年285,962輛分欄。','產業公會第一手調查，非政府官方生產統計；已獨立標示來源身份。','taiwan_statistics')
    add('N_TW_AUTO_REG','25','T_TTVMA','台灣2024年汽車領牌合計457,844輛，其中國產233,271輛、進口224,573輛。','undated','2024','台灣汽車產銷統計表 / 2024欄 / 合計與國產、進口列；表下注','表下注銷售台數來源為交通部領牌數；目前由公會轉載核對。','官方次級重製，未取得交通部原表；產量與國內領牌量不同，不以差額直接推算出口。','taiwan_statistics')
    add('N_TW_EV_POLICY','25','T_MOEA_EV','經濟部2025年6月26日說明以產創平台支持國產電動車，Model C自2024年量產上市。','2025','2024–2025','2025-06-26新聞 / 電動小客車段','機關原文說明政策工具、國內開發與在地生產，至2025年5月底累計領牌8,796輛。','8,796為累計至2025-05，不是2024全年；外銷計畫不當成完成訂單交付。','policy_institutions')

    scopes={'V2_TW12_MANUAL':'PDF4,6–9：生效日、統計單位、主要活動與零售口徑','T_WALMART_HISTORY':'Timeline1962,1969,1983,1988,1991 entries only','T_FORD_ARCHIVE':'PDF1–2,5 / cover,site data,Executive Summary only','T_TSMC_1998':'Company Profile substantive HTML text','S_tyson_10k_2024':'PDF4 Item1; prior FY2024 financial audit retained','T_MOEA_RETAIL24':'PDF1–4,10; definitions and tables2–3','T_IEA_EV25':'Opening electric car sales paragraphs and figure definition notes','T_FTC_CARREFOUR':'PDF1–3 all conditions read','T_JPM_HISTORY':'Opening founding/predecessor paragraphs only; embedded timeline not exhaustively reviewed','T_ROBOTS_JPE2020':'PDF1–4,10–13,16–17,49–51; research question,method,data,IV and scope; remaining sections not line-by-line read','T_BASKER_NYU':'PDF1–6,7–8,22–23 substantive sections consulted; manuscript only, not typeset journal'}
    for sid,scope in scopes.items():
        sources[sid]['status']='fulltext_read';sources[sid]['read_scope']=scope
    for sid,scope in {'T_YULON24':'PDF6,86–87 / printed1,81–82 shareholder report and parent/consolidated comparisons only','T_TTVMA':'汽車產銷統計表2024欄、年度標題與表下注；未核讀機車','T_MOEA_EV':'2025-06-26新聞政策及電動小客車段'}.items():
        sources[sid]['status']='fulltext_read';sources[sid]['read_scope']=scope
    if 'T_BASKER_2007' in sources:
        sources['T_BASKER_2007']['status']='abstract_verified';sources['T_BASKER_2007']['read_scope']='AEA bibliographic/abstract landing page only; PDF blocked'
    for sid,s in sources.items():
        if s['publication_year']=='See version':
            s['publication_year']='not_rechecked_this_batch'
    for sid,year in {'T_FORD_ARCHIVE':'2002','T_TSMC_1998':'not_stated; annual1998','T_YULON24':'2025','T_ROBOTS_JPE2020':'2020','T_BASKER_NYU':'2007','T_WALMART_HISTORY':'undated','T_JPM_HISTORY':'undated','T_TTVMA':'undated'}.items():sources[sid]['publication_year']=year
    for sid,identity in {'T_TTVMA':'台灣區車輛工業同業公會；生產為公會原始調查、領牌為交通部數據重製，非政府原始表','T_YULON24':'裕隆汽車製造股份有限公司2024年報；個體與合併分列','T_MOEA_EV':'經濟部產業發展署2025-06-26官方政策新聞','T_FORD_ARCHIVE':'NPS Historic American Engineering Record CA-326-H；LOC典藏；Fredric L. Quivik, Summer2002','T_BASKER_NYU':'NYU Faculty Digital Archive；2007年4月作者稿，非正式期刊排版','T_ROBOTS_JPE2020':'MIT經濟系保存之JPE2020期刊格式原文；印刷頁未編000'}.items():sources[sid]['identity']=identity
    for c in claims:
        if c['publication_year']=='See original source version':c['publication_year']=sources[c['source_id']]['publication_year']
    write('claims.csv',claims)
    # 原450列保留；新分類是檢索映射，不宣稱舊分類已提供技術知識。
    mapping={'classification':('technical_products;policy_institutions','分類可定義邊界，但不能替代產品技術證據'),'global':('global_statistics',''),'taiwan':('taiwan_statistics',''),'history':('industry_history',''),'company':('company_cases',''),'academic':('academic',''),'visual':('images_rights',''),'recent':('policy_institutions','近期動態不必全屬政策；仍須逐列確認'),'cross_industry':('value_chain','跨產業連結不代表完整價值鏈')}
    gaps=read(ROOT/'research/audit/full-acquisition-v2/lesson_gaps.csv'); out=[]
    for i,r in enumerate(gaps,1):
        cat,note=mapping[r['evidence_kind']]
        out.append(dict(legacy_gap_id=f'G{i:03}',lesson_id=r['lesson_id'],legacy_kind=r['evidence_kind'],requested_categories=cat,mapping_limit=note,legacy_status=r['source_status'],closed_by_this_mapping='false'))
    write('gap_reclassification.csv',out)
    papers=[]
    for r in read(OLD/'paper_reviews.csv'):
        ls=';'.join(x for x in r['lessons'].split(';') if x in LESSONS)
        if ls:
            r=dict(r);r['lessons']=ls;r['verification_origin']='prior_batch_core_read_not_new';r['status']='fulltext_read';papers.append(r)
            s=sources[r['source_id']];s['status']='fulltext_read';s['read_scope']='Inherited previous audit, not newly read: '+r['locator'];s['publication_year']=r['year']
    # 統一欄位、保存兩個新核讀版本，不以作者稿冒充正式期刊PDF。
    fields=list(papers[0]);
    for values in [dict(id='NEW_ROBOTS2020',authors='Daron Acemoglu; Pascual Restrepo',year='2020',title='Robots and Jobs: Evidence from US Labor Markets',journal='Journal of Political Economy128(6)',doi='10.1086/705716',version='MIT institutional journal-format pre-pagination copy; printed000; use PDF locators',lessons='25',question='工業機器人如何影響美國地方就業與工資？',mechanism='工作替代與生產力效果並存；跨區商品價格及資本收益外溢',sample='722 continental US commuting zones;19 IFR industries',period='1990–2007 main outcomes; robot adoption1993–2007; extensions2014',variables='baseline industrial employment shares; adjusted robot penetration; employment/population; log hourly wages',method='2SLS；歐洲產業機器人採用作工具變數；人口加權、地區及貿易等控制',results='地方就業人口比-0.39pp(SE0.09)、時薪約-0.77%(SE0.15)；非全國淨效果',limitations='排除與歐洲機器人採用共變的其他美國地方衝擊；全國推算另需結構模型；不能外推AI或今日台灣',locator='PDF16–17 data;PDF49–51 IV/magnitudes',status='fulltext_read',gap='未逐行讀全部57頁或附錄；未完成全球機器人市場與台灣汽車採用資料',source_id='T_ROBOTS_JPE2020',verification_origin='this_batch_core_sections'),dict(id='NEW_BASKER2007MS',authors='Emek Basker',year='2007',title='The Causes and Consequences of Wal-Mart’s Growth',journal='Related to JEP21(3):177–198; downloaded version is April2007 manuscript',doi='10.1257/jep.21.3.177',version='NYU archive April2007 author manuscript33PDFpages; not journal pagination',lessons='30',question='Walmart優勢來源及對勞工、消費者、競爭者與供應商的影響？',mechanism='IT、規模、範疇與密度經濟互補；採購議價與商業網絡',sample='文獻綜述；無單一新實證N；不得把引用研究樣本併為本篇樣本',period='多個歷史研究、截至2007；非統一估計窗',variables='概念：物流成本、規模、密度、買方力量、選址內生性',method='經濟研究與產業史料綜述，討論識別困難',results='技術與規模的回饋、選址的內生性；本稿轉述的因果估計須回查原研究',limitations='作者稿與正式版差異未逐字對照；美國歷史案例，不能代替台灣零售估計',locator='PDF4–8 manuscriptpp3–7;PDF22–23 pp21–22',status='fulltext_read',gap='AEA正式PDFrestricted；Basker2005原始實證PDFbroken；需追查Holmes等原始論文',source_id='T_BASKER_NYU',verification_origin='this_batch_author_manuscript_core_sections')]:
        papers.append({k:values.get(k,'') for k in fields})
    write('literature_readings.csv',papers)
    write('sources.csv',list(sources.values()))
    timelines=[dict(event_id=c['claim_id'],lesson_ids=c['lesson_ids'],event_year=c['data_year'],event=c['claim'],claim_id=c['claim_id'],source_id=c['source_id'],locator=c['precise_locator'],scope_limit=c['applicability_limit']) for c in claims if c['category']=='industry_history']
    write('timelines.csv',timelines)
    build_lessons(claims,papers,out)

def build_lessons(claims,papers,mapping):
    categories={'industry_history':'產業歷史','global_statistics':'全球統計','taiwan_statistics':'台灣統計','technical_products':'技術與產品','value_chain':'價值鏈','company_cases':'企業案例','academic':'學術研究','policy_institutions':'政策制度','images_rights':'圖像與授權'}
    plans={
    '00':('產業邊界與分類','以台積電專業代工及銀行法律實體展示企業、場所與產品市場的差別。','N_CLASS_UNIT;N_TSMC_BOUNDARY','還缺分類制度完整國際沿革、產品市場與行業差異的對照案例、一般讀者術語表證據。','場所單位 → 主要經濟活動 → 分類碼 → 統計範圍；企業另有多業與跨國邊界','Coase與TW12支持邊界，不能把TCE當分類規則。'),
    '01':('全球產業地圖','比較農業數量、半導體出口、銀行存量與零售營收，先解釋分母再比較。','I_O_FAO_CEREALS;I_O_GLOBAL_CHIPS;I_O_BIS_CREDIT;N_RETAIL_TW','還缺一致年度與分類之世界各產業附加價值、地區就業及跨國比較時間序列。','生產數量／價格 → 產值 → 中間投入 → 附加價值；跨境貨物流另列','不可將不同統計量相加作世界產業規模；目前只有跨口徑教學例。'),
    '05':('農業','以Tyson雞肉整合鏈與大成飼料／食品經營對照，補出農戶在價值鏈的位置。','N_TYSON_CHAIN;I_B_DACHAN_FEED','還缺台灣農地、農戶、勞動與作物長期史；糧食政策與風險；大成轉型歷程的逐年原證。','種苗／飼料 → 農場及契約農戶 → 加工冷鏈 → 批零與餐飲 → 消費者','Tyson1935只是一個歷史節點，不能代表世界農業史；飼料食品集團不是典型小農。'),
    '18':('半導體','用台積電1987–1998原始史料串起專業代工，對照2024台積電與Intel財報。','N_TSMC_1987;N_TSMC_BOUNDARY;N_TSMC_FABS;I_B_INTEL_RD','還缺電晶體與IC發明原始史料、設備材料／EDA／先進封裝技術、製程政策及全球產銷同口徑資料。','IP／EDA與設計 → 晶圓製造 → 封裝測試 → 系統；設備材料支援各環節','OECD16HS出口不是純IC市場份額；台積電兩套財報利潤不可混接。'),
    '25':('汽車','以Ford Richmond港鐵裝配史展示大量生產網絡，再接電動車轉型與勞動市場研究。','N_FORD_LOGISTICS;N_FORD_1931;N_FORD_1955;N_EV_WORLD;N_ROBOTS_EFFECT','還缺台灣車廠完整財報核讀、整車與零組件統計、ICE／BEV技術、經銷與售後、關稅及在地化政策。','原料／電池及零組件 → 系統整合與整車裝配 → 經銷與金融 → 使用維修及回收','Ford是全球企業的單廠故事；EV數字只含BEV/PHEV新乘用車；勞動研究不是汽車業全貌。'),
    '30':('零售','以Walmart業態與物流演變為主故事，以台灣業態統計及統一家樂福結合限制補足地方制度。','N_WM_1962;N_WM_1988;N_WM_REV;N_RETAIL_FORMATS;N_FTC_PROCURE;N_BASKER_MECHANISM','還缺世界一致定義零售統計、台灣代表企業經營及財報、百貨／超商／電商長期轉型史、期刊正式版及原始實證。','供貨商 → 採購議價與配送 → 門店／網店 → 消費者；銷售與庫存訊息回流','作者綜述不等於每個因果效果已核對；條件性核准不等於永久禁令。'),
    '31':('銀行','以JPMorgan多前身歷史提示銀行組織演變，搭配JPM銀行與兆豐銀行本體財報、Diamond–Dybvig機制。','N_JPM_ORIGINS;I_C_JPMBANK_deposits;I_C_MEGA_deposits_and_remittances;I_O_BIS_CREDIT','還缺中央銀行與存保制度歷史、銀行監理與資本風險、兆豐合併前後原始史料，以及全球銀行總量一致系列。','存款及資本 → 授信與證券資產 → 支付／清算與費用；期限及風險管理跨越全鏈','BIS跨境信用非全球銀行總資產；銀行本體、金控與監理列範圍不同。')}
    readiness=[];figures=[];requirements=[]
    for l in LESSONS:
        title,story,ids,missing,chain,limits=plans[l]
        cs=[c for c in claims if l in c['lesson_ids'].split(';')];ps=[p for p in papers if l in p['lessons'].split(';')]
        lines=[]
        for cat,label in categories.items():
            count=sum(c['category']==cat for c in cs)
            judgement='partial' if count else 'gap'
            if cat=='images_rights':judgement='redraw_plan_only'
            lines.append(f'| {label} | {count} | {judgement} |')
            requirements.append(dict(requirement_id=f'T{l}_{cat}',lesson_id=l,category=cat,verified_claim_count=count,status=judgement,whole_dimension_sufficient='false',legacy_gap_ids=';'.join(r['legacy_gap_id'] for r in mapping if r['lesson_id']==l and cat in r['requested_categories'].split(';')),remaining_need=missing if not count else '有局部證據；仍須補完整歷史、地理、期間與一般讀者解釋；不以筆數判充分'))
        table='| 領域 | 已核對主張 | 準備狀態 |\n|---|---:|---|\n'+'\n'.join(lines)
        ev='\n'.join(f"- `{c['claim_id']}` {c['claim']}〔{c['source_name']}；{c['precise_locator']}〕" for c in cs)
        paperlines='\n'.join(f"- {p['authors']} ({p['year']})，{p['version']}。核讀：{p['locator']}。限制：{p['limitations']}。來源`{p['source_id']}`。" for p in ps) or '- 尚無已核讀且適用本課的期刊原文；不得以候選替代。'
        md(f'lesson-{l}/evidence_pack.md',f'# 第{l}堂｜{title}：研究證據包\n\n研究用途，非正式教材，未通過四階段出版審查。查核日期：2026年11月6日。\n\n{story}\n\n## 可追溯事實\n\n{ev}\n\n## 歷史與企業故事的證據界線\n\n{limits}\n\n年代事件見[時間線](../timelines.csv)，每項以claim_id回查[主張表](../claims.csv)。本課沒有事件列的時期仍是缺口，不以推測補齊。既有六家企業財報查核見[前批研究包](../../deep-2026-11-06/README.md)。\n\n## 原文核讀與適用範圍\n\n{paperlines}\n\n## 價值鏈、商業模式與競爭機制\n\n{chain}。這是研究者的概念化整理，不是經估計的市場流量。支撐入口：{ids}；未有逐環節直接證據的部分列為待驗證，不將示意圖冒充已觀察到的產業結構。\n\n{limits}\n\n## 待驗證主張與缺口\n\n{missing}\n\n產業成長是否由特定企業、政策或技術造成，尚須比較研究或原始過程資料；年度報告的管理階層解釋不可直接當作因果識別。\n\n## 圖像方案\n\n自行繪製上述概念流程圖，明標「概念示意、非比例圖」，附claim IDs。數據圖只可取用已核對同口徑值，不複製PDF圖版。照片逐張授權尚未取得，不能使用公司網站圖片當作免授權素材。\n\n[本課撰寫準備度](teaching_readiness_report.md)\n')
        md(f'lesson-{l}/teaching_readiness_report.md',f'# 第{l}堂｜{title}：撰寫準備度\n\n**尚未達到可撰寫完整10,000–15,000字正式教材初稿的證據標準。** 可開始具來源的局部章節筆記，不據此宣稱課程完成。\n\n{table}\n\n已可使用：{story} 主張與範圍見[evidence_pack.md](evidence_pack.md)。合計{len(cs)}筆主張，其中{sum(c["origin"]=="new_original_read" for c in cs)}筆為本批新原文查核；各課共享主張不得加總當成獨立新增筆數。\n\n阻斷完整初稿的缺口：{missing}\n\n{limits}\n\n技術產品解釋、完整歷史、全球與台灣對照、企業歷程、一般讀者術語及圖表都必須有直接證據。表中partial只代表已有部分查核；不代表該領域充分。\n\n出版四關：資料與事實審查「局部」；理論與推論審查「未完成」；零基礎教學與文字審讀「未開始」；獨立第二輪審讀及修訂「未開始」。自動驗證只查結構與一致性。\n')
        readiness.append(dict(lesson_id=l,title=title,verified_claims=len(cs),new_claims=sum(c['origin']=='new_original_read' for c in cs),linked_readings=len(ps),ready_for_complete_draft='false',publication_review_passed='false',blocking_gaps=missing))
        figures.append(dict(figure_id='FIG_'+l,lesson_id=l,purpose='說明環節與統計邊界',proposed_visual=chain,source_claim_ids=ids,rights='Original redraw only; source facts cited; no third-party image embedded',status='plan_not_rendered',limit='conceptual; not proportional; unsupported edges require further source verification'))
    write('readiness.csv',readiness);write('priority_requirements.csv',requirements);write('figure_plans.csv',figures)
    md('README.md','# 正式教材證據研究包｜2026年11月6日\n\n以9a5f648為基礎，優先00、01、05、18、25、30、31。這是研究成果，七課均尚未具備完整10,000–15,000字初稿所需證據，也未完成出版審查。\n\n- [逐主張證據](claims.csv)：new_original_read與inherited_verified_observation分開；supporting_content為研究者中文釋義，不是原文逐字引文。\n- [來源與閱讀範圍](sources.csv)：fulltext_read只代表所列核心章節實際核讀，不表示逐行讀完全篇。claim_verified只放在逐主張表，不把文件全面升級。\n- [核讀卡](literature_readings.csv)：新增JPE2020期刊排版未編頁copy與Basker2007作者稿；正式JEP PDF受限，作者稿不冒充正式版。前批已核讀文獻保留血緣。\n- [450舊缺口映射](gap_reclassification.csv)：450列全保留，多重分類，沒有因重分類而結案。分類資料不能替代產品技術資料。\n- [七課63項需求](priority_requirements.csv)、[準備度](readiness.csv)、[時間線](timelines.csv)、[圖像方案](figure_plans.csv)。\n\n閱讀狀態：bibliography_only=只識別；abstract_verified=僅摘要；fulltext_downloaded=取得全文未完成核讀；fulltext_read=指定範圍已核讀；claim_verified=逐項有定位且未超出來源支持。這些不是自動隨下載器推進的同義詞。來源表保留失敗與受限的bibliography_only記錄，取得全文仍須查read_scope。\n\n複現：先執行既有full_acquisition.py fetch --lessons all --resume --skip-verified；本包可由python research/scripts/build_teaching_foundation.py重建（原始查核內容固定於程式，原件不公開）。再跑validate_teaching_foundation.py、validate_full_acquisition.py、validate_deep_evidence.py、validate.py。來源的公開可讀不等於可重散布，原始PDF/HTML全部留在忽略的private_sources。\n\n後續逐課進入lesson-NN/teaching_readiness_report.md；先補阻斷缺口，不以候選來源數量當完成率。\n')
    print(json.dumps({'claims':len(claims),'new_claims':sum(c['origin']=='new_original_read' for c in claims),'inherited_claims':sum(c['origin']!='new_original_read' for c in claims),'source_records':len(set(c['source_id'] for c in claims)),'legacy_gaps':len(mapping),'priority_requirements':len(requirements),'complete_draft_ready':0}))

if __name__=='__main__':main()
