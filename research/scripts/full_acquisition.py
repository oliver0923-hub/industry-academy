"""50課來源盤點與有界續跑。原文僅在private_sources；網頁資料不作操作指令。"""
import argparse,csv,hashlib,io,json,re,time,zipfile,sys
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode,urljoin,unquote
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
import acquire as a

ROOT=a.ROOT; R=a.R; B=R/'audit/full-acquisition-v2'; PRIVATE=a.PRIVATE/'full-v2'
NOW=lambda:datetime.now(timezone.utc).isoformat(timespec='seconds')
STATE=R/'sources/acquisition_state.csv'; TASKS=R/'sources/acquisition_tasks.csv'
SUCCESS={'downloaded','reused_existing','cached_verified'}
GAPS=[
'TW12活動定義與證交所索引差異；統計單位逐例定位',
'同表總產出與中間投入；企業收入到附加價值的調節',
'TiVA與FDI實際序列；增加值貿易與總額貿易區別',
'Bain/SCP原始實證、網絡效果與定價研究核讀',
'原文精確定位、MCD編碼損壞與財報口徑案例核對',
'台灣契作實證、農業修訂年鑑與集團產銷資料',
'台灣漁業及林業量值；兩版FAO年份與範圍調節',
'台灣礦種進口依賴與USGS礦種表逐值核對',
'台灣燃料平衡、煉製與石化用途資料及歷史',
'發電/燃氣/供水/廢棄物分開的台灣統計與監管歷史',
'食品加工與品牌製造原值、食品企業分部及衛生制度',
'紡織成衣鞋革分項產貿值、品牌/代工歷史與期刊',
'木材家具紙印刷分項統計、製程與台灣企業原文',
'基礎/特化/塑橡膠物量與原料投入；化工企業案例',
'鋼/非鐵/水泥/玻陶分項產能及能源成本原始資料',
'工具機訂單/產貿值與自動化採用；機器人論文方法核讀',
'電機/電纜/家電/能源設備分項量值與企業文件',
'精密零件與光學子產業邊界、原始企業和產業研究',
'設計/代工/記憶體/封測同年統計；TSMC會計差異調節',
'設備/材料/EDA分類、原始企業、專利與政策文本',
'EMS/ODM/OEM邊界與外部收入/內部交易調節',
'電腦/光電/顯示/感測/通訊設備分項統計與企業',
'台灣電信訂戶與營收、衛星及頻譜原始政策',
'軟體服務/雲端/SaaS收入分類、服務貿易與原始研究',
'算力與資料中心耗能/容量、平台收入範圍與政策',
'OICA失效連結替代、台灣汽車/電池/充電統計與原始財報',
'航太/船舶/鐵路/無人機各自官方資料與製造史',
'運輸方式別運量與運費；台灣物流、海空陸各自資料',
'工程承攬/營建量值、公共工程與原始企業風險揭露',
'不動產開發/租賃/仲介/物業分項統計及金融口徑',
'批零/電商營收與商品交易額分開；台灣通路案例',
'全球/台灣同口徑資產、銀行#註記、支付/金融科技研究',
'保險/證券/資管/PE分開的主管機關序列與期刊',
'代理商收入與平台廣告支出區別；市場研究及原始企業',
'顧問/法律/會計服務統計、監理制度與專業服務研究',
'工程設計/研發/檢測分項；原始合約與企業案例',
'派遣/招募/保全/清潔/客服分項、勞動制度與原始研究',
'出版/新聞/影視/音樂/串流各自量值；Disney受限替代',
'遊戲/電競/動畫/IP授權收入分項、原始平台與產業史',
'體育/藝文/博物館/休閒分項參與與收入、影像權利',
'台灣入境/旅宿/旅行社分項；觀光論文方法與期間核讀',
'加盟收入/系統銷售區分、MCD財表OCR及台灣餐飲案例',
'台灣院所/支付/照護原表、競爭review納入研究與識別',
'藥品/器材/CRO/CDMO分項、臨床試驗與主管機關文件',
'教育年度/學年區分、補教/職訓/EdTech資料與RCT核讀',
'美容/維修/洗衣/家事照護分項及非上市場所統計',
'公共採購金額/決標/預算分開；公共行政與國防邊界',
'能源轉型台灣實際容量/發電/碳排、礦物與供應鏈連結',
'控股/集團/總部統計、交易公告與多角化實證',
'全產業同口徑比較、危機時間線與企業配置原始證據']

def read(p):
    p=Path(p)
    return list(csv.DictReader(p.open(encoding='utf-8-sig',newline=''))) if p.exists() else []
def write(p,rows,fields=None):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    fields=fields or list(dict.fromkeys(k for r in rows for k in r))
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def sha(data):return hashlib.sha256(data).hexdigest()
def norm(url):
    s=urlsplit(url.strip());q=[(k,v) for k,v in parse_qsl(s.query,keep_blank_values=True) if not k.startswith('utm_') and k not in ['trk','fbclid']]
    return urlunsplit((s.scheme.lower(),s.netloc.lower(),unquote(s.path).rstrip('/'),urlencode(sorted(q)),''))
def safe(path):
    p=(ROOT/path).resolve()
    if not p.is_relative_to(ROOT.resolve()):raise ValueError('unsafe local_path')
    return p
def lesson_list():return [f'{i:02}' for i in range(50)]

