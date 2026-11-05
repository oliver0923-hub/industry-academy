"""驗證公開索引主鍵、外鍵、覆蓋、下載真實性與網站保全。"""
import acquire as a
import json,hashlib,subprocess
import pandas as pd

def main():
    checks=[]
    def check(name,ok,detail):checks.append(dict(check=name,passed=bool(ok),detail=detail))
    tables={p.stem:pd.read_csv(p,dtype=str,keep_default_na=False) for p in (a.R/'registries').glob('*.csv')}
    for name,t in tables.items():
        pk={'source_registry':['source_id'],'literature_master':['paper_id'],'company_filings':['filing_id'],'classification_master':['system','version','code'],'classification_crosswalk':['from_system','from_version','from_code','to_system','to_version','to_code'],'indicator_dictionary':['indicator_id'],'industry_lesson_matrix':['lesson_id','reference_id','source_role']}[name]
        check(name+'_unique',not t.duplicated(pk).any(),f'{len(t)} rows; keys {pk}')
        check(name+'_utf8_no_bom',not (a.R/'registries'/f'{name}.csv').read_bytes().startswith(b'\xef\xbb\xbf'),'pandas read with string dtypes')
    lit=tables['literature_master'];doi=lit.loc[lit.doi!='','doi'].str.lower()
    check('DOI_unique',not doi.duplicated().any(),f'{len(doi)} nonempty DOIs')
    matrix=tables['industry_lesson_matrix'];expected={f'{n:02}' for n in range(50)}
    check('50_lessons',set(matrix.lesson_id)==expected,'IDs 00–49 preserved')
    for typ,name,pk in [('source','source_registry','source_id'),('paper','literature_master','paper_id'),('filing','company_filings','filing_id')]:
        missing=set(matrix.loc[matrix.reference_type==typ,'reference_id'])-set(tables[name][pk])
        check(typ+'_foreign_keys',not missing,str(sorted(missing)))
    for role in ['global','taiwan','theory','firm']:
        covered=set(matrix.loc[matrix.source_role==role,'lesson_id'])
        check(role+'_candidate_coverage',covered==expected,f'{len(covered)}/50; candidate coverage is not evidence completeness')
    check('no_teaching_ready',not (matrix.status=='teaching-ready').any(),'No published lessons implied')
    cls=tables['classification_master']
    tw=cls[(cls.system=='TW_SIC')&(cls.version=='11')]
    check('TW11_sections',sum(tw.code.str.match(r'^[A-S]$'))==19,'19 historical sections required')
    for level,count in [('2',88),('3',249),('4',522)]:
        check('TW11_level_'+level,sum(tw.level==level)==count,f'official manual required {count}; range codes and ODT typo reconciled')
    naics=cls[cls.system=='NAICS'];check('NAICS2022_sectors',sum(naics.level=='2')==20,'20 sectors, including combined manufacturing/retail/transport codes')
    links=tables['classification_crosswalk'];bad=links[links.from_version.str.contains('conflict')]
    check('version_conflicts_quarantined',not (bad.verified=='true').any(),f'{len(bad)} mappings withheld from verified use')
    logs=a.read_csv('audit/download_log.csv');failures=[];valid=0
    for l in logs:
        if l['status'] not in ['downloaded','cached_download']:continue
        p=a.ROOT/l['local_path']
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=l['sha256']:failures.append(l['resource_id'])
        else:valid+=1
    check('download_checksum',not failures,f'{valid} success records matched bytes; mismatches {failures}')
    for path in ['docs/index.html','docs/styles.css','docs/app.js']:
        base=subprocess.check_output(['git','show','origin/main:'+path],cwd=a.ROOT)
        now=(a.ROOT/path).read_bytes()
        check('unchanged_'+path,base.replace(b'\r\n',b'\n')==now.replace(b'\r\n',b'\n'),'same Git content vs origin/main; Windows checkout CRLF normalized')
    tracked=subprocess.check_output(['git','ls-files'],cwd=a.ROOT,text=True).splitlines()
    check('private_not_tracked',not any(x.startswith('private_sources/') for x in tracked),'No PDF/raw private data in public Git index')
    check('no_pdf_public',not any(p.suffix.lower()=='.pdf' for p in a.R.rglob('*')),'All PDFs local ignored only')
    check('one_card_per_paper',all((a.R/f'notes/theory_cards/{p}.md').exists() for p in lit.paper_id),f'{len(lit)} cards expected')
    check('50_lesson_source_packs',all((a.R/f'notes/lessons/lesson-{n:02}/index.md').exists() for n in range(50)),'Per-lesson sources and gaps')
    data=a.PRIVATE/'data_gov_resource_6607_0.csv'
    if data.exists():
        ip=pd.read_csv(data,dtype=str,keep_default_na=False)
        check('industrial_data_unique',not ip.duplicated(['統計項目','行業代碼','資料期(民國年)']).any(),f'{len(ip)} actual source rows')
        check('industrial_units',set(ip['計量單位'])=={'110年=100'},'Volume index; cannot be treated as revenue/GDP')
    a.write_csv('audit/validation_checks.csv',checks)
    report='# 品質驗證報告\n\n'+f'{sum(x["passed"] for x in checks)}/{len(checks)} 結構與保全檢查通過。\n\n'
    report+='\n'.join(f'- {"PASS" if c["passed"] else "FAIL"} {c["check"]}: {c["detail"]}' for c in checks)
    report+='\n\n實質限制：URL HTTP成功不代表資料內容、授權、更新日或跨國可比性已核對。全文下載、身份核對、研究內容閱讀分開紀錄。期刊文章不一律為實證，也不一律經同等同行評審。分類版本衝突、受限平台及每課學術/年報缺口詳見 coverage_report.md 與 restricted_access_queue.md。\n'
    (a.R/'audit/verification_report.md').write_text(report,encoding='utf-8')
    # manifest 不涵蓋自己，避免自我參照 hash。
    manifest=[]
    for p in sorted(a.R.rglob('*')):
        if p.is_file() and p.name!='manifest.csv' and '__pycache__' not in p.parts:
            data=p.read_bytes();manifest.append(dict(path=p.relative_to(a.ROOT).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    a.write_csv('audit/manifest.csv',manifest)
    print(json.dumps(dict(passed=sum(c['passed'] for c in checks),checks=len(checks),failed=[c['check'] for c in checks if not c['passed']]),ensure_ascii=False))
    if any(not c['passed'] for c in checks):raise SystemExit(1)

if __name__=='__main__':main()
