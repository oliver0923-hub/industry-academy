"""選取官網實際連結的年度文件；保留版本與來源身份，不從 URL 猜已查核。"""
import acquire as a
import re,io,json
from urllib.parse import urljoin,urlparse
from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader

def main():
    filings=a.read_csv('registries/company_filings.csv');matrix=a.read_csv('registries/industry_lesson_matrix.csv')
    candidates=[];discover=[]
    for f in filings:
        if not f['filing_id'].startswith('F'):continue
        p=a.PRIVATE/(f['filing_id']+'.html')
        if not p.exists():continue
        s=a.soup(p.read_bytes())
        links=[(x.get_text(' ',strip=True),urljoin(f['source_url'],x['href'])) for x in s.select('a[href]')]
        annual=[(text,url) for text,url in links if '.pdf' in url.lower() and re.search(r'annual.report|annual-review|年報',text+' '+url,re.I) and re.search(r'202[45]',text+' '+url)]
        if annual:
            # 優先2024作歷史比較，勿將「2025」文件名視為最新或實際財年。
            annual.sort(key=lambda x:('2024' not in x[0]+' '+x[1],len(x[1])))
            candidates.append((f,annual[0]))
        elif f['geography']=='Taiwan' and any(int(n)<18 for n in f['lesson_ids'].split(';')):
            hits=[(text,url) for text,url in links if re.search(r'年報|財務資訊|投資人|annual.report|investor',text,re.I) and url.startswith('https://') and urlparse(url).netloc==urlparse(f['source_url']).netloc]
            if hits:discover.append((f,hits[0]))
    for f,(label,url) in discover:
        data,log=a.fetch(url,'discover_'+f['filing_id'])
        if not data:continue
        links=[(x.get_text(' ',strip=True),urljoin(url,x['href'])) for x in a.soup(data).select('a[href]')]
        hits=[(t,u) for t,u in links if '.pdf' in u.lower() and re.search(r'年報|annual.report',t+' '+u,re.I) and re.search(r'202[45]|11[34]',t+' '+u)]
        if hits:candidates.append((f,hits[0]))
    acquired=[]
    for f,(label,url) in candidates:
        fid='D_'+f['filing_id'];data,log=a.fetch(url,fid,'pdf')
        if not data:continue
        texts=[]
        try:texts=[p.extract_text() or '' for p in PdfReader(io.BytesIO(data)).pages]
        except Exception as e:log['reason']='PDF readable bytes but text extraction failed: '+str(e)[:120]
        if texts:(a.PRIVATE/(fid+'_extracted.txt')).write_text('\n'.join(f'\n[PDF page {n+1}]\n'+x for n,x in enumerate(texts)),encoding='utf-8')
        row=dict(f);row.update(filing_id=fid,source_url=url,fiscal_year='',status='annual_document_downloaded_identity_review_pending',notes='官方入口實際連結：'+label+'；PDF格式已驗證，財年、幣別、審計意見需閱讀核對，不由URL推測')
        filings.append(row);acquired.append(dict(filing_id=fid,issuer=f['issuer'],anchor_label=label,url=url,pdf_pages=len(texts),status=row['status']))
        for lid in f['lesson_ids'].split(';'):matrix.append(dict(lesson_id=lid,reference_id=fid,reference_type='filing',source_role='firm',confidence='direct official PDF link; identity review pending',verified_at=a.DATE,status='sourced'))
    a.write_csv('registries/company_filings.csv',filings);a.write_csv('registries/industry_lesson_matrix.csv',matrix);a.write_csv('audit/annual_document_discovery.csv',acquired,fields=['filing_id','issuer','anchor_label','url','pdf_pages','status']);a.flush_log()

if __name__=='__main__':main()
