"""檢查證據鏈、原值定位及容易誤用的內容；完整課程充分性另列未達標。"""
import csv, hashlib, json, re, subprocess
from pathlib import Path
from pypdf import PdfReader
import acquire as a
from build_deep_evidence import E, LESSONS

def read(name):
    with (E/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def main():
    checks=[]
    def ck(name,ok,detail):checks.append(dict(check=name,passed=bool(ok),detail=detail))
    tables={name:read(name+'.csv') for name in ['sources','observations','paper_reviews','company_cases','sufficiency','claims','gaps','audit_opinions']}
    for table,key in [('sources','source_id'),('observations','observation_id'),('paper_reviews','id'),('company_cases','case_id'),('sufficiency','lesson_id'),('claims','claim_id'),('gaps','gap_id')]:
        values=[r[key] for r in tables[table]];ck(table+'_keys',len(values)==len(set(values)),f'{len(values)} distinct records required')
    sources={r['source_id']:r for r in tables['sources']}
    ck('source_url_unique',len({r['url'] for r in sources.values()})==len(sources),'No exact duplicate evidence URL')
    bad=[]
    for r in sources.values():
        p=a.ROOT/r['local_private_path']
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:bad.append(r['source_id'])
    ck('all_source_bytes_match',not bad,str(bad))
    for table in ['observations','paper_reviews','company_cases','audit_opinions']:
        missing=set(r['source_id'] for r in tables[table])-set(sources)
        ck(table+'_source_fk',not missing,str(missing))
    for r in tables['observations']:
        assert r['value'] and r['unit'] and r['period'] and r['scope'] and r['locator'] and r['caution'],r['observation_id']
    ck('observations_metadata',True,'All numeric observations have units/period/scope/locator/caution; values may be rounded/lower bounds')
    obs={r['observation_id']:r for r in tables['observations']}
    # 原財報表中的正負號需人工核對；以下確認數字確實出現在正確來源頁。
    cache={}
    def pdftext(src,page):
        if src not in cache:cache[src]=PdfReader(a.ROOT/sources[src]['local_private_path'])
        return cache[src].pages[page-1].extract_text() or ''
    for case,page in [('TYSON',45),('DACHAN',8),('INTEL',65),('TSMC',64),('JPMBANK',5),('MEGA',13)]:
        rows=[r for r in tables['observations'] if r['observation_id'].startswith('C_'+case+'_') and r['metric'] not in ['total_assets','deposits','deposits_and_remittances']]
        text=pdftext(rows[0]['source_id'],page)
        missing=[r['observation_id'] for r in rows if f'{abs(int(r["value"])):,}' not in text]
        ck(case+'_income_original_page',not missing,f'PDF{page}; missing numeric tokens={missing}')
    ck('jpm_assets_original', '3,459,261' in pdftext('S_jpm_bank_official',7),'Bank subsidiary consolidated balance, not holding group')
    ck('mega_assets_original','4,192,553,310' in pdftext('S_mega_audited_2024',12),'Bank consolidated balance')
    # TSMC兩個年報URL只作出版物去重；不將有差異的20-F刪掉。
    t1=PdfReader(a.PRIVATE/'tsmc_2024.pdf').pages[63].extract_text()
    t2=pdftext('S_tsmc_annual',64)
    ck('tsmc_duplicate_financial_table',re.sub(r'\s+','',t1)==re.sub(r'\s+','',t2),'Both annual variants financial page64 match after whitespace normalization; original files/SHA retained')
    ck('tsmc_iasb_profit_conflict_retained',obs['O_TSMC_IASB_PROFIT']['value']!=str(int(obs['C_TSMC_net_income']['value'])/1000),'Different reporting basis retained; no artificial reconciliation')
    bank=read('taiwan_banks_2024_12.csv');keys=[(r['年'],r['月-期底'],r['銀行別']) for r in bank]
    ck('taiwan_bank_snapshot_keys',len(bank)==38 and len(set(keys))==38,'ROC113 December,38 unique reporting entries')
    mega=next(r for r in bank if r['銀行別']=='兆豐國際商業銀行#')
    ck('regulatory_mega_original',mega['資產-總額-新臺幣百萬元']==obs['O_FSC_MEGA']['value']=='4166596','Regulatory row retained; no replacement by annual consolidated value')
    rev={r['id']:r for r in tables['paper_reviews']}
    ck('conceptual_papers_no_invented_sample',all('不適用' in rev[p]['sample'] and '不適用' in rev[p]['period'] for p in ['Xa03c07055','P003','P004','X69013d8a3']),'Theoretical model time/publication years not sample periods')
    ck('gvc_versions_distinct','2003' in rev['W_GVC_2003']['version'] and rev['P005']['status']=='original_pdf_core_sections_reviewed','Both versions read; original2005 Table1 has its own printed p87')
    ck('mof_primary_value','165,042' in pdftext('S_mof_2024_release',3) and obs['O_TW_IC_PRIMARY']['value']=='165042','Original MOF preliminary2024 total, USD million; not rounded CBC figure')
    ck('dynamic_capability_version','processes' in rev['P009']['locator'] and '後來sensing' in rev['P009']['limitations'],'1997 processes/positions/paths; later framework not backdated')
    ck('pnas_locator_not_fabricated','待核' in rev['D_PNAS_2020']['locator'],'HTML fulltext read; exact print-page locator not invented')
    ck('pnas_design_not_panel','橫斷面' in rev['D_PNAS_2020']['method'] and '不能稱所得模型' in rev['D_PNAS_2020']['method'],'Income location FE vs individual labor household FE separated')
    ck('barney_vrin','VRIN' in rev['P003']['variables'] and '並非 VRIO' in rev['P003']['variables'],'Original1991 attributes not later framework')
    ck('hendersongeneration_measure','平減累積銷售' in rev['P007']['variables'],'Table2 not annual market share')
    ck('only_eight_sufficiency_records',set(r['lesson_id'] for r in tables['sufficiency'])==set(LESSONS),'No added industries')
    ck('no_false_complete_status',all(r['whole_lesson_sufficient']=='false' for r in tables['sufficiency']),'All eight retain full-lesson gaps; structural pass does not promote status')
    ck('six_company_cases',len(tables['company_cases'])==6 and all(sum(r['lesson_id']==l for r in tables['company_cases'])==2 for l in ['05','18','31']),'One global and one Taiwan firm for each demonstration industry')
    ck('operating_indicator_each_case',all(any(o['observation_id'].startswith('B_'+c['case_id']+'_') for o in tables['observations']) for c in tables['company_cases']),'Each case links a specific segment, operating or loan indicator')
    ck('six_audit_opinion_locators',len(tables['audit_opinions'])==6 and all(r['locator'] for r in tables['audit_opinions']),'Opinion scope/year separate from financial figure scope')
    links_bad=[]
    for p in E.rglob('*.md'):
        text=p.read_text(encoding='utf-8')
        for href in re.findall(r'\]\(([^)]+)\)',text):
            if not href.startswith(('https:','http:','#')) and not (p.parent/href).exists():links_bad.append(str(p)+':'+href)
    ck('evidence_relative_links',not links_bad,str(links_bad))
    for l in LESSONS:
        ck('lesson_'+l+'_pack',all(t in (E/f'lesson-{l}.md').read_text(encoding='utf-8') for t in ['已核對','尚待驗證','口徑','充分性']),'Evidence/pending/limitations separated')
    # 只對照八課增補，其他課既有筆記應完全不變。
    changed=subprocess.check_output(['git','diff','--name-only','51214ea1bc1e3c89af1a0e0c306d6854fe4b3692','--','research/notes/lessons'],cwd=a.ROOT,text=True).splitlines()
    ck('unselected_lessons_unchanged',all(any('/lesson-'+l+'/' in p for l in LESSONS) for p in changed if p.endswith('/index.md')),str(changed)+'; only legacy index.md constrained, new v2 acquisition notes for all50 explicitly authorized')
    with (E/'quality_checks.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['check','passed','detail']);w.writeheader();w.writerows(checks)
    result=dict(passed=sum(r['passed'] for r in checks),checks=len(checks),failed=[r['check'] for r in checks if not r['passed']],open_lesson_gaps=len(tables['gaps']),full_lessons_ready=0)
    (E/'quality_report.md').write_text('# 深度證據品質檢查\n\n'+json.dumps(result,ensure_ascii=False)+'\n\n'+''.join(f'- {"PASS" if r["passed"] else "FAIL"} {r["check"]}: {r["detail"]}\n' for r in checks)+'\n上述為證據鏈與內容約束檢查。全課充分性是另一道門檻，8課均有開放缺口，0課宣稱完整就緒。\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    if result['failed']:raise SystemExit(1)

if __name__=='__main__':main()
