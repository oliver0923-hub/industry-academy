"""Phase 4 深度查核：原作／重印／書評分離，補充合法典藏。"""
import acquire as a
import json,re,io,time,hashlib
from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader

def main():
    papers=a.read_csv('registries/literature_master.csv');matrix=a.read_csv('registries/industry_lesson_matrix.csv')
    replacements={
      'Xad1253dbc':('Akerlof original','10.2307/1879431','Information asymmetry','品質資訊不對稱與逆向選擇'),
      'X380ac0033':('Granovetter original','10.1086/225469','Social networks','弱連帶、橋接與非冗餘資訊'),
      'X548ba6340':('Arrow original','10.2307/1812044','Health economics','疾病與療效不確定性、資訊及醫療制度'),
      'Xd92208d87':('Bellemare contract farming','10.1016/j.worlddev.2011.12.008','Agricultural contracts','契作參與選擇與農戶福利；處理不可觀察異質性仍有假設')}
    aliases=[]
    for i,p in enumerate(papers):
        if p['paper_id'] in replacements:
            new=a.paper_metadata(replacements[p['paper_id']]);new['paper_id']=p['paper_id'];new['lesson_ids']=p['lesson_ids']
            aliases.append(dict(paper_id=p['paper_id'],excluded_doi=p['doi'],excluded_title=p['title'],excluded_container=p['journal_or_publisher'],reason='書名相近但並非所需原作：重印、百科條目或不同著作；已改用原作',replacement_doi=new['doi']))
            papers[i]=new
        elif p['paper_id'] in ['X19f70e4ce','X7df7512f2']:
            aliases.append(dict(paper_id=p['paper_id'],excluded_doi=p['doi'],excluded_title=p['title'],excluded_container=p['journal_or_publisher'],reason='原結果是書評；不能當作原專書',replacement_doi=''))
            if p['paper_id']=='X19f70e4ce':
                p.update(authors='Richard E. Caves',year='2000',title='Creative Industries: Contracts Between Art and Commerce',journal_or_publisher='Harvard University Press',publication_type='academic_book',peer_reviewed='false',doi='',landing_url='https://www.hup.harvard.edu/books/9780674008083',bibliographic_verified='false',volume='',issue='',pages='',metadata_url='https://www.hup.harvard.edu/books/9780674008083',notes='原自動結果為書評，已隔離；原作出版社頁另查核，不猜 DOI')
            else:
                p.update(authors='Universities-National Bureau Committee for Economic Research',year='1962',title='The Rate and Direction of Inventive Activity: Economic and Social Factors',journal_or_publisher='Princeton University Press / NBER',publication_type='edited_academic_book',peer_reviewed='false',doi='',landing_url='https://www.nber.org/books-and-chapters/rate-and-direction-inventive-activity-economic-and-social-factors',bibliographic_verified='false',volume='',issue='',pages='',metadata_url='https://www.nber.org/books-and-chapters/rate-and-direction-inventive-activity-economic-and-social-factors',notes='原查詢為書評，已隔離；原作 NBER 專書另查核')
    extras=[
      ('Coase firm','10.1111/j.1468-0335.1937.tb00002.x','TCE','企業內組織與價格機制的協調成本',[0,1,3,4,28,34,35,36,45,48,49]),
      ('Hardin commons','10.1126/science.162.3859.1243','Commons','開放取得下的外部性；不能推論共同治理必然失敗',[6,7,9,46]),
      ('Advertising empirical','10.1016/S0167-2681(98)00118-8','Signaling','廣告與品質訊號的可觀察關係',[25,33]),
      ('Schultz capital','10.2307/1818907','Human capital','教育與技能投資；不能忽略自我選擇',[44]),
      ('Ostrom commons','10.1126/science.284.5412.278','Commons governance','共同治理規則與開放取得不同；制度條件改變資源結果',[6,9,46,47])]
    for title,doi,theory,mech,ids in extras:
        new=a.paper_metadata((title,doi,theory,mech));new['lesson_ids']=';'.join(f'{n:02}' for n in ids)
        if not any(p['doi'].lower()==new['doi'].lower() for p in papers):papers.append(new)
    # 校對原作機制的反向案例；僅針對書目，不假稱讀過全部全文。
    for p in papers:
        if p['publication_type'] in ['edited-book','book','reference-entry','other','academic_book','edited_academic_book']:p['peer_reviewed']='false'
        if p['paper_id']=='P010':p['notes']+=' 指定來源為學術專書，不是期刊論文。'
        if p['paper_id']=='P015':p['publication_type']='peer_reviewed_literature_review';p['peer_reviewed']='true';p['notes']+=' 線上首次出版2023；卷期年須與online-first分開。'
    artifact_specs=[
      ('arrow_original','https://assets.aeaweb.org/asset-server/files/9442.pdf','pdf','X548ba6340'),
      ('granovetter_original','https://smg.media.mit.edu/library/Granovetter1973.pdf','pdf','X380ac0033'),
      ('bellemare_preprint','https://mpra.ub.uni-muenchen.de/23638/1/contractfarmingwelfareimpactsmpra.pdf','pdf','Xd92208d87'),
      ('caves_publisher','https://www.hup.harvard.edu/books/9780674008083','html','X19f70e4ce'),
      ('nber_book','https://www.nber.org/books-and-chapters/rate-and-direction-inventive-activity-economic-and-social-factors','html','X7df7512f2'),
      ('coase_publisher','https://onlinelibrary.wiley.com/doi/full/10.1111/j.1468-0335.1937.tb00002.x','html',''),
    ]
    with ThreadPoolExecutor(max_workers=3) as ex:out=list(ex.map(lambda x:a.fetch(x[1],x[0],x[2]),artifact_specs))
    for spec,(data,log) in zip(artifact_specs,out):
        key,url,kind,pid=spec
        if not data:continue
        p=next((p for p in papers if p['paper_id']==pid),None)
        if kind=='pdf':
            try:
                texts=[page.extract_text() or '' for page in PdfReader(io.BytesIO(data)).pages]
                (a.PRIVATE/(key+'_extracted.txt')).write_text('\n'.join(f'\n[PDF page {i+1}]\n'+t for i,t in enumerate(texts)),encoding='utf-8')
                if p:p.update(oa_url=url,access_status='fulltext_downloaded_review_pending',notes=p['notes']+' 合法出版社／機構公開版下載；非全文可重散布授權。'+(' MPRA是2010工作稿，與2012期刊原作分開，不能混用效果量。' if 'preprint' in key else ''))
            except Exception as e:log['reason']='PDF extraction failed: '+str(e)[:160]
        elif p:
            body=a.soup(data).get_text(' ',strip=True)
            if ('Creative Industries' in body if 'caves' in key else 'Rate and Direction' in body):p['bibliographic_verified']='true'
    # 保存出版社摘要狀態；不複製全文摘要到公開庫。
    for p in papers:
        # 修正替換後 Crossref 原始檔的 hash ID。
        candidates=[a.PRIVATE/('crossref_'+p['paper_id']+'.json')]
        if p['doi']:candidates.insert(0,a.PRIVATE/('crossref_X'+hashlib.sha256(p['doi'].encode()).hexdigest()[:9]+'.json'))
        meta=next((x for x in candidates if x.exists()),None)
        if meta:
            obj=json.loads(meta.read_text(encoding='utf-8'))['message']
            if obj.get('DOI','').lower()==p['doi'].lower() and obj.get('abstract'):
                p['notes']+=' 出版社登錄摘要可讀；僅摘要證據，不填全文樣本。'
                if not p['access_status'].startswith('fulltext'):p['access_status']='abstract_available'
    a.write_csv('audit/excluded_bibliographic_matches.csv',aliases)
    a.write_csv('registries/literature_master.csv',papers)
    keys={(r['lesson_id'],r['reference_id'],r['source_role']) for r in matrix}
    for p in papers:
        for lid in filter(None,p['lesson_ids'].split(';')):
            key=(lid,p['paper_id'],'theory')
            if key not in keys:
                matrix.append(dict(lesson_id=lid,reference_id=p['paper_id'],reference_type='paper',source_role='theory',confidence='original work identified; applicability needs review',verified_at=a.DATE if p['bibliographic_verified']=='true' else '',status='metadata'));keys.add(key)
    a.write_csv('registries/industry_lesson_matrix.csv',matrix)
    # 刪除重複公司入口列並統一外鍵；相同主體、URL、年度才合併。
    filings=a.read_csv('registries/company_filings.csv');seen={};new=[];remap={}
    for f in filings:
        k=(f['issuer'],f['source_url'],f['fiscal_year'])
        if k in seen:
            target=seen[k];target['lesson_ids']=';'.join(sorted(set(target['lesson_ids'].split(';')+f['lesson_ids'].split(';'))));remap[f['filing_id']]=target['filing_id']
        else:seen[k]=f;new.append(f)
    for m in matrix:m['reference_id']=remap.get(m['reference_id'],m['reference_id'])
    unique={ (m['lesson_id'],m['reference_id'],m['source_role']):m for m in matrix}
    a.write_csv('registries/company_filings.csv',new);a.write_csv('registries/industry_lesson_matrix.csv',list(unique.values()))
    a.flush_log();a.build_cards_and_reports()

if __name__=='__main__':main()
