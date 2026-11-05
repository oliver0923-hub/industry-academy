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
    with ThreadPoolExecutor(max_workers=4) as ex:papers=list(ex.map(paper_metadata,CORE))
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

if __name__=='__main__':
    globals()['phase'+sys.argv[1]]()
