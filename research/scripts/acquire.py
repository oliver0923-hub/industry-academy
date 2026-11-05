"""可重跑的有界來源蒐集；不使用憑證、不推送全文、不改網站。"""
from pathlib import Path
import csv, json, re, hashlib, sys, time, difflib
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, quote
import requests
import pandas as pd
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]
R=ROOT/'research'; PRIVATE=ROOT/'private_sources'
DATE='2026-11-06'
for d in ['registries','notes/theory_cards','notes/lessons','audit','schemas','sources','scripts']:
    (R/d).mkdir(parents=True,exist_ok=True)
PRIVATE.mkdir(exist_ok=True)
LOG=[]
def write_csv(name,rows,fields=None):
    path=R/name; path.parent.mkdir(parents=True,exist_ok=True)
    fields=fields or list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def read_csv(name):
    p=R/name
    return list(csv.DictReader(p.open(encoding='utf-8'))) if p.exists() else []
def fetch(url,key,kind='html'):
    ext={'html':'.html','json':'.json','pdf':'.pdf','xlsx':'.xlsx','csv':'.csv','odt':'.odt'}.get(kind,'.bin')
    path=PRIVATE/(key+ext)
    entry=dict(resource_id=key,url=url,accessed_at=DATE,http_status='',status='',content_type='',bytes=0,sha256='',local_path='',license='not assessed; local use only',reason='')
    try:
        if path.exists():
            data=path.read_bytes();entry.update(status='cached_download',local_path='private_sources/'+path.name)
        else:
            response=requests.get(url,timeout=(8,28),headers={'User-Agent':'IndustryAcademyResearch/1.0 (personal scholarly research)'})
            entry.update(http_status=response.status_code,content_type=response.headers.get('Content-Type',''),final_url=response.url)
            response.raise_for_status();data=response.content
            if not data: raise ValueError('empty response')
            if kind=='pdf' and not data.startswith(b'%PDF'):raise ValueError('not a PDF; possible access/login/error page')
            if kind in ['xlsx','odt'] and not data.startswith(b'PK'):raise ValueError('not ZIP-based office format')
            if kind=='json':json.loads(data)
            if kind=='html':
                text=data[:150000].decode('utf-8','ignore').lower()
                if any(x in text for x in ['just a moment...','access denied','verify you are human','request unsuccessful']):raise ValueError('challenge or denied page')
            path.write_bytes(data);entry.update(status='downloaded',local_path='private_sources/'+path.name)
        entry.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        return data,entry
    except Exception as e:
        entry.update(status='restricted' if str(entry.get('http_status')) in ['401','403','429'] else 'failed',reason=str(e)[:350])
        return None,entry
    finally:LOG.append(entry)
def flush_log():
    old=read_csv('audit/download_log.csv')
    merged={ (x['resource_id'],x['url']):x for x in old+LOG }
    write_csv('audit/download_log.csv',list(merged.values()))
def soup(data):return BeautifulSoup(data.decode('utf-8-sig','replace'),'html.parser')
def lessons():
    js=(ROOT/'docs/app.js').read_text(encoding='utf-8-sig')
    return json.loads('['+js.split('const TITLES=[')[1].split('];')[0]+']')
def base_phase():
    (ROOT/'.gitignore').write_text('private_sources/\n__pycache__/\n*.pyc\n',encoding='utf-8')
    (R/'README.md').write_text('''# Industry Academy 研究知識庫

來源蒐集批次：2026-11-06。保留 v2.0 的 00–49 課號及網站九個群組；原文「十個模組」與實際九組不同，不重編。

本庫是可追溯的來源索引與研究卡，並非 50 堂正式講義。所有原文下載只在被 Git 忽略的 `private_sources/`；公開成果為原創筆記、來源連結及核對狀態。即使可公開瀏覽，亦不推定可重新散布全文。不得使用 Railway、修改 M&A Academy、覆寫 docs 或變更 Pages。

`registries/`：七份主索引；`notes/theory_cards/`：逐篇研究卡；`notes/lessons/`：逐課來源狀態；`audit/`：下載、覆蓋與限制；`schemas/`：欄位約定；`scripts/`：蒐集及驗證程序。

執行：Python 3，安裝 requests pandas beautifulsoup4 openpyxl pypdf。依序執行 `python research/scripts/acquire.py 1` 至 `4`，最後 `python research/scripts/validate.py`。網路結果會隨時間變動；本批日期固定保留，不宣稱即時同步。重跑沿用本機快取，下載紀錄記為 cached_download。

狀態：metadata=僅書目或入口；sourced=已有特定資料/文件且核對內容；reviewed=已閱讀原文與核對主張；teaching-ready=另需正式教材審查，本批不使用。HTTP 200 只代表入口可讀，不能證明資料已下載、全文可讀或單位一致。

授權：未取得可用的已登入校園 session；不讀取憑證。使用者允許使用台大管理學院可用內容，取得困難時可略過。受限文件保留 DOI 與存取佇列。
''',encoding='utf-8')
    (R/'schemas/README.md').write_text('''# Schema 與使用限制

所有 CSV 為 UTF-8，空字串代表未知，不以 0 代替。代碼、lesson_id 一律字串讀入（保留前導零）。主鍵：source_id、paper_id、filing_id；分類為 system/version/code；矩陣為 lesson_id/reference_id/source_role。外鍵必須存在。license=unknown 不代表開放授權。

source_registry：source_id,agency,dataset,measure,definition,unit,nominal_real,geography,frequency,coverage,update_frequency,url,license,access_status,lesson_ids,downloaded_on,verification_status。入口核對與資料取回分開。
literature_master：paper_id,authors,year,title,journal_or_publisher,publication_type,peer_reviewed,doi,landing_url,oa_url,access_status,license,theory,mechanism,industry_scope,lesson_ids,bibliographic_verified,fulltext_verified,notes；額外 volume/issue/pages/metadata_url 等為追溯欄位。Crossref 的 journal-article 類型不能單獨證明同行評審。
industry_lesson_matrix：lesson_id,reference_id,reference_type,source_role,confidence,verified_at,status。confidence 僅文字依據（official publisher / curated candidate），不是統計機率。
company_filings：filing_id,issuer,identifier,ticker,fiscal_year,reporting_currency,audited,source_url,filing_date,geography,lesson_ids,status。IR 主頁只能為 candidate，不可標示 filing_verified。
classification_master：system/version/code/label/definition/url/accessed_at/level/parent_code/verification_status。空定義代表尚未取得，標籤不可冒充完整活動定義。
classification_crosswalk：from_system/from_version/from_code/to_system/to_version/to_code/verified/confidence/notes/url。官方表未完成列解析時只記 artifact 索引，不猜配對。
indicator_dictionary：指標分開定義，不能加總營收、GDP、出口、市值、產能、市場規模。
audit/download_log：實際 HTTP 狀態、下載格式、bytes、SHA-256、失敗原因與本機相對路徑；不提交 cookies、token 或原始下載內容。
''',encoding='utf-8')

