"""50課盤點、來源身份、續跑及原始檔檢查；不以PASS宣稱教材充分。"""
import json,re,subprocess
from collections import Counter,defaultdict
from pathlib import Path
import full_acquisition as f

def main():
    checks=[];issues=[]
    def ck(name,ok,detail):checks.append(dict(check=name,passed=bool(ok),detail=detail))
    tasks=f.read(f.TASKS);taskmap={t['task_id']:t for t in tasks};states=f.read(f.STATE)
    ck('task_keys_unique',len(tasks)==len(taskmap),str(len(tasks)))
    ck('normalized_task_urls_unique',len({f.norm(t['url']) for t in tasks})==len(tasks),'same URL reused, not downloaded twice')
    ck('all_lessons_have_inventory',set(r['lesson_id'] for r in f.read(f.B/'coverage.csv'))==set(f.lesson_list()),'00–49 exactly')
    gaps=f.read(f.B/'lesson_gaps.csv');ck('nine_gap_dimensions_per_lesson',len(gaps)==450 and all(sum(r['lesson_id']==l for r in gaps)==9 for l in f.lesson_list()),'classification/global/Taiwan/history/academic/company/recent/visual/cross-industry')
    ck('no_complete_lessons',all(r['whole_lesson_sufficient']=='false' for r in f.read(f.B/'coverage.csv')),'candidate and download counts not publication readiness')
    # 新增內容品質規則重新檢查既有成功嘗試，保留原始嘗試紀錄；目前狀態可被降級。
    for r in states:
        if r['status'] not in f.SUCCESS:continue
        p=f.safe(r['local_path']);ck('bytes_'+r['task_id'],p.exists() and f.sha(p.read_bytes())==r['sha256'],r['local_path'])
        try:
            meta,text=f.inspect(p.read_bytes(),taskmap[r['task_id']]['format']);r.update(meta)
            if meta['parse_status']!='parsed':issues.append(dict(task_id=r['task_id'],severity='high',issue=meta['parse_status'],handling='file exists; do not infer financial values or study findings from corrupt/empty text'))
        except Exception as e:
            r.update(status='broken' if 'soft404' in str(e) else 'failed',error=str(e),reason=str(e),parse_status='invalid_source_content')
            issues.append(dict(task_id=r['task_id'],severity='high',issue=str(e),handling='reclassified from prior apparent HTTP success; original attempt retained'))
    f.write(f.STATE,states);f.write(f.B/'content_issues.csv',issues,fields=['task_id','severity','issue','handling'])
    # 更新latest download view，不覆寫逐次append-only acquisition_attempts。
    latest=f.read(f.R/'audit/download_log.csv');lookup={r['task_id']:r for r in states}
    for r in latest:
        if r['resource_id'] in lookup:
            s=lookup[r['resource_id']];r.update(status='downloaded' if s['status'] in f.SUCCESS else s['status'],parse_status=s['parse_status'],reason=s['reason'])
    f.a.write_csv('audit/download_log.csv',latest)
    f.materialize();current=f.inventory('current_inventory.csv')
    raw=[r for r in current if r['access_status']=='local_source_artifact'];unique={r['sha256'] for r in raw}
    f.write(f.B/'deduplicated_local_sources.csv',[dict(sha256=h,paths=';'.join(r['path'] for r in raw if r['sha256']==h),origin_urls=' | '.join(sorted({r['origin_url'] for r in raw if r['sha256']==h}))) for h in sorted(unique)],fields=['sha256','paths','origin_urls'])
    catalog=f.read(f.R/'sources/catalog.csv');ids={r['source_id'] for r in catalog}
    ck('catalog_ids_unique',len(catalog)==len(ids),str(len(catalog)))
    for table,keys in [('source_registry',['source_id']),('literature_master',['paper_id']),('company_filings',['filing_id']),('industry_lesson_matrix',['lesson_id','reference_id','source_role'])]:
        rows=f.read(f.R/'registries'/f'{table}.csv');composite=[tuple(r[k] for k in keys) for r in rows]
        ck(table+'_keys',len(composite)==len(set(composite)),str(len(rows)))
    matrix=f.read(f.R/'registries/industry_lesson_matrix.csv')
    ck('matrix_source_references',all(m['source_id'] in ids for m in matrix),'legacy union source/paper/filing plus deep document catalog')
    lit=f.read(f.R/'registries/literature_master.csv');dois=[r['doi'].lower() for r in lit if r['doi']]
    ck('doi_valid_unique',len(dois)==len(set(dois)) and all(re.match(r'^10\.\d{4,9}/\S+$',d) for d in dois),'DOI shape and uniqueness, not proof of content')
    ck('working_papers_not_journal',all(r['peer_reviewed']=='false' for r in lit if r['paper_id'] in ['F_ROBOTS_2017','F_TUTORING_2024']),'NBER original cover explicitly says not peer reviewed')
    cls=f.read(f.R/'registries/classification_master.csv');new=[r for r in cls if r['system']=='TW_SIC' and r['version']=='12'];hist=[r for r in cls if r['system']=='TW_SIC' and r['version']=='11']
    ck('tw12_counts',Counter(r['level'] for r in new)=={'section':20,'2':88,'3':254,'4':530},'official PDF4 and21–37')
    ck('tw11_historical_preserved',len(hist)==878 and all(r['version_status']=='historical_not_current' for r in hist),'not current reference in2026')
    parents={(r['system'],r['version'],r['code']) for r in cls}
    ck('tw12_parent_keys',all(not r['parent_code'] or (r['system'],r['version'],r['parent_code']) in parents for r in new),'do not guess industry fine-code crosswalk')
    for r in states:
        if r['local_path']:ck('private_path_'+r['task_id'],f.safe(r['local_path']).is_relative_to(f.a.PRIVATE.resolve()),r['local_path'])
    ck('new_downloads_not_claims',all(r.get('status') not in ['fulltext_verified','claim_verified'] for r in states),'download states never imply content read')
    claims=f.read(f.R/'sources/verified_observations_v2.csv')
    ck('claim_source_fk',all(r['source_id'] in ids for r in claims),str(len(claims)))
    needles={'V2_FAO_FISH24':['223.2','185.4','37.8'],'V2_FAO_FISH26':['235 million','195 million','103 million'],'V2_IEA_ELECTRICITY':['4.3%','1 080'],'V2_WHO25_RELEASE':['1.8 years','2019 and 2021']}
    for tid,values in needles.items():
        t=next(r for r in states if r['task_id']==tid);_,text=f.inspect(f.safe(t['local_path']).read_bytes(),taskmap[tid]['format']);ck('original_values_'+tid,all(v in text for v in values),str(values)+'; manual scope/period review separate')
    from pypdf import PdfReader
    nhe=PdfReader(f.safe(next(s['local_path'] for s in states if s['task_id']=='V2_MOHW113_A'))).pages[22].extract_text()
    ck('Taiwan_NHE_original',all(v in nhe for v in ['6,951','7.5','2,687']), 'PDF23/printed22;111ROC=2022,2024edition; added LTC and retrospective revisions')
    tracked=subprocess.check_output(['git','ls-files'],cwd=f.ROOT,text=True).splitlines()
    ck('no_private_files_public',not any(p.startswith(('private_sources/','downloads/','cache/','credentials/')) or p.lower().endswith(('.pdf','.zip')) for p in tracked),'raw third-party originals remain ignored')
    ck('website_unchanged',not subprocess.check_output(['git','diff','0bd0256','--name-only','--','docs'],cwd=f.ROOT).strip(),'no website/deployment edits')
    ck('source_urls_http',all(not r['url'] or r['url'].startswith(('https://','http://')) for r in catalog),'no credential/file URL')
    schema={p.name:list(f.read(p)[0]) for p in (f.R/'registries').glob('*.csv') if f.read(p)}
    (f.R/'schemas/full_acquisition_v2.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2),encoding='utf-8')
    attempt=f.read(f.R/'audit/acquisition_attempts_v2.csv');counts=Counter(r['status'] for r in states);newformats=Counter(taskmap[r['task_id']]['format'] for r in states if r['status']=='downloaded');reusedformats=Counter(taskmap[r['task_id']]['format'] for r in states if r['status']=='reused_existing')
    result=dict(local_files_inventoried=len(current),source_files_with_origin=len(raw),deduplicated_source_files=len(unique),verified_dois=sum(bool(r['doi']) and r['bibliographic_verified']=='true' for r in lit),source_catalog_records=len(catalog),tasks=len(tasks),actual_attempts=len(attempt),current_states=dict(counts),new_download_formats=dict(newformats),reused_formats=dict(reusedformats),new_files_parseable=sum(r['status']=='downloaded' and r['parse_status']=='parsed' for r in states),text_quality_issues=issues,verified_new_observations=len(claims),passed=sum(r['passed'] for r in checks),checks=len(checks),failed=[r['check'] for r in checks if not r['passed']],lessons_sufficient_for_publication=0,running_in_background=False)
    (f.B/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');f.write(f.B/'validation_checks.csv',checks)
    (f.B/'verification_report.md').write_text('# 全課程來源查核\n\n'+json.dumps(result,ensure_ascii=False,indent=2)+'\n\n下載與格式檢查不是整篇核讀；本輪新增原文身份核對與具定位官方發布數值核對，其餘內容仍須核讀。歷史來源、影像權利及細碼跨版對照仍有大範圍缺口。\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    if result['failed']:raise SystemExit(1)

if __name__=='__main__':main()