# 直接文件或正式內容頁；網路回傳之前僅為identified，不能標示已存在或已讀。
# 產業映射是來源適用候選，並非這些課的主張已查核。
SEEDS=[
('TW12_META','行政院主計總處','行業統計分類XML詮釋資料','https://data.gov.tw/dataset/14321','html','classification','Taiwan','00-49','2026','2026-01-01 effective','政府資料開放授權條款1.0'),
('TW12_MANUAL','行政院主計總處','行業統計分類第12次修正','https://ws.dgbas.gov.tw/001/Upload/463/ebook/ebook_356166/pdf/full.pdf','pdf','classification','Taiwan','00-49','2026','2026 revision','官方文件；原文僅私存'),
('USGS26','USGS','Mineral Commodity Summaries2026','https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf','pdf','global','Global','07;14;19;25;47','2026','2025 estimates and historical series','USGS public domain subject to credited third-party material'),
('FAO_FISH24','FAO','SOFIA2024正式發布與統計摘要','https://www.fao.org/newsroom/detail/fao-report-global-fisheries-and-aquaculture-production-reaches-a-new-record-high/en','html','global','Global','06','2024','2022; stock sustainability2021','官方內容；不推定原圖重散布權'),
('FAO_FISH26','FAO','SOFIA2026正式發布','https://www.fao.org/newsroom/detail/sofia-2026--global-fisheries-and-aquaculture-production-reaches-new-highs/','html','global','Global','06','2026','2024 observations; confirm document','官方內容；原文僅私存'),
('IEA_GER25','IEA','Global Energy Review2025','https://iea.blob.core.windows.net/assets/5b169aa1-bc88-4c96-b828-aaa50406ba80/GlobalEnergyReview2025.pdf','pdf','global','Global','08;09;16;24;25;47','2025','2024','CC BY4.0 subject to report exceptions'),
('IEA_ELECTRICITY','IEA','GER2025 electricity chapter','https://www.iea.org/reports/global-energy-review-2025/electricity','html','global','Global','09;16;24;47','2025','2024','CC BY4.0 subject to exceptions'),
('EIA_OIL','US EIA','Oil and petroleum products explained','https://www.eia.gov/energyexplained/oil-and-petroleum-products/','html','history','United States','08;13;27','unknown','historical explanation; not current market series','US government; third-party images may differ'),
('WHO25','WHO / UN Digital Library','World health statistics2025','https://digitallibrary.un.org/record/4085690/files/9789240110496-eng.pdf','pdf','global','Global','42;43','2025','various years; table-specific','WHO license must be checked; local only'),
('WHO25_RELEASE','WHO','World health statistics2025發布','https://www.who.int/news/item/15-05-2025-who-warns-of-slowing-global-health-gains-in-new-statistics-report','html','global','Global','42;43','2025','various years','WHO copyright; local only'),
('MOHW113','衛生福利部','113年版衛生福利年報','https://www.mohw.gov.tw/cp-3196-79806-1.html','html','taiwan','Taiwan','42;43','2024','2024 edition; underlying year must be checked','官方內容；附件授權另核'),
('MOE_HIGHER113','教育部','113學年度大專校院概況統計電子書','https://stats.moe.gov.tw/bookcase/Higher/114/46/index.html','html','taiwan','Taiwan','44','2025','SY2024-2025; selected table page','官方統計；不可視為全冊已讀'),
('UNESCO_GEM24','UNESCO','Global Education Monitoring Report2024/5','https://www.unesco.org/gem-report/en/2024-leadership','html','global','Global','44','2024','report-specific','UNESCO terms; original private'),
('UNCTAD_MARITIME24','UNCTAD','Review of Maritime Transport2024','https://unctad.org/publication/review-maritime-transport-2024','html','global','Global','26;27','2024','2023/2024 report-specific','UN publication; original private'),
('OICA24','OICA','2024 production statistics','https://www.oica.net/category/production-statistics/2024-statistics/','html','global','Global','25','2025','2024','industry association; not government'),
('ITU24','ITU','Facts and Figures2024','https://www.itu.int/itu-d/reports/statistics/2024/11/10/ff24-internet-use/','html','global','Global','22;23;24;37;38','2024','2024 estimates','ITU copyright; private copy'),
('WIPO24','WIPO','World Intellectual Property Indicators2024','https://www.wipo.int/web-publications/world-intellectual-property-indicators-2024/en/','html','global','Global','15;17;19;23;35;38;43','2024','2023 applications; table-specific','WIPO license check before reuse of charts'),
('WTO24','WTO','Global Trade Outlook and Statistics2024','https://www.wto.org/english/res_e/booksp_e/trade_outlook24_e.pdf','pdf','global','Global','02;10;11;12;13;14;15;16;17;20;21;30;49','2024','2023 actual /2024 forecast separated','WTO report; original private'),
('ILO_SERVICES','ILO','World Employment and Social Outlook Trends2025','https://www.ilo.org/publications/flagship-reports/world-employment-and-social-outlook-trends-2025','html','global','Global','28;29;30;33;34;35;36;39;40;41;44;45;46','2025','report-specific','ILO report; original private'),
('OECD_TOUR24','OECD','Tourism Trends and Policies2024','https://www.oecd.org/en/publications/oecd-tourism-trends-and-policies-2024_80885d8b-en.html','html','global','Global','39;40;41','2024','report-specific','OECD license check'),
('TW_CULTURE','文化部','文化統計','https://stat.moc.gov.tw/','html','taiwan','Taiwan','33;37;38;39','unknown','dynamic portal; values not extracted','official portal; not a completed statistical series'),
('TW_ENERGY','經濟部能源署','能源統計資料查詢','https://www.esist.org.tw/','html','taiwan','Taiwan','08;09;16;24;25;47','unknown','dynamic portal','official portal; values pending'),
('TW_EDU','教育部','教育統計查詢網','https://stats.moe.gov.tw/','html','taiwan','Taiwan','44','unknown','dynamic portal','official portal'),
('TW_TOURISM','交通部觀光署','觀光統計資料庫','https://stat.taiwan.net.tw/','html','taiwan','Taiwan','39;40;41','unknown','dynamic portal','official portal'),
('TW_MOTC','交通部','交通統計資料查詢','https://stat.motc.gov.tw/mocdb/stmain.jsp?sys=100','html','taiwan','Taiwan','25;26;27','unknown','dynamic portal','official portal'),
('TW_LABOR','勞動部','勞動統計查詢','https://statfy.mol.gov.tw/','html','taiwan','Taiwan','34;35;36;45','unknown','dynamic portal','official portal'),
('TW_ENV','環境部','環境統計','https://stat.moenv.gov.tw/','html','taiwan','Taiwan','09;13;14;47','unknown','dynamic portal','official portal'),
('TW_HEALTH_STATS','衛生福利部','衛生福利統計專區','https://dep.mohw.gov.tw/DOS/lp-5099-113.html','html','taiwan','Taiwan','42;43','unknown','annual statistics portal','official portal'),
('FED_HISTORY','Federal Reserve History','Creation of the Federal Reserve','https://www.federalreservehistory.org/essays/founding-of-the-fed','html','history','United States','31;32;46','unknown','1913 event; confirm article date','Federal Reserve historical article; private original'),
('SMITHSONIAN_CHIP','Smithsonian','Integrated circuits','https://americanhistory.si.edu/collections/object/nmah_334900','html','history','United States','18;19;21','unknown','historical museum object; verify identity','museum image rights not assumed'),
('US_CENSUS_HISTORY','US Census','History of NAICS','https://www.census.gov/naics/','html','classification','United States','00-49','2022','NAICS versions separately','US government'),
('BLS_OES24','US BLS','May2024 national industry-specific occupational estimates','https://www.bls.gov/oes/2024/may/oessrci.htm','html','global','United States','28;29;30;33;34;35;36;37;38;39;40;41;42;44;45;46','2025','May2024; United States not global aggregate','US government'),
('TWSE_FILINGS','TWSE','上市公司每月營業收入 openAPI','https://openapi.twse.com.tw/v1/opendata/t187ap05_L','json','taiwan','Taiwan','10;11;12;13;14;15;16;17;18;19;20;21;25;26;28;29;30;32;33;35;36;37;38;39;40;41;43;45','unknown','API rows company/report year specific','政府資料開放授權條款1.0; verify API terms'),
('TWSE_MONTHLY','TWSE','上市公司月營收 openAPI','https://openapi.twse.com.tw/v1/opendata/t187ap05_L','json','taiwan','Taiwan','10;11;12;13;14;15;16;17;18;19;20;21;25;26;28;29;30;32;33;35;36;37;38;39;40;41;43;45','unknown','dynamic; same endpoint alias, identity to be checked','政府資料開放授權條款1.0'),
('FORD24','Ford Motor Company','Ford2024 annual report','https://s201.q4cdn.com/693218008/files/doc_financials/2024/ar/2024-annual-report.pdf','pdf','firm','Global','25','2025','FY2024','issuer annual report; private only'),
('MAERSK24','A.P. Moller-Maersk','Annual report2024','https://investor.maersk.com/static-files/edd017f9-1b91-4efb-b972-19806720e72c','pdf','firm','Global','27','2025','FY2024','issuer report; private only'),
('BERK24','Berkshire Hathaway','2024 annual report','https://www.berkshirehathaway.com/2024ar/2024ar.pdf','pdf','firm','Global','32;48','2025','FY2024','issuer annual report; private only'),
('MSFT24','Microsoft','2024 annual report','https://www.microsoft.com/investor/reports/ar24/index.html','html','firm','Global','23;24;48','2024','FY ended2024-06-30','issuer report; private only'),
]