CORE=[
('Bain concentration profitability','10.2307/1882217','IO/SCP','市場集中與進入障礙；不直接推論當代因果效果'),
('Porter five forces','','Five Forces','供應商、買方、替代品、潛在進入與既有競爭'),
('Barney resources','10.1177/014920639101700108','RBV','異質且難以模仿的資源與持續競爭優勢'),
('Williamson transaction costs','10.1086/466942','TCE','交易特性與治理安排配適'),
('Gereffi value chains','10.1080/09692290500049805','GVC','交易複雜度、可編碼性與供應商能力'),
('Teece appropriability','10.1016/0048-7333(86)90027-2','Innovation','可占有性與互補資產影響創新價值攫取'),
('Henderson Clark architecture','10.2307/2393549','Architectural innovation','元件連結改變可能使既有組織知識失效'),
('Cohen Levinthal absorption','10.2307/2393553','Absorptive capacity','先前知識與辨識吸收運用外部知識'),
('Teece Pisano Shuen capabilities','10.1002/(SICI)1097-0266(199708)18:7<509::AID-SMJ882>3.0.CO;2-Z','Dynamic capabilities','整合、建立及重組能力；不等於任何成功事後解釋'),
('Baldwin Clark modularity','10.7551/mitpress/2366.001.0001','Modularity','設計規則與模組分工的選擇權'),
('Adner ecosystem','10.1177/0149206316678451','Ecosystem','價值主張要求互補活動與多方位置配適'),
('Rochet Tirole platforms','10.1162/154247603322493212','Two-sided markets','跨邊網路效果與價格結構'),
('Dyer Singh relational view','10.5465/amr.1998.1255632','Relational view','關係專屬資產、知識共享及互補資源'),
('Ocasio attention','10.1002/(SICI)1097-0266(199707)18:1+<187::AID-SMJ936>3.0.CO;2-K','ABV','注意力的組織分配影響議題與行動選擇'),
('Geopolitical supply chains','10.1080/09537287.2023.2286283','Geopolitical disruption','供應鏈重構與地緣政治風險；review 不等於因果識別')]

def paper_metadata(item):
    time.sleep(1.1)  # Crossref 小批次限流，禁止高頻重試
    key,doi,theory,mechanism=item
    pid='P'+str(CORE.index(item)+1).zfill(3) if item in CORE else 'X'+hashlib.sha256(doi.encode()).hexdigest()[:9]
    if not doi:
        return dict(paper_id=pid,authors='Michael E. Porter',year='2008',title='The Five Competitive Forces That Shape Strategy',journal_or_publisher='Harvard Business Review',publication_type='management_article',peer_reviewed='false',doi='',landing_url='https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy',oa_url='',access_status='metadata_only',license='unknown',theory=theory,mechanism=mechanism,industry_scope='跨產業候選機制，需逐課論證',lesson_ids='',bibliographic_verified='false',fulltext_verified='false',notes='非同行評審實證研究；需出版社頁核對',volume='86',issue='1',pages='78–93',metadata_url='')
    url='https://api.crossref.org/works/'+quote(doi,safe='')
    data,log=fetch(url,'crossref_'+pid,'json')
    row=dict(paper_id=pid,authors='',year='',title=key,journal_or_publisher='',publication_type='',peer_reviewed='unknown',doi=doi.lower(),landing_url='https://doi.org/'+doi,oa_url='',access_status='metadata_only',license='unknown',theory=theory,mechanism=mechanism,industry_scope='跨產業候選；須區分情境適用性',lesson_ids='',bibliographic_verified='false',fulltext_verified='false',notes='',volume='',issue='',pages='',metadata_url=url)
    if data:
        m=json.loads(data)['message']
        row.update(authors='; '.join(' '.join([a.get('given',''),a.get('family','')]).strip() for a in m.get('author',[])),year=str(m.get('published',m.get('issued',{})).get('date-parts',[['']])[0][0]),title='; '.join(m.get('title',[])),journal_or_publisher='; '.join(m.get('container-title',[])) or m.get('publisher',''),publication_type=m.get('type',''),volume=m.get('volume',''),issue=m.get('issue',''),pages=m.get('page',''),bibliographic_verified='true',license='; '.join(sorted(set(l.get('URL','') for l in m.get('license',[])))) or 'unknown')
        row['peer_reviewed']='false' if m.get('type') in ['book','monograph','book-chapter'] else 'journal_status_to_verify'
        row['notes']='Crossref DOI 登錄核對成功；並非全文核對或同行評審認證。'
    return row

