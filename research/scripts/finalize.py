"""保存人工查核結果、版本差異與本批交付狀態。"""
import acquire as a
import json,html,re,hashlib
from pathlib import Path

def main():
    papers=a.read_csv('registries/literature_master.csv');matrix=a.read_csv('registries/industry_lesson_matrix.csv')
    for p in papers:
        p['journal_or_publisher']=html.unescape(p['journal_or_publisher'])
        meta=a.PRIVATE/('crossref_'+p['paper_id']+'.json')
        if meta.exists():
            m=json.loads(meta.read_text(encoding='utf-8'))['message']
            if m.get('DOI','').lower()==p['doi'].lower():
                p['online_first_year']=str(m.get('published-online',{}).get('date-parts',[['']])[0][0])
                year=m.get('published-print',{}).get('date-parts',[['']])[0][0]
                if year:p['year']=str(year)
                if m.get('subtitle'):p['title']=': '.join(m.get('title',[])+m['subtitle'])
        if p['paper_id']=='X548ba6340':
            # 不能把 JSTOR stable identifier 自動當作已註冊 DOI。
            p.update(authors='Kenneth J. Arrow',year='1963',title='Uncertainty and the Welfare Economics of Medical Care',journal_or_publisher='The American Economic Review',publication_type='theoretical_article',peer_reviewed='true',doi='',landing_url='https://www.jstor.org/stable/1812044',volume='53',issue='5',pages='941-973',metadata_url='https://assets.aeaweb.org/asset-server/files/9442.pdf',bibliographic_verified='true',fulltext_verified='true',access_status='fulltext_selected_sections_reviewed',notes='AEA官方原始PDF頁1及33核對作者、期刊、年份、頁碼；實讀印刷頁941–950及971–973。JSTOR stable ID 未通過Crossref DOI查核，DOI留空。',review_status='selected_sections_reviewed')
        if p['paper_id']=='Xa036b12b8':
            p.update(authors='Theodore W. Schultz',year='1961',title='Investment in Human Capital',journal_or_publisher='The American Economic Review',publication_type='presidential_address',peer_reviewed='not_applicable_presidential_address',doi='',landing_url='https://www.jstor.org/stable/1818907',volume='51',issue='1',pages='1-17',metadata_url='https://www.jstor.org/pss/1818907',bibliographic_verified='true',notes='JSTOR期刊書目由web查核；stable ID不等於DOI。AEA主席演說，不能冒稱匿名同行評審實證。')
        if p['paper_id'].startswith('P') and p['paper_id'] not in ['P002','P010']:
            p['peer_reviewed']='true'
            if 'peer_reviewed不表示實證或因果識別' not in p['notes']:p['notes']+=' 屬核心學術期刊研究／理論文章；peer_reviewed不表示實證或因果識別。'
        if p['paper_id']=='P011':p['year']='2017';p['online_first_year']='2016'
        if p['paper_id']=='Xc64db7c78':p['year']='2024';p['online_first_year']='2023'
        if p['paper_id']=='P015':
            p.update(year='2025',volume='36',issue='4',pages='536-562',online_first_year='2023',notes=p['notes']+' 出版社卷期頁核對：https://www.tandfonline.com/doi/full/10.1080/09537287.2023.2286283；Crossref仍是online-first，保留差異。')
        if p['paper_id']=='X380ac0033':p['access_status']='pdf_downloaded_scanned_unreviewed';p['notes']+=' PDF22頁為掃描，文字層不足；未聲稱讀過全文。'
        if p['paper_id']=='Xd92208d87':p['access_status']='journal_metadata_preprint_separate';p['oa_url']='';p['notes']+=' 2010MPRA稿獨立為W_Bellemare_2010；不能視為2012期刊全文取得。'
    original=next(p for p in papers if p['paper_id']=='Xd92208d87')
    work=dict(original);work.update(paper_id='W_Bellemare_2010',year='2010',journal_or_publisher='Munich Personal RePEc Archive, Paper 23638',publication_type='working_paper',peer_reviewed='false',doi='',landing_url='https://mpra.ub.uni-muenchen.de/23638/',oa_url='https://mpra.ub.uni-muenchen.de/23638/1/contractfarmingwelfareimpactsmpra.pdf',access_status='fulltext_selected_sections_reviewed',fulltext_verified='true',bibliographic_verified='true',volume='',issue='',pages='',metadata_url='https://mpra.ub.uni-muenchen.de/23638/',notes='2010-07-03工作稿；已讀PDF頁1–7，非2012正式期刊版本，禁止混用效果量。',review_status='selected_sections_reviewed')
    if not any(p['paper_id']==work['paper_id'] for p in papers):papers.append(work)
    for lid in work['lesson_ids'].split(';'):matrix.append(dict(lesson_id=lid,reference_id=work['paper_id'],reference_type='paper',source_role='theory',confidence='author-deposited working-paper version; selected sections read',verified_at=a.DATE,status='reviewed'))
    a.write_csv('registries/literature_master.csv',papers)
    a.write_csv('registries/industry_lesson_matrix.csv',list({(m['lesson_id'],m['reference_id'],m['source_role']):m for m in matrix}.values()))
    # SIC入口由web工具實讀；本機HTTP403不被改寫成下載成功。
    cls=[c for c in a.read_csv('registries/classification_master.csv') if c['system']!='TW_SIC']
    import zipfile
    s=a.BeautifulSoup(zipfile.ZipFile(a.PRIVATE/'tw11_definitions.odt').read('content.xml'),'xml');stack={}
    for tr in s.find_all('table-row'):
        cells=tr.find_all('table-cell',recursive=False)
        if len(cells)!=5:continue
        codes=[c.get_text(' ',strip=True) for c in cells[:4]]
        # ODT 的170小類誤植1700；官方PDF分類系統表PDF頁21明列17/170/1700。
        if codes[1:] == ['17','1700','1700']:codes[2]='170'
        valid=[(i,c) for i,c in enumerate(codes) if re.fullmatch([r'[A-S]',r'\d{2}(?:-\d{2})?',r'\d{3}',r'\d{4}'][i],c)]
        if not valid:continue
        ps=[p.get_text(' ',strip=True) for p in cells[4].find_all('p')]
        label=ps[0] if ps else '';definition=' '.join(ps[1:])
        for i,code in valid:
            parent=stack.get(i-1,'') if i else '';stack[i]=code
            cls.append(dict(system='TW_SIC',version='11',code=code,label=label,definition=definition,url='https://ws.dgbas.gov.tw/001/Upload/463/attachment/11195/90015/01222134057t64vqlsy.odt',accessed_at=a.DATE,level=str(i+1),parent_code=parent,verification_status='official_definition_and_exclusions;170_reconciled_to_manual' if code=='170' else 'official_definition_and_exclusions'))
    sic=['Agriculture, Forestry, And Fishing','Mining','Construction','Manufacturing','Transportation, Communications, Electric, Gas, And Sanitary Services','Wholesale Trade','Retail Trade','Finance, Insurance, And Real Estate','Services','Public Administration']
    if not any(c['system']=='SIC' for c in cls):
        for code,label in zip('ABCDEFGHIJ',sic):cls.append(dict(system='SIC',version='1987',code=code,label=label,definition='',url='https://www.osha.gov/data/sic-manual',accessed_at=a.DATE,level='division',parent_code='',verification_status='official_web_tool_read; local_HTTP403; definitions_pending'))
    # ISIC5官方說明表，code(with section)移除前導section字母後才能和結構檔連結。
    import pandas as pd
    note_path=a.PRIVATE/'isic5_notes.xlsx'
    if note_path.exists():
        df=pd.read_excel(note_path,dtype=str).fillna('')
        defs={}
        for _,r in df.iterrows():
            raw=str(r.iloc[0]);code=raw if len(raw)==1 else raw[1:]
            defs[code]=' '.join(str(r.iloc[i]).replace('_x000D_',' ') for i in [3,4,5,6] if str(r.iloc[i]))
        for c in cls:
            if c['system']=='ISIC' and c['version']=='5' and c['code'] in defs:
                c['definition']=defs[c['code']];c['verification_status']='official_structure_and_explanatory_notes'
    for c in cls:
        if c['system']=='ISIC' and c['version']=='5':
            c['definition']=''
            c['verification_status']='official_structure; explanatory_notes_local_only_license_unconfirmed'
        c['definition']=re.sub(r'\s+',' ',c['definition']).strip()
        c['label']=c['label'].strip()
    a.write_csv('registries/classification_master.csv',cls)
    cross=a.read_csv('registries/classification_crosswalk.csv')
    dedup={}
    for c in cross:
        key=tuple(c[k] for k in ['from_system','from_version','from_code','to_system','to_version','to_code'])
        if key not in dedup:dedup[key]=c
        elif c['notes'] not in dedup[key]['notes']:dedup[key]['notes']+=' | '+c['notes']
    a.write_csv('registries/classification_crosswalk.csv',list(dedup.values()))
    # 行業第11次中類實際86類；不沿用未查核的舊數量。
    (a.R/'audit/version_and_identity_issues.md').write_text('''# 版本與來源身份查核

1. 台灣第12次已自2026-01-01生效；課綱指定第11次保留為歷史版。官方公告：https://www.stat.gov.tw/News_Content.aspx?n=3144&s=235560 。第11次依官方PDF核對19大類、88中類、249小類、522細類。ODT含45-46與47-48合併代碼，不可漏掉；170小類在ODT誤植1700，已依官方PDF頁21改正且保留查核標記。
2. 台灣–ISIC官方XLSX中文標題第11次，英文仍寫Rev.10,2016；所有相關列verified=false，禁止直接合併。
3. ISIC5已核實為UN通過版本；官方頁仍表示出版編修中。保存2026-08-19說明表及結構CSV，不能混同Rev.4。說明表全文只存本機，未確認重散布授權前公開CSV只留代碼/標籤，定義留空且不聲稱已公開完整定義。
4. Crossref查詢會返回書評、重印與百科；6筆已隔離於excluded_bibliographic_matches.csv。這些是初次候選檢索的錯配，不是可引用原作。
5. JSTOR stable ID不一定有可解析DOI。Arrow及Schultz原作已核對書目但DOI留空，不將stable ID拼成DOI。
6. Adner卷期年2017、online-first2016；Ando等卷期年2024、online-first2023。地緣政治review期刊卷期年2025，Crossref仍列2023線上版；保留日期差異。
7. Bellemare2010工作稿和2012期刊原作分成不同列；取得工作稿不代表期刊版已取得。Granovetter取得掃描PDF，尚未OCR及閱讀，不能提供實證樣本摘述。
8. Harvard DASH 的Henderson–Clark典藏原檔回401；metadata可讀不代表PDF可讀，保留為全文未取得。
9. 全課為metadata級來源包；個別文件可sourced/reviewed。共同理論可供比較，不代表各細產業實證文獻已補齊。無任何課標teaching-ready。
''',encoding='utf-8')
    # Schema machine-readable snapshot，與實際標頭完全一致。
    schemas={}
    for p in (a.R/'registries').glob('*.csv'):
        df=pd.read_csv(p,dtype=str,keep_default_na=False);schemas[p.stem]={'encoding':'UTF-8','fields':list(df.columns),'unknown_value':'','read_dtype':'string','rows':len(df)}
    (a.R/'schemas/tables.json').write_text(json.dumps(schemas,ensure_ascii=False,indent=2),encoding='utf-8')
    filings=a.read_csv('registries/company_filings.csv')
    identity={'A_tsmc_2024':('2024','PDF頁1封面與印行日期2025-03-12'),'A_microsoft_2024':('2024','官方HTML標題Microsoft2024 Annual Report'),'A_berkshire_2024':('2024','PDF頁1與3封面/目錄'),'D_F002':('2023','PDF頁1 Integrated Annual Report2023；URL含2024是上傳年'),'D_F014':('2024','PDF頁1 Form10-K，財年截至2024-03-31'),'D_F023':('2024','PDF頁1 Annual Report2024；財年不可預設曆年'),'D_F024':('2025','PDF頁1封面，頁2截至2025-12-31'),'D_F047':('2024','PDF頁1封面；與另一TSMC2024連結為不同SHA檔案版本，不加倍計算公司數')}
    for f in filings:
        if f['filing_id'] in identity:
            year,locator=identity[f['filing_id']];f.update(fiscal_year=year,status='annual_document_identity_verified',notes='已讀身份定位：'+locator+'；財務表口徑及查核意見未審閱，幣別與audited保持空白。')
    a.write_csv('registries/company_filings.csv',filings)
    a.build_cards_and_reports()
    cards={
    'X548ba6340':'''\n## 已讀原文補記（2026-11-06）

問題：醫療市場為何偏離完全競爭的福利條件？機制是疾病及療效不確定性、風險市場缺失與專業資訊難以交易，促成保險、專業信任及非市場制度。方法為理論與制度比較，沒有迴歸樣本或因果效果量。支持醫療制度可作為市場失靈的回應；不支持所有現存制度都有效率，也不是台灣健保的效果估計。

定位：Section I，印刷頁941–947（PDF1–7）；Section II.A–B，948–950（PDF8–10）；附錄保險命題971–973（PDF31–33）。短引文：“uncertainty in the incidence of disease and in the efficacy of treatment”（p.941）。教學42比較醫院、醫師、病人與支付方的資訊與風險；43須區分治療服務與新藥研發。只標選定章節已讀，未宣稱逐頁完成全篇評析。
''',
    'W_Bellemare_2010':'''\n## 已讀工作稿補記（2026-11-06）

問題：契作農戶是否獲得較佳福利，還是較有能力者先選擇契作？機制涉及契約協調與參與選擇。此2010稿使用Madagascar於2008年7–12月蒐集的資料，設計樣本1200戶、分析保留1178戶；作者以contingent valuation取得參與WTP，處理不可觀察異質性。這些樣本細節僅屬工作稿。

定位：PDF2摘要；PDF4–5（稿頁3–4）說明選擇偏誤與WTP策略；PDF6–7（稿頁5–6）資料設計及樣本。工作稿摘要報告正向福利結果，本卡不轉錄效果量或將其套用2012期刊版。限制是WTP／福利反向關係及排除限制仍需評估，不能直接外推台灣。教學05、10：比較穩定採購與農戶依賴，並檢查契作參與選擇。Citation readiness：僅引用2010工作稿版本及已讀段落。
'''}
    for pid,text in cards.items():
        p=a.R/f'notes/theory_cards/{pid}.md';p.write_text(p.read_text(encoding='utf-8')+text,encoding='utf-8')
    # 上方通用卡的待查文字由補記取代，不保留矛盾狀態。
    for pid in cards:
        p=a.R/f'notes/theory_cards/{pid}.md';text=p.read_text(encoding='utf-8');text=text.replace('方法／樣本／期間：尚未完成全文查核，不填入無法核實的觀察值、估計或效果量。主要發現：本卡暫不作全文研究結果摘述。','方法、樣本與發現：見下方已讀原文補記；核對範圍限明列章節與版本。');p.write_text(text,encoding='utf-8')
    phases={'Phase 1':'completed_with_gaps: schemas, classifications and 15 seeds; detailed mappings pending where blocked','Phase 2':'indexed: 50/50 global and Taiwan candidates; comparable numerical series pending','Phase 3':'partial: 9 groups mapped, original-work corrections completed; many actual annual reports and industry-specific studies pending','Phase 4':'executed_with_access_limits: legal downloads, cards, logs and validation; not 50 teaching-ready lessons'}
    (a.R/'audit/progress.json').write_text(json.dumps({'date':a.DATE,'branch':'codex/research-source-foundation','phases':phases,'user_authorization':'NTU College of Management accessible content; may skip difficult access','credentials_read':False,'website_modified':False,'railway_used':False},ensure_ascii=False,indent=2),encoding='utf-8')
    readme=a.R/'README.md';text=readme.read_text(encoding='utf-8').split('\n最終批次須接續')[0];text+='\n最終批次須接續 `python research/scripts/refine.py`、`python research/scripts/enrich.py`、`python research/scripts/supplement_official.py`、`python research/scripts/finalize.py`，最後 `python research/scripts/validate.py`。refine隔離同名書評及重印錯配，finalize保存人工版本核對；只重跑acquire不會重現最終人工查核狀態。\n';readme.write_text(text,encoding='utf-8')
    (a.R/'scripts/requirements.txt').write_text('requests\npandas\nbeautifulsoup4\nopenpyxl\npypdf\nlxml\n',encoding='utf-8')

if __name__=='__main__':main()