def expand(s):
    if s=='00-49':return ';'.join(lesson_list())
    return s

def init():
    B.mkdir(parents=True,exist_ok=True);PRIVATE.mkdir(parents=True,exist_ok=True)
    tasks=read(TASKS);seen={norm(r['url']):r['task_id'] for r in tasks};aliases=[]
    for tag,issuer,title,url,fmt,role,country,lessons,year,period,license in SEEDS:
        urlkey=norm(url)
        if urlkey in seen:
            aliases.append(dict(alias='V2_'+tag,canonical=seen[urlkey],reason='same normalized URL; different labels do not imply different datasets'))
            continue
        tid='V2_'+tag;seen[urlkey]=tid
        tasks.append(dict(task_id=tid,source_id=tid,issuer=issuer,title=title,url=url,format=fmt,source_role=role,country=country,lesson_ids=expand(lessons),publication_date=year,data_period=period,license=license,content_kind='landing' if 'portal' in period else 'document',origin='curated public official/issuer seed; existence confirmed only after fetch'))
    write(TASKS,tasks)
    if aliases:write(B/'task_aliases.csv',aliases)
    # 已存在原始快取的URL索引只採成功記錄且檔案雜湊吻合。
    write(B/'input_status.csv',input_status())
    inventory('baseline_inventory.csv')
    materialize()

def input_status():
    results=[]
    for name in ['Industry_Academy_Codex_Full_Source_Acquisition_v2.md','Industry_Academy_Master_Instructions_v2.txt','Industry_Academy_Codex_Acquisition_Prompt_v1.txt','Industry_Academy_Editorial_Teaching_Standards_v1.0.txt']:
        p=Path.home()/'Downloads'/name;results.append(dict(input=name,path=str(p),status='read_available' if p.exists() else 'BLOCKED_INPUT',sha256=sha(p.read_bytes()) if p.exists() else '',notes='Actual attachment extension.md used despite request mentioning.txt' if name.endswith('_v2.md') else 'original retained'))
    desktop=Path.home()/'OneDrive/Desktop';zips=list(desktop.glob('Industry_Academy_研究資料_*.zip'))
    for p in zips:
        with zipfile.ZipFile(p) as z:
            bad=z.testzip();members=[x for x in z.infolist() if not x.is_dir()]
        results.append(dict(input='existing research ZIP',path=str(p),status='CRC_verified' if bad is None else 'corrupt_archive',sha256=sha(p.read_bytes()),notes=f'{len(members)} entries; no extraction or duplicate import; current repo/private originals reused'))
    if not zips:results.append(dict(input='existing research ZIP',path='',status='BLOCKED_INPUT',sha256='',notes='not available at known Desktop location; repo inventory continues'))
    return results

def artifacts():
    # 一份實體原始檔可對應多個URL；不把OCR/文字或API書目當期刊全文。
    logs=read(R/'audit/download_log.csv')+read(R/'audit/acquisition_attempts_v2.csv')
    invalid={norm(s['url']) for s in read(STATE) if s.get('parse_status')=='invalid_source_content'}
    bypath=defaultdict(list)
    for l in logs:
        path=l.get('local_path','')
        if path and l.get('status') in SUCCESS|{'cached_download'} and norm(l['url']) not in invalid:bypath[path].append(l)
    return bypath