def phase1():
    base_phase()
    papers=list(map(paper_metadata,CORE))
    write_csv('registries/literature_master.csv',papers)
    classifications=[('TW_SIC','11','https://www.stat.gov.tw/StandardIndustrialClassification.aspx?RID=11&n=3144&sms=11195'),('TW_SIC_FILES','11','https://www.stat.gov.tw/News_Content.aspx?n=3144&s=90015'),('NAICS','2022','https://www.census.gov/naics/'),('SIC','1987','https://www.osha.gov/data/sic-manual'),('TWSE','accessed_2026-11-06','https://twse-regulation.twse.com.tw/TW/law/DOC01.aspx?FLCODE=FL007104&FLNO=2'),('ISIC','5','https://unstats.un.org/unsd/classifications/Econ/isic'),('ISIC','4','https://unstats.un.org/unsd/classifications/Econ/isic/Rev4/default.asp')]
    rows=[];artifacts=[]
    for system,version,url in classifications:
        data,log=fetch(url,system+'_'+version)
        artifacts.append(dict(source_id='C_'+system+'_'+version,agency=system,dataset='官方分類 '+version,measure='classification',definition='分類定義、排除與階層；依實際取回範圍',unit='code',nominal_real='not_applicable',geography='Taiwan' if system.startswith('TW') else 'United States' if system in ['SIC','NAICS'] else 'Global',frequency='revision',coverage=version,update_frequency='by revision',url=url,license='unknown; link and original notes only',access_status=log['status'],lesson_ids=';'.join(f'{n:02}' for n in range(50)),downloaded_on=DATE if data else '',verification_status='landing_retrieved' if data else 'unverified'))
        if data:
            s=soup(data)
            for a in s.select('a[href]'):
                label=a.get_text(' ',strip=True);href=urljoin(url,a['href'])
                if system=='SIC' and re.match(r'Division\s+[A-J]',label,re.I):
                    code=re.search(r'Division\s+([A-J])',label,re.I)[1]
                    rows.append(dict(system=system,version=version,code=code,label=label,definition='',url=href,accessed_at=DATE,level='division',parent_code='',verification_status='official_label_only'))
                if system=='TW_SIC' and 'StandardIndustrialClassificationContent' in href:
                    match=re.match(r'([A-S])\s*[\s：:、.-]*(.+)',label)
                    if match:rows.append(dict(system='TW_SIC',version='11',code=match[1],label=match[2],definition='',url=href,accessed_at=DATE,level='section',parent_code='',verification_status='official_label_only'))
    write_csv('registries/classification_master.csv',rows,fields=['system','version','code','label','definition','url','accessed_at','level','parent_code','verification_status'])
    write_csv('registries/classification_crosswalk.csv',[],fields=['from_system','from_version','from_code','to_system','to_version','to_code','verified','confidence','notes','url'])
    write_csv('registries/source_registry.csv',artifacts)
    write_csv('registries/industry_lesson_matrix.csv',[dict(lesson_id=f'{n:02}',reference_id='C_TW_SIC_11',reference_type='source',source_role='methodology',confidence='official source; detailed lesson code pending',verified_at=DATE if artifacts[0]['verification_status']!='unverified' else '',status='metadata') for n in range(50)])
    for n,title in enumerate(lessons()):
        p=R/f'notes/lessons/lesson-{n:02}/index.md';p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(f'# {n:02}｜{title}\n\nSourcing status: metadata。課名與號碼取自既有 docs/app.js；來源配對見矩陣。尚非正式講義。\n',encoding='utf-8')
    (R/'audit/phase-1.md').write_text(f'# Phase 1\n\n15 筆核心種子（含 1 管理文章及 1 學術專書，非 15 篇同行評審論文）；Crossref 核對成功 {sum(p["bibliographic_verified"]=="true" for p in papers)} 筆。50 課來源骨架；分類來源 {len(artifacts)} 個入口，分類列 {len(rows)}。\n\n未完成：完整活動定義、排除條款及官方 crosswalk 列解析由 Phase 4 繼續。台灣第11次為指定歷史版本，現行第12次另列版本差異；ISIC Rev.5 已獲 UN 通過，出版狀態依官方頁。\n',encoding='utf-8')
    flush_log()

