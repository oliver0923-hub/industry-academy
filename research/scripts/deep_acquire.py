"""八課深度驗證下載。僅官網、作者與機構典藏；原檔留在private_sources。"""
import acquire as a
import io,json,re,sys
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader

PAGES=[
('bellemare_author','https://marcfbellemare.com/wordpress/research'),
('diamond_repository','https://knowledge.uchicago.edu/records/3sa4m-hvw53'),
('dachan_annual','https://www.dachan.com/en/annual'),
('intel_annual','https://www.intc.com/filings-reports/annual-reports'),
('tyson_annual','https://ir.tyson.com/financials/annual-reports/default.aspx'),
('bot_annual','https://www.bot.com.tw/tw/about/annual-report'),
('oecd_semiconductor','https://www.oecd.org/en/publications/mapping-the-semiconductor-value-chain_4154cdbf-en.html'),
('fao_production','https://www.fao.org/statistics/highlights-archive/highlights-detail/agricultural-production-statistics-2010-2024/'),
('moa_2024','https://www.moa.gov.tw/sp_ws.php?id=2517097'),
('moa_scope','https://agrstat.moa.gov.tw/moasdweb/visualize/VisualChart.aspx?c=A01&s=2'),
('fsc_bank_data','https://data.gov.tw/dataset/28781'),
('fsc_assets_data','https://data.gov.tw/dataset/104098'),
('bis_2024','https://www.bis.org/statistics/rppb2504.htm'),
('coase_author','https://www.coase.org/coaseonline'),
('gvc_author','https://www.globalvaluechains.org/publications/'),
]
PDFS=[
('jpm_2024','https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/annualreport-2024.pdf'),
('coase_1937','https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1468-0335.1937.tb00002.x'),
('harvard_henderson_retry','https://dash.harvard.edu/server/api/core/bitstreams/99ac7120-48cf-4ff2-ba8a-60a3bd6ed0a0/content'),
('bis_2024_pdf','https://www.bis.org/statistics/rppb2504.pdf'),
]
def get(key,url,kind='html'):
    data,log=a.fetch(url,'deep_'+key,kind)
    if data:
        if kind=='pdf':
            try:
                reader=PdfReader(io.BytesIO(data));pages=[dict(pdf_page=i+1,text=p.extract_text() or '') for i,p in enumerate(reader.pages)]
                (a.PRIVATE/('deep_'+key+'_pages.json')).write_text(json.dumps(pages,ensure_ascii=False),encoding='utf-8')
                (a.PRIVATE/('deep_'+key+'_text.txt')).write_text('\n'.join(f'\n[PDF page {p["pdf_page"]}]\n'+p['text'] for p in pages),encoding='utf-8')
                print(key,'PDF',len(pages),'text_chars',sum(len(p['text']) for p in pages),flush=True)
            except Exception as e:log['reason']='PDF parser failed: '+str(e)[:200];print(key,'parse failed',flush=True)
        else:
            s=a.soup(data);links=[dict(label=x.get_text(' ',strip=True),url=urljoin(url,x['href'])) for x in s.select('a[href]')]
            (a.PRIVATE/('deep_'+key+'_links.json')).write_text(json.dumps(links,ensure_ascii=False),encoding='utf-8')
            print(key,'HTML',len(data),flush=True)
    else:print(key,log['status'],flush=True)
    return data
def main():
    if '--evidence-manifest' in sys.argv:
        import csv,hashlib
        manifest=a.R/'evidence/deep-2026-11-06/sources.csv'
        with manifest.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
        for row in rows:
            target=a.ROOT/row['local_private_path']
            key=target.stem
            kind=target.suffix.lstrip('.')
            data,log=a.fetch(row['url'],key,kind)
            if data and hashlib.sha256(data).hexdigest()!=row['sha256']:
                print('VERSION_CHANGED',row['source_id'],flush=True)
            elif data:
                print('MATCH',row['source_id'],flush=True)
            else:print('UNAVAILABLE',row['source_id'],log['status'],flush=True)
        a.flush_log()
        return
    with ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(lambda x:get(*x),PAGES))
    with ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(lambda x:get(*x,'pdf'),PDFS))
    a.flush_log()

if __name__=='__main__':main()