def inventory(name):
    bypath=artifacts();rows=[];catalog=read(R/'sources/catalog.csv');byhash=defaultdict(list)
    for c in catalog:
        if c['sha256']:byhash[c['sha256']].append(c)
    for folder in ['private_sources','research']:
        for p in sorted((ROOT/folder).rglob('*')):
            if not p.is_file() or '__pycache__' in p.parts or p.is_relative_to(B):continue
            if p.name.endswith('_publish_bundle.json') or p.name=='manifest.csv':continue
            rel=p.relative_to(ROOT).as_posix();raw=p.read_bytes();links=bypath.get(rel,[])
            rows.append(dict(path=rel,filename=p.name,format=p.suffix.lstrip('.'),bytes=len(raw),sha256=sha(raw),title='; '.join(sorted({x.get('title',x.get('resource_id','')) for x in links})) or p.stem,origin_url='; '.join(sorted({x.get('url','') for x in links})),publication_year='unknown_not_inferred',data_period='unknown_not_inferred',license='; '.join(sorted({x.get('license','unknown') for x in links})) or 'unknown',download_date='; '.join(sorted({x.get('accessed_at',x.get('fetched_at','')) for x in links})),access_status='local_source_artifact' if links else 'derived_or_unlinked_file',verification_status='hash_inventoried_not_content_reviewed',applicable_lesson_ids=''))
            matched=byhash.get(rows[-1]['sha256'],[])
            if matched:
                for target,field in [('title','title'),('publication_year','publication_year'),('data_period','data_period'),('license','license'),('verification_status','source_status')]:rows[-1][target]='; '.join(sorted({c[field] for c in matched if c[field]})) or rows[-1][target]
                rows[-1]['applicable_lesson_ids']=';'.join(sorted({l for c in matched for l in c['lesson_ids'].split(';') if l}))
    write(B/name,rows)
    return rows

def inspect(data,fmt):
    if not data:raise ValueError('empty response')
    out=dict(pdf_pages='',text_chars='',parse_status='parsed',detected_title='')
    text=''
    if fmt=='pdf':
        if not data.startswith(b'%PDF'):raise ValueError('not PDF header; possible login/error HTML')
        pdf=PdfReader(io.BytesIO(data));out['pdf_pages']=len(pdf.pages)
        if not pdf.pages:raise ValueError('PDF has no pages')
        text='\n'.join(p.extract_text() or '' for p in pdf.pages)
        out['parse_status']='parsed_scan_needs_OCR' if len(text)<100 else 'parsed'
        controls=sum(ord(c)<32 and c not in '\n\r\t' for c in text)
        if controls/max(1,len(text))>0.02:out['parse_status']='parsed_text_encoding_issue_needs_OCR'
    elif fmt=='json':
        obj=json.loads(data);text=json.dumps(obj,ensure_ascii=False)
    elif fmt=='csv':
        text=data.decode('utf-8-sig');
        if text.lstrip().startswith('<'):raise ValueError('HTML returned instead of CSV')
        if not list(csv.reader(io.StringIO(text))):raise ValueError('CSV missing rows')
    else:
        text=data.decode('utf-8-sig','replace');s=BeautifulSoup(text,'html.parser')
        if s.title:out['detected_title']=s.title.get_text(' ',strip=True)
        if any(x in text[:180000].lower() for x in ['just a moment...','access denied','verify you are human','request unsuccessful','enable javascript and cookies']):raise ValueError('challenge/denial HTML')
        for tag in s(['script','style','nav','footer']):tag.decompose()
        text=s.get_text(' ',strip=True)
        if any(x in text[:1500].lower() for x in ['content not found','page not found','404 not found','找不到網頁','網頁不存在']):raise ValueError('soft404: readable error page, not source content')
        if len(text)<80:raise ValueError('HTML has insufficient readable content; SPA/login may require manual access')
    out['text_chars']=len(text)
    return out,text

def discover(args):
    """從已存官方HTML辨識附件，不對候選宣稱已取得或已讀。"""
    tasks=read(TASKS);known={norm(r['url']) for r in tasks};states={r['task_id']:r for r in read(STATE)};added=[]
    selected=set(lesson_list()) if args.lessons=='all' else set(args.lessons.split(','))
    for parent in list(tasks):
        st=states.get(parent['task_id'],{})
        if st.get('status') not in SUCCESS or parent['format']!='html' or parent['source_role'] in ['theory','bibliography'] or not(set(parent['lesson_ids'].split(';'))&selected):continue
        soup=BeautifulSoup(safe(st['local_path']).read_bytes(),'html.parser');count=0
        for link in soup.select('a[href]'):
            url=urljoin(parent['url'],link['href']);parts=urlsplit(url);path=parts.path.lower()
            if not url.startswith(('https://','http://')):continue
            fmt='pdf' if path.endswith('.pdf') else 'csv' if path.endswith('.csv') else 'json' if path.endswith('.json') else ''
            if not fmt or norm(url) in known:continue
            title=link.get_text(' ',strip=True) or link.get('title','') or Path(parts.path).name
            if any(k in title.lower() for k in ['privacy','cookie','logo','facebook']):continue
            tag='D_'+sha(norm(url).encode())[:12];known.add(norm(url));task={**parent,'task_id':tag,'source_id':tag,'url':url,'title':title[:240],'format':fmt,'content_kind':'document','origin':'attachment link in '+parent['task_id']+'; identity/date/lesson applicability require review','publication_date':'','data_period':'attachment-specific; not inherited from parent'};tasks.append(task);added.append(task);count+=1
            if count>=2 or len(added)>=args.max_files_per_run:break
        if len(added)>=args.max_files_per_run:break
    write(TASKS,tasks);write(B/'discovered_candidates.csv',added,fields=list(tasks[0]));materialize()
    print(json.dumps(dict(new_identified_candidates=len(added),downloaded_by_discovery=0,task_ids=[r['task_id'] for r in added])))