DATASETS=[
('G_WDI','World Bank','World Development Indicators','https://data.worldbank.org/','Global','GDP/sector value added','current or constant USD, %; by series','by series','annual',list(range(5))+[48,49]),
('G_TIVA','OECD','Trade in Value Added','https://www.oecd.org/en/topics/sub-issues/trade-in-value-added.html','Global','domestic/foreign value added in trade','USD million or %; by measure','current prices','annual',[2,4,10,11,12,13,14,15,16,17,18,19,20,21,25,26,48,49]),
('G_COMTRADE','UN Statistics','UN Comtrade','https://comtradeplus.un.org/','Global','merchandise exports/imports by HS','USD and quantity separately','nominal','annual/monthly',[2]+list(range(5,22))+[25,26,43]),
('G_FAO','FAO','FAOSTAT','https://www.fao.org/faostat/en/','Global','agricultural production/trade','tonnes, USD; separate domains','by series','annual',[5,6,10]),
('G_FISH','FAO','FishStat fisheries and aquaculture','https://www.fao.org/fishery/en/statistics','Global','capture/aquaculture output','tonnes live weight; by table','not_applicable','annual',[6]),
('G_USGS','US Geological Survey','Mineral Commodity Summaries 2025','https://pubs.usgs.gov/publication/mcs2025','Global','mineral production/reserves','commodity-specific tonnes and values','by table','annual',[7,14,25,47]),
('G_IEA','IEA','Energy statistics and data','https://www.iea.org/data-and-statistics','Global','energy balances/generation/capacity','TJ, GWh, MW separately','not_applicable','annual/monthly',[8,9,16,24,25,47]),
('G_UNIDO','UNIDO','Industrial Statistics Databases','https://stat.unido.org/','Global','manufacturing output/value added/employment','national currency, USD, persons; separate','by measure','annual',list(range(10,22))+[25,26,43]),
('G_STAN','OECD','Structural Analysis Database','https://www.oecd.org/en/data/datasets/structural-analysis-database.html','Global','industry output/value added/employment','by series','by series','annual',list(range(10,22))+[25,26]),
('G_ITU','ITU','ICT DataHub','https://datahub.itu.int/','Global','ICT access/use/subscriptions','persons, subscriptions, percentages','not_applicable','annual',[22,23,24,33,37,38]),
('G_OICA','OICA','Production Statistics','https://www.oica.net/category/production-statistics/','Global','motor vehicle production','vehicles','not_applicable','annual',[25]),
('G_TRANSPORT','International Transport Forum OECD','Transport statistics','https://www.itf-oecd.org/transport-statistics','Global','transport volumes','tonne-km, passenger-km separately','not_applicable','annual',[26,27]),
('G_UNCTAD','UNCTAD','Data Hub','https://unctadstat.unctad.org/','Global','maritime trade, investment and services','by series','by series','annual',[2,27,30,48,49]),
('G_ILOSTAT','ILO','ILOSTAT data','https://ilostat.ilo.org/data/','Global','employment by economic activity','persons, hours, rates separately','not_applicable','annual/quarterly',list(range(28,47))),
('G_BIS','Bank for International Settlements','BIS Data Portal','https://data.bis.org/','Global','banking, credit and property prices','currency, ratios and indices separately','by series','quarterly/monthly',[29,31,32]),
('G_IMF','IMF','IMF Data','https://data.imf.org/','Global','financial and macroeconomic statistics','by series','by series','monthly/quarterly',[1,31,32,49]),
('G_BEA','BEA','GDP by Industry','https://www.bea.gov/data/gdp/gdp-industry','United States','industry gross output/value added','USD or chained index; separate','current/real separately','quarterly/annual',list(range(5))+list(range(28,42))+[45,48,49]),
('G_CBP','US Census','County Business Patterns','https://www.census.gov/programs-surveys/cbp.html','United States','establishments/employment/payroll','establishments/persons/USD','nominal payroll','annual',[28,29,30,33,34,35,36,37,38,39,40,41,45]),
('G_UIS','UNESCO','UIS Data Browser','https://databrowser.uis.unesco.org/','Global','education/cultural participation','persons, expenditure, rates; by indicator','by series','annual',[37,39,44]),
('G_TOURISM','UN Tourism','Tourism Statistics Database','https://www.unwto.org/tourism-statistics/tourism-statistics-database','Global','visitor arrivals/tourism expenditure','arrivals or currency; separate','by series','annual/monthly',[40,41]),
('G_WHO','WHO','Global Health Observatory','https://www.who.int/data/gho','Global','health resources, delivery and outcomes','persons, beds, ratios; by indicator','not_applicable','annual',[42,43]),
('G_TRIALS','US National Library of Medicine','ClinicalTrials.gov','https://clinicaltrials.gov/data-api/api','Global','registered clinical trials','trials; not market size','not_applicable','continuous',[43]),
('G_PROCURE','WTO','Government Procurement Agreement','https://www.wto.org/english/tratop_e/gproc_e/gp_gpa_e.htm','Global','covered public procurement and statistical reporting','by member report; scope differs','nominal','annual',[46]),
('T_DGBAS','行政院主計總處','國民所得與統計資料庫','https://nstatdb.dgbas.gov.tw/dgbasall/webMain.aspx?sys=100&funid=defjsp','Taiwan','產業附加價值、GDP、就業','TWD million, persons; 按表分開','名目／實質分列','annual/quarterly',list(range(5))+list(range(28,50))),
('T_MOEA','經濟部統計處','產業經濟統計','https://www.moea.gov.tw/Mns/dos/home/Home.aspx','Taiwan','工業生產、銷售、商業營收','指數、TWD；按統計表','名目營收／實質生產指數分列','monthly',list(range(10,22))+[23,24,25,26,30,33,35,36,38,41,43]),
('T_TRADE','財政部關務署','海關進出口統計','https://portal.sw.nat.gov.tw/APGA/GA30','Taiwan','HS進出口額及數量','USD/TWD/quantity；分開','nominal','monthly',list(range(5,22))+[25,26,43]),
('T_AGRI','農業部','農業統計資料查詢','https://agrstat.moa.gov.tw/sdweb/public/book/Book.aspx','Taiwan','農林漁牧生產量值','公噸、TWD；分開','名目產值','annual',[5,6,10]),
('T_FISH','農業部漁業署','漁業統計','https://www.fa.gov.tw/','Taiwan','捕撈與養殖產量值','公噸、TWD；分開','nominal value','annual',[6]),
('T_MINERAL','經濟部地質調查及礦業管理中心','礦產統計','https://www.gsmma.gov.tw/','Taiwan','礦產生產與供應','各礦種單位；逐表確認','by table','annual',[7]),
('T_ENERGY','經濟部能源署','能源統計資訊系統','https://www.esist.org.tw/','Taiwan','能源供需平衡、發電及裝置容量','熱值、GWh、MW；分開','not_applicable','monthly/annual',[8,9,16,24,25,47]),
('T_ENV','環境部','環境統計查詢網','https://stat.moenv.gov.tw/','Taiwan','廢棄物處理與排放','公噸、CO2e；口徑分開','not_applicable','annual',[9,13,14,47]),
('T_NCC','國家通訊傳播委員會','通訊傳播統計','https://www.ncc.gov.tw/chinese/','Taiwan','電信訂戶、通訊服務','戶數／營收；逐表確認','by series','quarterly',[22,23,24,37]),
('T_MOTC','交通部','交通統計查詢網','https://stat.motc.gov.tw/mocdb/stmain.jsp?sys=100','Taiwan','運量、運能、運輸營運','人次、噸公里、車輛；分開','not_applicable','monthly/annual',[25,26,27]),
('T_MOI','內政部','不動產資訊平台','https://pip.moi.gov.tw/','Taiwan','住宅價格、租賃、建設','TWD、戶、坪；逐表確認','nominal prices','monthly/quarterly',[28,29]),
('T_FSC','金融監督管理委員會','金融統計','https://www.fsc.gov.tw/ch/home.jsp?id=192&parentpath=0,6','Taiwan','金融機構資產、保費、證券交易','TWD；存量與流量分開','nominal','monthly',[31,32]),
('T_CBC','中央銀行','金融統計資料庫','https://statdb.cbc.gov.tw/','Taiwan','匯率、信貸、金融部門','TWD per currency、TWD；分開','nominal','daily/monthly',[1,2,31,32,49]),
('T_LABOR','勞動部','勞動統計查詢網','https://statfy.mol.gov.tw/','Taiwan','行業就業、薪資、工時','人、TWD、時數；分開','nominal wages','monthly/annual',[34,35,36,45]),
('T_CULTURE','文化部','文化統計','https://stat.moc.gov.tw/','Taiwan','文化產業與參與','產值、家數、人次；分開','by series','annual',[33,37,38,39]),
('T_TOURISM','交通部觀光署','觀光統計資料庫','https://stat.taiwan.net.tw/','Taiwan','旅客、旅宿、觀光支出','人次、間、TWD；分開','nominal spending','monthly',[39,40,41]),
('T_HEALTH','衛生福利部','衛生福利統計專區','https://dep.mohw.gov.tw/DOS/','Taiwan','醫療資源、健康支出、社福','人、床、TWD；分開','by series','annual',[42,43,45]),
('T_TFDA','衛生福利部食品藥物管理署','藥物與醫材統計','https://www.fda.gov.tw/','Taiwan','許可證、審查、製藥監管','件數；不是銷售或市場規模','not_applicable','annual',[43]),
('T_EDU','教育部','教育統計查詢網','https://stats.moe.gov.tw/','Taiwan','學校、學生與教育經費','校、人、TWD；分開','by series','academic year',[44]),
('T_PROCURE','行政院公共工程委員會','政府電子採購網','https://web.pcc.gov.tw/','Taiwan','政府採購決標與公告','TWD、案數；非一般產業總營收','nominal','continuous',[28,35,46]),
]
def phase2():
    sources=read_csv('registries/source_registry.csv');matrix=read_csv('registries/industry_lesson_matrix.csv')
    def one(item):
        sid,agency,name,url,geo,measure,unit,real,freq,ids=item
        data,log=fetch(url,sid)
        return dict(source_id=sid,agency=agency,dataset=name,measure=measure,definition='官方統計／資料庫入口；須選取具體指標、活動分類與分母後方可跨國比較',unit=unit,nominal_real=real,geography=geo,frequency=freq,coverage='依資料表及版本；尚未認定為完整時間序列',update_frequency=freq,url=url,license='dataset-specific; redistribution not assumed',access_status=log['status'],lesson_ids=';'.join(f'{n:02}' for n in ids),downloaded_on=DATE if data else '',verification_status='landing_retrieved' if data else 'unverified')
    with ThreadPoolExecutor(max_workers=4) as ex:new=list(ex.map(one,DATASETS))
    sources+=new
    for row in new:
        for lid in row['lesson_ids'].split(';'):
            matrix.append(dict(lesson_id=lid,reference_id=row['source_id'],reference_type='source',source_role='taiwan' if row['geography']=='Taiwan' else 'global',confidence='official agency candidate; numerical comparability pending',verified_at=DATE if row['verification_status']=='landing_retrieved' else '',status='metadata'))
    write_csv('registries/source_registry.csv',sources);write_csv('registries/industry_lesson_matrix.csv',matrix)
    definitions=[('revenue','營收','企業銷售商品與服務的收入；依會計合併範圍','currency/period','flow','企業／集團；不能直接代表產業規模'),('gross_output','產值／總產出','生產活動總產出，包含中間投入價值','currency/period','flow','場所／行業；價值鏈加總可能重複計算'),('value_added','附加價值','總產出減中間消費；依國民帳定義','currency/period','flow','行業；基本價格與市場價格要區分'),('gdp_share','GDP貢獻','行業附加價值相對GDP的比率；分子分母價格基準須相容','percent','ratio','經濟體；不可用營收除GDP冒充'),('exports','出口額','跨境貨品或服務流量；HS與活動分類非同一系統','currency/period','flow','海關領域／國際收支；FOB與CIF分開'),('market_cap','市值','特定估值日股價乘流通股數','currency/date','stock','上市企業；不等於產值或銷售'),('capacity','產能','期間內在特定條件下的最大可生產量','physical unit/period','capacity','設施／製程；不等於實際產量'),('market_size','市場規模','須定義產品、地區、期間與交易層級；可能為支出或銷售','currency/period','flow','產品市場；預測與實績分列'),('employment','就業','依人數／職位／全時當量及主要活動分類','persons/jobs/FTE','stock or average','不可混用人數與職位數'),('exchange_rate','匯率','一單位外幣對本幣；均價與期末匯價分列','local per foreign','price','換算流量常用期間均價，存量常用期末價；依問題定義')]
    write_csv('registries/indicator_dictionary.csv',[dict(indicator_id=i,label=l,definition=d,unit=u,stock_flow=s,scope_and_caution=c,required_metadata='currency;geography;period;nominal_real;statistical_unit;retrieved_at;forecast_or_actual') for i,l,d,u,s,c in definitions])
    complete=sum(all(any(r['lesson_id']==f'{n:02}' and r['source_role']==role for r in matrix) for role in ['global','taiwan']) for n in range(50))
    (R/'audit/phase-2.md').write_text(f'# Phase 2\n\n新增 {len(new)} 個官方統計入口；{sum(r["verification_status"]=="landing_retrieved" for r in new)} 個 HTTP 內容可取回。50 課中 {complete} 課已配對全球與台灣入口。這是來源索引覆蓋，不是已取得可直接比較的50組數值。\n\n新增指標字典 10 筆，嚴格區分營收、產值、附加價值、GDP貢獻、出口、市值、產能與市場規模。所有單位／資料期間仍須按實際表核對。受限或失效入口見 download_log，國際資料庫可能不納入台灣，不能用中國資料取代。\n',encoding='utf-8');flush_log()

