"""修復已改址的官方分類；補充實際資料下載，所有狀態留紀錄。"""
import acquire as a
import io,re,json
import pandas as pd
from urllib.parse import urljoin
from pypdf import PdfReader

def main():
    url='https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/ISIC_Rev_4_english_structure.Txt'
    data,log=a.fetch(url,'isic4_official','csv')
    if data:
        df=pd.read_csv(io.BytesIO(data),dtype=str).fillna('');print('ISIC4',df.shape)
        cls=[c for c in a.read_csv('registries/classification_master.csv') if not(c['system']=='ISIC' and c['version']=='4')];stack={}
        for _,r in df.iterrows():
            code=r.iloc[0];level=1 if code.isalpha() else len(code);parent=stack.get(level-1,'');stack[level]=code
            cls.append(dict(system='ISIC',version='4',code=code,label=r.iloc[1],definition='',url=url,accessed_at=a.DATE,level=str(level),parent_code=parent,verification_status='official_structure'))
        a.write_csv('registries/classification_master.csv',cls)
        sources=a.read_csv('registries/source_registry.csv')
        for s in sources:
            if s['source_id']=='C_ISIC_4':s.update(url=url,access_status=log['status'],downloaded_on=a.DATE,verification_status='official_structure_downloaded')
        a.write_csv('registries/source_registry.csv',sources)
    # TWSE官方分類只有名稱，未取得正式數值代碼前不發明碼。
    p=a.PRIVATE/'TWSE_accessed_2026-11-06.html'
    if p.exists():
        text=a.soup(p.read_bytes()).get_text(' ',strip=True)
        segment=text.split('產業類別劃分為',1)[-1].split('等三十',1)[0]
        segment=re.sub(r'\s+','',segment)
        labels=re.split('、|及其他',segment)
        labels=[x for x in labels if x];labels.append('其他')
        a.write_csv('sources/twse_industry_labels.csv',[dict(label=l,official_numeric_code='',url='https://twse-regulation.twse.com.tw/TW/law/DOC01.aspx?FLCODE=FL007104&FLNO=2',version='amended_2025-06-09',accessed_at=a.DATE,note='上市企業分類；非總體產業統計分類，不推定數值代碼') for l in labels])
        print('TWSE labels',len(labels))
    # data.gov.tw具體資料集；只取由官方頁直接列出的資源連結。
    for sid in ['6607','54817']:
        url='https://data.gov.tw/dataset/'+sid;data,log=a.fetch(url,'data_gov_'+sid)
        if not data:continue
        ss=a.soup(data);links=[x['href'] for x in ss.select('a[href]') if '.csv' in x['href'].lower()]
        embedded=re.findall(r'https?[^\s<>"\\]+\.csv[^\s<>"\\]*',data.decode('utf-8','replace'),re.I)
        links=list(dict.fromkeys(links+embedded));print('dataset',sid,'CSV candidates',links[:3])
        for n,link in enumerate(links[:1]):a.fetch(link,'data_gov_resource_'+sid+'_'+str(n),'csv')
    industrial=a.PRIVATE/'data_gov_resource_6607_0.csv'
    if industrial.exists():
        df=pd.read_csv(industrial,dtype=str,keep_default_na=False)
        monthly=df[df['資料期(民國年)'].str.fullmatch(r'\d{3}(?:0[1-9]|1[0-2])')]
        quality=dict(rows=len(df),columns=list(df.columns),key=['統計項目','行業代碼','資料期(民國年)'],duplicate_keys=int(df.duplicated(['統計項目','行業代碼','資料期(民國年)']).sum()),nulls=df.isna().sum().to_dict(),monthly_period_min=monthly['資料期(民國年)'].min(),monthly_period_max=monthly['資料期(民國年)'].max(),units=sorted(df['計量單位'].unique().tolist()),source_url='https://service.moea.gov.tw/EE520/opendata/d.csv',metadata_url='https://data.gov.tw/dataset/6607',license='Open Government Data License Taiwan 1.0',retrieved_at=a.DATE,note='實際資源只有生產指數；metadata題名同時提價值不代表此CSV有生產價值。Z/I1等彙總碼不是官方分類細碼，不擅自join分類主表。')
        (a.R/'audit/taiwan_industrial_production_profile.json').write_text(json.dumps(quality,ensure_ascii=False,indent=2),encoding='utf-8')
        selected=monthly[(monthly['行業代碼'].isin(['Z','C','08','11','14','18','24','29','28','25'])) & (monthly['資料期(民國年)']>='11301')].copy()
        selected=selected.sort_values(['行業代碼','資料期(民國年)']).groupby('行業代碼',sort=False).tail(3)
        rows=[]
        for _,r in selected.iterrows():
            period=r['資料期(民國年)'];rows.append(dict(source_id='T_MOEA_IP',source_activity_code=r['行業代碼'],source_activity_label=r['行業別'],period=f'{int(period[:3])+1911}-{period[3:]}',value=r['統計值(指數)'],unit=r['計量單位'],nominal_real='volume_index',currency='not_applicable',geography='Taiwan',statistical_unit='industrial activity aggregate; see agency methodology',forecast_or_actual='published_observation_subject_to_revision',accessed_at=a.DATE,source_url=quality['source_url'],license=quality['license']))
        a.write_csv('sources/taiwan_industrial_production_sample.csv',rows)
        src=a.read_csv('registries/source_registry.csv');base=next(s for s in src if s['source_id']=='T_MOEA');new=dict(base);new.update(source_id='T_MOEA_IP',dataset='工業生產指數開放CSV（資料集6607）',measure='production_volume_index',definition='110年（2021）=100的工業生產指數；非名目產值、營收或GDP',unit='2021=100',nominal_real='volume_index',coverage=quality['monthly_period_min']+'–'+quality['monthly_period_max']+' ROC monthly',url=quality['source_url'],license=quality['license'],access_status='data_downloaded',downloaded_on=a.DATE,verification_status='CSV_schema_keys_units_period_checked')
        src=[s for s in src if s['source_id']!='T_MOEA_IP']+[new];a.write_csv('registries/source_registry.csv',src)
        matrix=a.read_csv('registries/industry_lesson_matrix.csv')
        for lid in base['lesson_ids'].split(';'):
            if int(lid) in list(range(10,22))+[25,26,43]:matrix.append(dict(lesson_id=lid,reference_id='T_MOEA_IP',reference_type='source',source_role='taiwan',confidence='official data file schema checked; exact series per lesson pending',verified_at=a.DATE,status='sourced'))
        a.write_csv('registries/industry_lesson_matrix.csv',list({(m['lesson_id'],m['reference_id'],m['source_role']):m for m in matrix}.values()))
    # 統一官網實際連到的IR服務才視為公司授權發布入口。
    data,log=a.fetch('https://www.uni-president.com.tw/','uni_official_hub')
    if data:
        links=[x['href'] for x in a.soup(data).select('a[href]') if 'sp88' in x['href']]
        if not links:
            invest,invest_log=a.fetch('https://www.uni-president.com.tw/invest/index.html','uni_invest_hub')
            if invest:
                si=a.soup(invest)
                links=[x.get('href') or x.get('src') for x in si.select('a[href],iframe[src]') if 'sp88' in (x.get('href','')+x.get('src',''))]
        print('Uni official delegated IR links',links)
        if links:
            url='https://ir.sp88.tw/en/finance.php';data,log=a.fetch(url,'uni_delegated_ir')
            if data:
                pdfs=[urljoin(url,x['href']) for x in a.soup(data).select('a[href]') if '.pdf' in x['href'].lower()]
                target=next((u for u in pdfs if 'fin_202505130828336643' in u),None)
                if target:
                    data,log=a.fetch(target,'uni_2024','pdf')
                    if data:
                        texts=[p.extract_text() or '' for p in PdfReader(io.BytesIO(data)).pages]
                        (a.PRIVATE/'uni_2024_extracted.txt').write_text('\n'.join(f'\n[PDF page {n+1}]\n'+t for n,t in enumerate(texts)),encoding='utf-8')
                        filings=a.read_csv('registries/company_filings.csv');f=next(f for f in filings if f['issuer']=='統一企業');row=dict(f);row.update(filing_id='A_uni_2024',source_url=target,fiscal_year='2024',status='annual_document_downloaded_identity_review_pending',notes='由公司官網連結sp88投資人服務；英文為摘要翻譯，與中文版本有差異以中文為準；尚未核對審計意見與幣別。');filings.append(row);a.write_csv('registries/company_filings.csv',filings)
                        matrix=a.read_csv('registries/industry_lesson_matrix.csv')
                        for lid in row['lesson_ids'].split(';'):matrix.append(dict(lesson_id=lid,reference_id=row['filing_id'],reference_type='filing',source_role='firm',confidence='official delegated IR document; review pending',verified_at=a.DATE,status='sourced'))
                        a.write_csv('registries/industry_lesson_matrix.csv',matrix)
    a.flush_log()

if __name__=='__main__':main()