def run(args):
    tasks=read(TASKS);selected=set(args.lessons.split(',')) if args.lessons!='all' else set(lesson_list())
    tasks=[t for t in tasks if t.get('enabled','true')!='false' and set(t['lesson_ids'].split(';'))&selected and (not args.task_ids or t['task_id'] in args.task_ids.split(','))]
    state={r['task_id']:r for r in read(STATE)}
    # 從舊成功下載與本批已存內容查重；不再請求相同URL。
    byurl={}
    for rel,ls in artifacts().items():
        p=safe(rel)
        if not p.exists():continue
        digest=sha(p.read_bytes())
        for l in ls:
            if digest==l.get('sha256'):byurl[norm(l['url'])]=(p,l)
    attempts=read(R/'audit/acquisition_attempts_v2.csv');total=0;files=0;planned=[];robots={};last={};runid=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    def save():
        write(STATE,list(state.values()));write(R/'audit/acquisition_attempts_v2.csv',attempts)
    for task in tasks:
        tid=task['task_id'];previous=state.get(tid,{})
        if previous.get('status') in SUCCESS and args.skip_verified:
            p=safe(previous['local_path'])
            if p.exists() and sha(p.read_bytes())==previous['sha256']:continue
        if previous and previous.get('status') not in SUCCESS and not args.retry_failures:continue
        if files>=args.max_files_per_run or total>=args.max_bytes_per_run:break
        if args.dry_run:planned.append(task);files+=1;continue
        started=time.monotonic();base=dict(task_id=tid,resource_id=tid,source_id=task['source_id'],url=task['url'],title=task['title'],lesson_ids=task['lesson_ids'],fetched_at=NOW(),accessed_at=NOW()[:10],http_status='',content_type='',head_status='',head_mime='',head_bytes='',bytes=0,sha256='',local_path='',license=task['license'],error='',reason='',retry=0,elapsed=0,final_url='',status='',pdf_pages='',text_chars='',parse_status='',detected_title='')
        try:
            cached=byurl.get(norm(task['url']))
            if cached:
                p,l=cached;data=p.read_bytes();meta,text=inspect(data,task['format']);base.update(meta,status='reused_existing',bytes=len(data),sha256=sha(data),local_path=p.relative_to(ROOT).as_posix(),final_url=l.get('final_url',task['url']));state[tid]=base
            else:
                host=urlsplit(task['url']).netloc;origin=urlunsplit((urlsplit(task['url']).scheme,host,'','',''))
                if host not in robots:
                    u=origin+'/robots.txt';rr=requests.get(u,timeout=(8,20),headers={'User-Agent':'IndustryAcademyResearch/2.0'})
                    rp=RobotFileParser();rp.set_url(u)
                    if rr.status_code==200:rp.parse(rr.text.splitlines());robots[host]=rp
                    elif rr.status_code in [404,410]:robots[host]=None
                    elif rr.status_code in [401,403,429]:raise PermissionError('robots policy unavailable/denied: HTTP'+str(rr.status_code))
                    else:raise RuntimeError('robots policy temporary failure: HTTP'+str(rr.status_code))
                if robots[host] and not robots[host].can_fetch('IndustryAcademyResearch',task['url']):raise PermissionError('robots.txt disallows this path')
                crawl=robots[host].crawl_delay('*') if robots[host] else 0
                delay=max(args.rate_limit,float(crawl or 0));time.sleep(max(0,delay-(time.monotonic()-last.get(host,0))))
                headers={'User-Agent':'IndustryAcademyResearch/2.0 (personal scholarly source collection)'}
                h=requests.head(task['url'],allow_redirects=True,timeout=(8,25),headers=headers);base.update(head_status=h.status_code,head_mime=h.headers.get('Content-Type',''),head_bytes=h.headers.get('Content-Length',''))
                remaining=args.max_bytes_per_run-total
                if base['head_bytes'].isdigit() and int(base['head_bytes'])>min(remaining,args.max_file_bytes):raise OverflowError('HEAD size exceeds remaining/per-file byte budget')
                for retry in range(2):
                    response=requests.get(task['url'],stream=True,timeout=(8,30),headers=headers);base['retry']=retry
                    if response.status_code in [502,503,504] and retry==0:response.close();time.sleep(2);continue
                    break
                last[host]=time.monotonic();base.update(http_status=response.status_code,content_type=response.headers.get('Content-Type',''),final_url=response.url)
                response.raise_for_status();chunks=[];size=0
                for chunk in response.iter_content(65536):
                    size+=len(chunk)
                    if size>min(remaining,args.max_file_bytes):raise OverflowError('stream exceeds byte budget; partial bytes not saved')
                    chunks.append(chunk)
                response.close();data=b''.join(chunks);total+=size
                meta,text=inspect(data,task['format']);p=args.output_dir/(tid+'.'+task['format']);p.parent.mkdir(parents=True,exist_ok=True)
                if p.exists() and sha(p.read_bytes())!=sha(data):p=p.with_name(tid+'_'+sha(data)[:12]+'.'+task['format'])
                p.write_bytes(data);(p.with_suffix(p.suffix+'.text.txt')).write_text(text,encoding='utf-8')
                base.update(meta,status='downloaded',bytes=len(data),sha256=sha(data),local_path=p.relative_to(ROOT).as_posix());byurl[norm(task['url'])]=(p,base);state[tid]=base
        except Exception as e:
            code=str(base['http_status']);status='restricted' if code in ['401','403','429'] or isinstance(e,PermissionError) else 'broken' if code in ['404','410'] or 'soft404' in str(e) else 'budget_deferred' if isinstance(e,OverflowError) else 'failed'
            base.update(status=status,error=str(e)[:350],reason=str(e)[:350]);state[tid]=base
        finally:
            files+=1;base['elapsed']=round(time.monotonic()-started,3);base['attempt_id']=runid+'_'+str(len(attempts)+1);attempts.append(base);save()
            print(tid,base['status'],base['bytes'],flush=True)
    if args.dry_run:
        print(json.dumps(dict(dry_run=True,planned=len(planned),tasks=[r['task_id'] for r in planned]),ensure_ascii=False));return
    # 舊下載索引為latest view；完整每次嘗試保存在append-only v2 log。
    logs=a.read_csv('audit/download_log.csv');keys={(r['resource_id'],r['url']):r for r in logs}
    for row in state.values():keys[(row['resource_id'],row['url'])]={**row,'status':'downloaded' if row['status'] in SUCCESS else row['status']}
    a.write_csv('audit/download_log.csv',list(keys.values()))
    (B/'checkpoint.json').write_text(json.dumps(dict(run_id=runid,finished_at=NOW(),attempts_this_run=files,new_download_bytes=total,total_state_rows=len(state),running_in_background=False),indent=2),encoding='utf-8')
    materialize()