SUPPLEMENTS=[
('The Nature of the Firm','TCE','組織邊界與市場協調成本',[0,1,3,4,28,34,35,36,45,48,49]),
('The Simple Economics of Artificial Intelligence','AI economics','預測成本下降與互補決策',[24]),
('The Economics of Two-Sided Markets','Platform economics','平台跨邊外部性與參與誘因',[22,23,24,30,33,37,38,40,41]),
('Contract farming in developing countries: a review','Agricultural contracts','契作治理、風險分配與農戶選擇',[5,10]),
('The tragedy of the commons','Common pool resources','共享資源的私人成本與集體外部性',[6,9,46]),
('The Economics of Resources or the Resources of Economics','Resource economics','耗竭資源與跨期選擇',[7,8]),
('A theory of regulatory capture','Regulation','受管制企業與監管資訊不對稱',[9,31,32,46,47]),
('The Governance of Global Value Chains','GVC','供應商能力、可編碼性與治理',[10,11,12,13,14,15,16,17,20,21,25,26,27]),
('How Does Learning Happen? Understanding the Knowledge-Creation Process','Learning','知識創造與學習',[15,17,19,35]),
('The Dynamics of Product Innovation and Firm Competences','Innovation','產品架構與企業能力演化',[16,18,19,20,21,25,26]),
('The Competitive Advantage of Interconnected Firms: An Extension of the Resource-Based View','Networks','網絡資源與互補',[17,22,27,35,48]),
('Dynamic Returns in Imperfectly Competitive Markets','Learning curves','累積產量、學習與動態競爭',[18,19]),
('System competition and network effects','Network effects','相容性、標準與網路外部性',[21,22,23,24,38]),
('The Value of Corporate Real Estate Assets: An Empirical Investigation','Real estate','資產配置與企業價值；書目候選需讀全文',[28,29]),
('Banking, Liquidity, and Bank Runs in an Infinite Horizon Economy','Financial intermediation','流動性轉換與擠兌',[31]),
('The market for lemons quality uncertainty and the market mechanism','Information asymmetry','品質不確定性與逆向選擇',[30,32,34,35,42,43,44,45]),
('Advertising as a signal of product quality','Signaling','廣告投入與品質訊號',[33,37]),
('The Strength of Weak Ties','Social networks','橋接關係與非冗餘資訊',[34,36,48]),
('Creative Industries: Contracts Between Art and Commerce','Creative industries','創意品不確定性與契約協調',[37,38,39]),
('Tourism and economic growth: a panel data analysis for the period 1990–2011','Tourism economics','旅遊與成長關聯；不能直接視為因果',[39,40]),
('Plural forms of governance: A review and research agenda','Franchising governance','自營與加盟並存的誘因與監督',[30,41,45]),
('Uncertainty and the Welfare Economics of Medical Care','Health economics','醫療不確定性、資訊與保險制度',[42,43]),
('The Rate and Direction of Inventive Activity: Economic and Social Factors','Innovation economics','研究投入與創新誘因；專書需另辨識',[43]),
('Investment in Human Capital','Human capital','教育投資與生產力；選擇效果另辨識',[44]),
('Public Procurement for Innovation as mission-oriented innovation policy','Public procurement','公共需求與創新方向',[46]),
('Toward a New Conception of the Environment-Competitiveness Relationship','Environmental innovation','環境管制、創新補償與條件',[9,13,14,16,25,47]),
('Diversification Strategy and Profitability','Diversification','多角化範圍與績效；內生性需處理',[48,49]),
('Supply Chain Decoupling: Geopolitical Debates and Economic Dynamism in East Asia','Geopolitical risk','重組、區域分工與貿易風險',[2,7,8,11,18,19,20,25,27,47,49])]

COMPANIES=[
('Nestle','NESN','https://www.nestle.com/investors/annual-report','Global',[1,5,10]),
('Mowi','MOWI','https://mowi.com/investors/reports/','Global',[6]),
('BHP','BHP','https://www.bhp.com/investors/annual-reporting','Global',[7,14]),
('Shell','SHEL','https://www.shell.com/investors/results-and-reporting/annual-report.html','Global',[8]),
('National Grid','NG','https://www.nationalgrid.com/investors/annual-reports-and-accounts','Global',[9,47]),
('Nike','NKE','https://investors.nike.com/investors/news-events-and-reports/default.aspx','Global',[11,39]),
('International Paper','IP','https://internationalpaper2022rd.q4web.com/investors/financials/annual-reports-and-proxy/default.aspx','Global',[12]),
('BASF','BAS','https://report.basf.com/2024/en/','Global',[13]),
('Caterpillar','CAT','https://www.caterpillar.com/en/investors/financial-information/annual-report.html','Global',[15]),
('Siemens','SIE','https://www.siemens.com/global/en/company/investor-relations/annual-reports.html','Global',[16,35]),
('SKF','SKF','https://investors.skf.com/en/financial-reports','Global',[17]),
('Intel','INTC','https://www.intc.com/filings-reports/annual-report','Global',[18]),
('ASML','ASML','https://www.asml.com/en/investors/annual-report','Global',[19]),
('Flex','FLEX','https://investors.flex.com/financials/annual-reports-and-proxy/default.aspx','Global',[20]),
('Apple','AAPL','https://investor.apple.com/sec-filings/default.aspx','Global',[0,4,21]),
('Vodafone','VOD','https://investors.vodafone.com/reports-information/annual-reports','Global',[22]),
('Microsoft','MSFT','https://www.microsoft.com/en-us/Investor/annual-reports.aspx','Global',[23,24]),
('Toyota','7203','https://global.toyota/en/ir/library/annual/','Global',[25]),
('Airbus','AIR','https://www.airbus.com/en/investors/financial-results-annual-reports','Global',[26]),
('Maersk','MAERSK','https://investor.maersk.com/financials/annual-reports','Global',[2,27]),
('Vinci','DG','https://www.vinci.com/en/finance/financial-information/annual-reports','Global',[28]),
('CBRE','CBRE','https://ir.cbre.com/financial-reports/annual-reports-and-proxy-statements','Global',[29]),
('Walmart','WMT','https://stock.walmart.com/financials/annual-reports/default.aspx','Global',[3,30]),
('JPMorgan Chase','JPM','https://www.jpmorganchase.com/ir/annual-report','Global',[31,32]),
('WPP','WPP','https://www.wpp.com/investors/annual-report','Global',[33]),
('Accenture','ACN','https://investor.accenture.com/financials/annual-reports/default.aspx','Global',[34]),
('Adecco','ADEN','https://www.adeccogroup.com/investors/financial-news/financial-results','Global',[36]),
('Disney','DIS','https://thewaltdisneycompany.com/investor-relations/','Global',[37,38]),
('Marriott','MAR','https://marriott.gcs-web.com/financial-information/annual-reports','Global',[40]),
('McDonalds','MCD','https://corporate.mcdonalds.com/corpmcd/investors/financial-information.html','Global',[41]),
('HCA Healthcare','HCA','https://investor.hcahealthcare.com/financials/annual-reports-and-proxy/default.aspx','Global',[42]),
('Pfizer','PFE','https://investors.pfizer.com/Investors/Financials/Annual-Reports/default.aspx','Global',[43]),
('Pearson','PSON','https://plc.pearson.com/en-GB/investors/annual-reports','Global',[44]),
('Service Corporation International','SCI','https://investors.sci-corp.com/financial-information/annual-reports','Global',[45]),
('Lockheed Martin','LMT','https://www.lockheedmartin.com/en-us/investor-relations/annual-reports.html','Global',[46]),
('Berkshire Hathaway','BRK','https://www.berkshirehathaway.com/reports.html','Global',[48,49]),
('統一企業','1216','https://www.uni-president.com.tw/','Taiwan',[1,5,10,30]),
('大成長城','1210','https://www.dachan.com/','Taiwan',[6]),
('亞洲水泥','1102','https://www.acc.com.tw/','Taiwan',[7,14]),
('台灣中油','','https://www.cpc.com.tw/','Taiwan',[8]),
('台灣電力','','https://www.taipower.com.tw/','Taiwan',[9,47]),
('儒鴻','1476','https://www.eclat.com.tw/','Taiwan',[11]),
('永豐餘','1907','https://www.yfy.com/','Taiwan',[12]),
('台塑','1301','https://www.fpc.com.tw/','Taiwan',[13]),
('上銀','2049','https://www.hiwin.tw/','Taiwan',[15,17]),
('東元','1504','https://www.teco.com.tw/','Taiwan',[16,35]),
('台積電','2330','https://investor.tsmc.com/english/annual-reports','Taiwan',[0,2,3,4,18,19]),
('鴻海','2317','https://www.foxconn.com/en-us/investor-relations/annual-reports','Taiwan',[20,48]),
('華碩','2357','https://www.asus.com/EVENT/Investor/','Taiwan',[21]),
('中華電信','2412','https://www.cht.com.tw/en/home/cht/investors/financials/annual-reports','Taiwan',[22]),
('叡揚','6752','https://www.gss.com.tw/','Taiwan',[23]),
('緯穎','6669','https://www.wiwynn.com/','Taiwan',[24]),
('裕隆','2201','https://www.yulon-motor.com.tw/','Taiwan',[25]),
('漢翔','2634','https://www.aidc.com.tw/','Taiwan',[26]),
('長榮海運','2603','https://www.evergreen-marine.com/','Taiwan',[27]),
('中鼎','9933','https://www.ctci.com/','Taiwan',[28,35]),
('信義房屋','9940','https://www.sinyi.com.tw/','Taiwan',[29]),
('國泰金控','2882','https://www.cathayholdings.com/','Taiwan',[31,32]),
('聯廣','8497','https://www.ucgroup.com.tw/','Taiwan',[33]),
('勤業眾信','','https://www.deloitte.com/tw/zh.html','Taiwan',[34]),
('中保科','9917','https://www.secom.com.tw/','Taiwan',[36]),
('東森國際','2614','https://www.emic.com.tw/','Taiwan',[37]),
('遊戲橘子','6180','https://www.gamania.com/','Taiwan',[38]),
('巨大','9921','https://www.giantgroup-cycling.com/','Taiwan',[39]),
('晶華','2707','https://www.fihregent.com/','Taiwan',[40]),
('王品','2727','https://www.wowprime.com/','Taiwan',[41]),
('長庚醫療財團法人','','https://www.cgmh.org.tw/','Taiwan',[42]),
('保瑞','6472','https://www.bora-corp.com/','Taiwan',[43]),
('志光數位','8068','https://www.public.com.tw/','Taiwan',[44]),
('龍巖','5530','https://www.lyls.com.tw/','Taiwan',[45]),
('漢翔','2634','https://www.aidc.com.tw/','Taiwan',[46]),
('遠東新世紀','1402','https://www.fenc.com/','Taiwan',[48,49])]