def materialize():
    B.mkdir(parents=True,exist_ok=True)
    tasks=read(TASKS);state={r['task_id']:r for r in read(STATE)}
    # 遷移只追加欄位，不改舊主鍵。對未確認資料明確留空。
    migration=[]
    extensions={
    'source_registry':['issuer','title','source_type','primary_vs_secondary','doi','publication_date','data_period','country','indicators','local_path','sha256','fetched_at','last_checked'],
    'literature_master':['abstract','oa_status','local_path','sha256','fetched_at','last_checked'],
    'company_filings':['local_path','sha256','fetched_at','last_checked','event_date','source_date','evidence_vs_interpretation'],
    'industry_lesson_matrix':['source_id','section_topic','evidence_claim_id','verification_status','last_checked']}
    for table,fields in extensions.items():
        rows=read(R/'registries'/f'{table}.csv');oldfields=list(rows[0])
        for row in rows:
            for f in fields:row.setdefault(f,'')
            if table=='source_registry':
                row.update(issuer=row.get('issuer') or row['agency'],title=row.get('title') or row['dataset'],source_type=row.get('source_type') or ('classification' if row['source_id'].startswith('C_') else 'official_portal'),primary_vs_secondary=row.get('primary_vs_secondary') or 'agency_original_portal_not_observations',country=row.get('country') or row['geography'],indicators=row.get('indicators') or row['measure'])
            elif table=='industry_lesson_matrix':row.update(source_id=row.get('source_id') or row['reference_id'],verification_status=row.get('verification_status') or row['status'])
        migration.append(dict(table=table,added_fields=';'.join(f for f in fields if f not in oldfields),preservation='legacy keys/columns retained; blank is unknown; no old reading status promoted'))
        a.write_csv('registries/'+table+'.csv',rows)
    prior=B/'schema_migration.csv'
    if not prior.exists():write(prior,migration)
    sources=read(R/'registries/source_registry.csv');sby={norm(r['url']):r for r in sources};matrix=read(R/'registries/industry_lesson_matrix.csv')
    for task in tasks:
        sr=sby.get(norm(task['url']));st=state.get(task['task_id'],{})
        if sr is None:
            sr={k:'' for k in sources[0]};sr.update(source_id=task['source_id'],agency=task['issuer'],dataset=task['title'],url=task['url'],lesson_ids=task['lesson_ids'],issuer=task['issuer'],title=task['title'],source_type=task['source_role'],primary_vs_secondary='academic_original_or_working_paper' if task['source_role']=='theory' else 'bibliographic_metadata' if task['source_role']=='bibliography' else 'industry_association' if task['issuer']=='OICA' else 'primary_official_or_issuer',publication_date=task['publication_date'],data_period=task['data_period'],country=task['country'],geography=task['country'],license=task['license']);sources.append(sr);sby[norm(task['url'])]=sr
        if sr['source_id']==task['source_id']:sr.update(title=task['title'],dataset=task['title'],publication_date=task['publication_date'],data_period=task['data_period'])
        if st:
            sr.update(local_path=st.get('local_path',''),sha256=st.get('sha256',''),fetched_at=st.get('fetched_at',''),last_checked=st.get('fetched_at',''),access_status='fulltext_downloaded' if st['status'] in SUCCESS and task['content_kind']=='document' else 'metadata_verified' if st['status'] in SUCCESS else st['status'],verification_status='format_parsed_content_not_reviewed' if st['status'] in SUCCESS else 'not_verified')
        if task.get('enabled','true')=='false':
            sr.update(access_status='superseded',verification_status='link_not_selected_due_to_relevance',notes=task['origin'])
            continue
        for lesson in task['lesson_ids'].split(';'):
            key=(lesson,sr['source_id'],task['source_role'])
            if not any((r['lesson_id'],r['reference_id'],r['source_role'])==key for r in matrix):matrix.append(dict(lesson_id=lesson,reference_id=sr['source_id'],reference_type='source',source_role=task['source_role'],confidence='applicability_candidate_not_claim_evidence',verified_at=st.get('fetched_at',''),status='identified',source_id=sr['source_id'],section_topic=task['title'],evidence_claim_id='',verification_status=sr.get('verification_status','identified'),last_checked=st.get('fetched_at','')))
    a.write_csv('registries/source_registry.csv',sources);a.write_csv('registries/industry_lesson_matrix.csv',matrix)
    # 統一catalog為join view，主表不將公司文件與論文入口混為官方統計。
    catalog=[];logs=artifacts();urlmap={}
    for path,ls in logs.items():
        for l in ls:urlmap[norm(l['url'])]=(path,l)
    for table,key,typ,urlcol in [('source_registry','source_id','official','url'),('literature_master','paper_id','academic','landing_url'),('company_filings','filing_id','company','source_url')]:
        for r in read(R/'registries'/f'{table}.csv'):
            url=r[urlcol];urls=[url]+([r['oa_url']] if r.get('oa_url') else []);found=next((urlmap[norm(u)] for u in reversed(urls) if norm(u) in urlmap),None)
            path,log=found if found else ('',{})
            status='metadata_verified' if r.get('bibliographic_verified')=='true' else 'identified'
            if r.get('access_status') in ['restricted','broken','failed','budget_deferred','superseded']:status=r['access_status']
            fmt=Path(path).suffix.lstrip('.') if path else ''
            document=(fmt in ['pdf','csv','xlsx','odt'] or typ=='academic' and bool(r.get('fulltext_verified')=='true') or r.get('access_status')=='fulltext_downloaded')
            if path and document:status='fulltext_downloaded'
            if r.get('fulltext_verified')=='true':status='fulltext_verified'
            catalog.append(dict(source_id=r[key],record_type='academic' if r.get('source_type')=='theory' else typ,title=r.get('title',r.get('dataset',r.get('issuer',''))),issuer=r.get('agency',r.get('authors',r.get('issuer',''))),url=url,download_url=log.get('url',''),doi=r.get('doi',''),publication_year=r.get('year',r.get('fiscal_year',r.get('publication_date',''))),data_period=r.get('data_period',''),lesson_ids=r.get('lesson_ids',''),license=r.get('license','unknown'),local_path=path,sha256=log.get('sha256',''),format=fmt,source_status=status,is_document=str(document).lower(),fetched_at=log.get('accessed_at',''),last_checked=r.get('last_checked',''),notes='source availability is not reviewed claim or lesson completeness'))
    # 深度批次的原文與逐主張核對保留為獨立的document identity。
    deep=R/'evidence/deep-2026-11-06';reviews=read(deep/'paper_reviews.csv');obs=read(deep/'observations.csv');case=read(deep/'company_cases.csv')
    for s in read(deep/'sources.csv'):
        lids=set()
        for item in reviews+obs:
            if item['source_id']==s['source_id']:lids.update(item.get('lessons',item.get('lesson_ids','')).split(';'))
        for c in case:
            if c['source_id']==s['source_id']:lids.add(c['lesson_id'])
        status='claim_verified' if any(o['source_id']==s['source_id'] for o in obs) else 'fulltext_verified' if any(p['source_id']==s['source_id'] for p in reviews) else 'fulltext_downloaded'
        catalog.append(dict(source_id=s['source_id'],record_type='deep_document',title=s['title'],issuer=s['identity'],url=s['url'],download_url=s['url'],doi='',publication_year='',data_period=s['version'],lesson_ids=';'.join(sorted(lids-{''})),license=s['rights'],local_path=s['local_private_path'],sha256=s['sha256'],format=Path(s['local_private_path']).suffix.lstrip('.'),source_status=status,is_document='true',fetched_at=s['accessed_at'],last_checked=s['accessed_at'],notes='claim_verified applies only to observations with exact locators; not every sentence'))
    current_claims=read(R/'sources/verified_observations_v2.csv')
    for c in catalog:
        if any(o['source_id']==c['source_id'] for o in current_claims):c.update(source_status='claim_verified',notes='Only named observations in verified_observations_v2.csv checked; not entire report or lesson')
    for m in matrix:
        ids=[o['observation_id'] for o in current_claims if o['source_id']==m['reference_id'] and m['lesson_id'] in o['lesson_ids'].split(';')]
        if ids:m.update(evidence_claim_id=';'.join(ids),verification_status='claim_verified_scoped')
    a.write_csv('registries/industry_lesson_matrix.csv',matrix)
    write(R/'sources/catalog.csv',catalog)
    groups=defaultdict(list)
    for c in catalog:
        if c['sha256']:groups[('sha256',c['sha256'])].append(c['source_id'])
        if c['doi']:groups[('doi',c['doi'].lower())].append(c['source_id'])
        if c['url']:groups[('normalized_url',norm(c['url']))].append(c['source_id'])
    write(B/'identity_groups.csv',[dict(identity_type=k[0],identity=k[1],source_ids=';'.join(sorted(set(v))),handling='retain distinct index/document roles; coverage deduplicates SHA, no deletion of versions') for k,v in groups.items() if len(set(v))>1],fields=['identity_type','identity','source_ids','handling'])
    coverage(catalog)