def phase3():
    papers=read_csv('registries/literature_master.csv');matrix=read_csv('registries/industry_lesson_matrix.csv')
    # 僅對失敗書目作一次低頻重試；不反覆撞擊付費平台。
    for i,row in enumerate(papers):
        if row['doi'] and row['bibliographic_verified']!='true':papers[i]=paper_metadata(CORE[i])
    query_audit=[]
    for title,theory,mechanism,ids in SUPPLEMENTS:
        time.sleep(1.2)
        url='https://api.crossref.org/works?query.title='+quote(title)+'&rows=1'
        data,log=fetch(url,'query_'+hashlib.sha256(title.encode()).hexdigest()[:10],'json')
        match=None;score=0
        if data:
            items=json.loads(data)['message']['items']
            if items:
                match=items[0];found=' '.join(match.get('title',[]))
                norm=lambda x:re.sub(r'[^a-z0-9]','',x.lower())
                score=difflib.SequenceMatcher(None,norm(title),norm(found)).ratio()
        accepted=bool(match and score>=0.90)
        query_audit.append(dict(query_title=title,metadata_url=url,candidate_title=' '.join(match.get('title',[])) if match else '',doi=match.get('DOI','') if match else '',match_similarity=round(score,4),accepted=str(accepted).lower(),lesson_ids=';'.join(f'{n:02}' for n in ids),notes='字面比對只核對書目候選，不代表內容適用或全文查證'))
        if not accepted:continue
        doi=match['DOI'].lower()
        existing=next((p for p in papers if p['doi'].lower()==doi),None)
        if existing:
            existing['lesson_ids']=';'.join(sorted(set(existing['lesson_ids'].split(';')+ [f'{n:02}' for n in ids])- {''}))
        else:
            row=paper_metadata((title,doi,theory,mechanism));row['lesson_ids']=';'.join(f'{n:02}' for n in ids);papers.append(row)
    # 逐課指定核心機制與補充，不把含關鍵字視為已讀實證。
    core_map=[3,4,5,1,4,4,4,4,4,4,5,5,5,6,6,7,7,13,9,6,5,7,12,12,11,7,13,5,4,4,12,4,4,12,3,8,14,12,12,3,12,4,4,6,8,4,4,11,13,9]
    for n,pnum in enumerate(core_map):
        p=papers[pnum-1];p['lesson_ids']=';'.join(sorted(set(p['lesson_ids'].split(';')+[f'{n:02}'])-{''}))
        for extra in ([9,14] if n<5 or n==49 else [3]):
            p=papers[extra-1];p['lesson_ids']=';'.join(sorted(set(p['lesson_ids'].split(';')+[f'{n:02}'])-{''}))
    for p in papers:
        for lid in filter(None,p['lesson_ids'].split(';')):
            matrix.append(dict(lesson_id=lid,reference_id=p['paper_id'],reference_type='paper',source_role='theory',confidence='curated theoretical applicability; fulltext review pending',verified_at=DATE if p['bibliographic_verified']=='true' else '',status='metadata'))
    write_csv('registries/literature_master.csv',papers);write_csv('audit/literature_search_log.csv',query_audit)
    filings=[]
    for idx,(issuer,ticker,url,geo,ids) in enumerate(COMPANIES):
        fid=f'F{idx+1:03}'
        filings.append(dict(filing_id=fid,issuer=issuer,identifier='',ticker=ticker,fiscal_year='',reporting_currency='',audited='',source_url=url,filing_date='',geography=geo,lesson_ids=';'.join(f'{n:02}' for n in ids),status='candidate_ir_hub',notes='公司一手候選入口；未取得年度文件前不宣稱已核對財報、財年、幣別或查核意見'))
        for n in ids:matrix.append(dict(lesson_id=f'{n:02}',reference_id=fid,reference_type='filing',source_role='firm',confidence='candidate official issuer; comparable scope pending',verified_at='',status='metadata'))
    write_csv('registries/company_filings.csv',filings);write_csv('registries/industry_lesson_matrix.csv',matrix)
    (R/'audit/phase-3.md').write_text(f'# Phase 3\n\n書目 {len(papers)} 筆；新增產業主題檢索 {len(query_audit)} 筆，接受精確／近精確書名 {sum(x["accepted"]=="true" for x in query_audit)} 筆，其餘保留失配原因與原查詢。全球／台灣公司候選入口 {len(filings)} 筆。矩陣逐課明列書目與公司，非僅長文字描述。\n\n待補：部分課仍僅共用理論、特定產業實證不足；公司入口不是年報本身，Phase 4 取回年度文件才提升狀態。未上市專業服務、教育與公共行政不強行假設有可比上市公司。\n',encoding='utf-8');flush_log()

if __name__=='__main__':
    globals()['phase'+sys.argv[1]]()