def coverage(catalog):
    titles=a.lessons();matrix=read(R/'registries/industry_lesson_matrix.csv');roles=defaultdict(set)
    for m in matrix:roles[(m['lesson_id'],m['source_role'])].add(m['reference_id'])
    deep=R/'evidence/deep-2026-11-06';reviews=read(deep/'paper_reviews.csv');obs=read(deep/'observations.csv')+read(R/'sources/verified_observations_v2.csv');cases=read(deep/'company_cases.csv')
    rows=[];gaps=[]
    for lid,title in zip(lesson_list(),titles):
        entries=[c for c in catalog if lid in c['lesson_ids'].split(';')]
        claims=[o for o in obs if lid in o['lesson_ids'].split(';')];papers=[p for p in reviews if lid in p['lessons'].split(';')]
        docs={c['sha256'] for c in entries if c['sha256'] and c['is_document']=='true'};available={c['sha256'] for c in entries if c['sha256']}
        rolecounts={role:len(roles[(lid,role)]) for role in ['classification','global','taiwan','theory','firm','history']}
        missing=GAPS[int(lid)]+'；歷史/圖像權利/跨產業主張仍須逐項核對'
        rows.append(dict(lesson_id=lid,title=title,classification_candidates=rolecounts['classification']+len(roles[(lid,'methodology')]),global_candidates=rolecounts['global'],taiwan_candidates=rolecounts['taiwan'],academic_candidates=len(roles[(lid,'theory')]),company_candidates=rolecounts['firm'],history_candidates=rolecounts['history'],available_artifacts=len(available),distinct_documents_available=len(docs),reviewed_papers=len(papers),claim_checked_observations=len(claims),reviewed_company_cases=sum(c['lesson_id']==lid for c in cases),source_status='claim_checked_partial' if claims or papers else 'fulltext_available_unreviewed' if docs else 'metadata_only',whole_lesson_sufficient='false',important_gaps=missing))
        rows[-1]['content_checked_sources']=len({o['source_id'] for o in claims}|{p['source_id'] for p in papers})
        for role,target in [('classification',1),('global',2),('taiwan',2),('history',1),('academic',2),('company',1),('recent',1),('visual',1),('cross_industry',1)]:
            role_claims=[o for o in claims if o.get('kind')=='official_statistic' and (o['entity'] in ['World','BIS reporting banks worldwide'] if role=='global' else o['entity'] in ['Taiwan','Chinese Taipei','兆豐國際商業銀行#','臺灣銀行#'])]
            verified=len(role_claims) if role in ['global','taiwan'] else len(papers) if role=='academic' else sum(c['lesson_id']==lid for c in cases) if role=='company' else 0
            # global/taiwan不以同一總主張數充當已驗證；逐筆分類待核。
            gaps.append(dict(lesson_id=lid,evidence_kind=role,target_sources=target,source_status='partially_verified' if verified else 'gap_unresolved',verified_evidence_count=verified,verified_source_count=len({o['source_id'] for o in role_claims}) if role in ['global','taiwan'] else verified,missing_reason='全球/台灣逐主張分類與口徑核對尚未完成；可用候選數不等於已驗證' if role in ['global','taiwan'] else '逐項證據仍須依來源定位核讀；不得由下載量填滿門檻',whole_lesson_sufficient='false'))
        p=R/f'notes/lessons/lesson-{lid}/acquisition-v2.md'
        text=f'# {lid}｜{title}\n\n這是來源盤點，不是教材。狀態：{rows[-1]["source_status"]}。\n\n原始文件可用（SHA去重）{len(docs)}；已核讀研究{len(papers)}；已定位數值{len(claims)}。\n\n## 已有來源與下載層級\n\n'
        for c in entries:text+=f'- {c["source_id"]}｜{c["title"]}｜{c["source_status"]}｜{c["url"]}\n'
        text+=f'\n## 尚缺\n\n{missing}。所有課均不足以宣稱已完成10,000–15,000字出版級教材。\n\n研究問題、子產業與學習範圍沿用本課index.md；本輪不補寫沒有來源的歷史或研究發現。\n'
        p.write_text(text,encoding='utf-8')
    write(B/'coverage.csv',rows);write(B/'lesson_gaps.csv',gaps)
    report='# 00–49來源涵蓋盤點 v2\n\n候選數包括入口；可用文件依SHA去重，已確認原文數在本表保守採既有逐篇核讀卡，不等於已查核整篇所有內容。US資料不是全球總量。50課皆未達出版級教材充分性。\n\n|課|分類候選|全球候選|台灣候選|學術候選|企業候選|歷史候選|可用文件|核讀研究|已核對觀察|狀態／主要缺口|\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|\n'
    for r in rows:report+='|'+ '|'.join(str(r[k]) for k in ['lesson_id','classification_candidates','global_candidates','taiwan_candidates','academic_candidates','company_candidates','history_candidates','distinct_documents_available','reviewed_papers','claim_checked_observations'])+'|'+r['source_status']+'；'+r['important_gaps']+'|\n'
    (R/'audit/coverage_report.md').write_text(report,encoding='utf-8')
    restricted=[s for s in read(STATE) if s['status'] not in SUCCESS]
    write(B/'restricted_and_failures.csv',restricted,fields=list(restricted[0]) if restricted else ['task_id','status','error'])
    (R/'audit/next_actions.md').write_text('''# 下一批續跑

本輪未執行背景自動任務。先查看 full-acquisition-v2/coverage.csv、lesson_gaps.csv、restricted_and_failures.csv。

從repository目錄執行：

```powershell
python research/scripts/full_acquisition.py fetch --lessons all --resume --skip-verified --rate-limit 2 --max-files-per-run 25 --max-bytes-per-run 80000000
python research/scripts/full_acquisition.py discover --lessons all --max-files-per-run 20
python research/scripts/full_acquisition.py fetch --lessons 06,07,08,09,27,42,44 --resume --skip-verified --retry-failures --max-files-per-run 15 --max-bytes-per-run 60000000
python research/scripts/full_acquisition.py report
python research/scripts/validate_full_acquisition.py
python research/scripts/validate_deep_evidence.py
python research/scripts/validate.py
```

`--dry-run`僅列待辦、不發送請求。預設不自動重試受限或失敗來源；開啟retry-failures才重新嘗試，每次最多一次暫時性502/503/504退避。遇robots/login/CAPTCHA不繞過。download log保留latest view，每次嘗試另存acquisition_attempts_v2.csv。

優先下一步：逐課補兩項真正全球資料與兩項台灣統計，對已下載文件核對定義與值；擴充產業專屬期刊OA查核及公司時間線；取得TW12正式細目與TW11官方對照，不猜配對；歷史／圖像權利／跨產業主張須獨立核讀。現有候選不足的課應先以官方搜尋補源，不能把共用宏觀入口當產業專屬證據。
''',encoding='utf-8')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['init','fetch','report','inventory','discover']);parser.add_argument('--lessons',default='all');parser.add_argument('--task-ids',default='');parser.add_argument('--resume',action='store_true');parser.add_argument('--skip-verified',action='store_true');parser.add_argument('--retry-failures',action='store_true');parser.add_argument('--dry-run',action='store_true');parser.add_argument('--rate-limit',type=float,default=2);parser.add_argument('--max-files-per-run',type=int,default=30);parser.add_argument('--max-bytes-per-run',type=int,default=100000000);parser.add_argument('--max-file-bytes',type=int,default=25000000);parser.add_argument('--output-dir',type=Path,default=PRIVATE)
    args=parser.parse_args();args.output_dir=args.output_dir.resolve()
    if args.resume:args.skip_verified=True
    if not args.output_dir.is_relative_to(a.PRIVATE.resolve()):parser.error('output-dir must remain inside gitignored private_sources')
    if args.command=='init':init()
    elif args.command=='fetch':run(args)
    elif args.command=='inventory':inventory('current_inventory.csv')
    elif args.command=='discover':discover(args)
    else:materialize();inventory('current_inventory.csv')

if __name__=='__main__':main()
