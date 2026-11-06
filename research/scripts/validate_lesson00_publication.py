"""候選稿一致性檢查；不能替代獨立審稿或把未解問題自動結案。"""
from pathlib import Path
import csv,json,hashlib,re,subprocess,xml.etree.ElementTree as ET
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'research/editorial/lesson-00'
def read(name):
    with (OUT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def main():
    checks=[]
    def ck(name,ok,detail=''):checks.append(dict(check=name,passed=bool(ok),detail=detail))
    t=(OUT/'candidate.md').read_text(encoding='utf-8');sha=hashlib.sha256((OUT/'candidate.md').read_bytes()).hexdigest()
    body=t.split('### 理解問題')[0]
    prose='\n'.join(l for l in body.splitlines() if not l.startswith(('|','#','>','![')) and not l.startswith(('圖1','圖2','圖3')))
    count=len(re.findall(r'[\u3400-\u9fff]',prose))
    ck('body_substantial_not_word_count_only',count>=9500,str(count)+' CJK excluding headings/tables/images/captions/references/questions/glossary')
    ck('ten_narrative_sections',len(re.findall(r'^## [0-9]+　',body,re.M))==10)
    ck('no_production_self_reference',not any(w.lower() in t.lower() for w in ['Codex','ZIP','AI生成','博士研究任務','private_sources','內部資料包']))
    ck('five_comprehension_questions',len(re.findall(r'^[1-5]\. ',t.split('### 理解問題')[1].split('### 產業情境')[0],re.M))==5)
    ck('scenario_and_glossary',all(x in t for x in ['### 產業情境','### 重要術語','### 相關課程']))
    refs=re.findall(r'^\[\^([^\]]+)\]:',t,re.M);used=re.findall(r'\[\^([^\]]+)\](?!:)',t)
    ck('footnote_keys_unique',len(refs)==len(set(refs)))
    ck('footnotes_resolve',set(refs)==set(used),str(sorted(set(used)-set(refs))))
    cs=read('claim_to_source.csv');ss=read('sources.csv');sm={r['source_id']:r for r in ss}
    ck('source_ids_unique',len(sm)==len(ss))
    ck('claim_ids_unique',len({r['claim_id'] for r in cs})==len(cs))
    ck('all_sections_mapped',{r['section_id'] for r in cs}=={f'S{i:02}' for i in range(1,11)})
    for c in cs:
        ck('anchor_'+c['claim_id'],c['candidate_anchor'] in t)
        if c['status']=='claim_verified':ck('trace_'+c['claim_id'],c['source_id'] in sm and all(c[k] for k in ['original_url','publication_year','data_year','precise_locator','supporting_content','scope_limit']))
        else:ck('hypothesis_not_fact_'+c['claim_id'],c['status'] in ['teaching_hypothesis','conditional_reasoning'] and c['source_id']=='AUTHOR_EXPOSITION')
    for s in ss:
        p=ROOT/s['local_private_path'];ck('original_sha_'+s['source_id'],p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'])
        ck('scoped_read_'+s['source_id'],s['status']=='fulltext_read' and bool(s['read_scope']))
    obs=read('observations.csv')
    for k in ['AGR','IND','SRV']:
        a=json.loads((ROOT/sm['WDI_'+k]['local_private_path']).read_text(encoding='utf-8'))
        for v in a[1]:
            r=next(x for x in obs if x['observation_id']=='WDI_'+k+'_'+v['countryiso3code'])
            ck('value_'+r['observation_id'],r['value']=='' and r['status']=='missing_not_zero' if v['value'] is None else float(r['value'])==v['value'])
    page=PdfReader(ROOT/sm['TW_STRUCTURE']['local_private_path']).pages[2].extract_text()
    compact=re.sub(r'\s+','',page)
    ck('taiwan_original_values',all(x in compact for x in ['1.8','36.3','62.0','1.5','40.4','58.1','31.4','35.7']))
    ck('hypothetical_arithmetic',sum([20,15,30,35])==100 and sum([20,35,65,100])==220 and '交易金額' in t and '35元買賣差價' in t)
    ck('wdi_open_issue_visible','待核對' in t and '未重新正規化為100%' in t)
    for f in read('figure_plan.csv'):
        p=OUT/f['file'];root=ET.parse(p).getroot();ck('svg_'+f['figure_id'],root.tag.endswith('svg') and '<script' not in p.read_text(encoding='utf-8'))
        ck('figure_link_'+f['figure_id'],f['file'] in t)
    reviews=read('section_reviews.csv');issues=read('unresolved_issues.csv')
    ck('forty_section_stage_reviews',len(reviews)==40 and len({(r['stage'],r['section_id']) for r in reviews})==40)
    ck('reviews_match_final_candidate',all(r['candidate_sha256']==sha for r in reviews))
    ck('independent_gate_not_faked',all(r['outcome']=='critical_reread_done_independent_gate_pending' for r in reviews if r['stage']=='4'))
    ck('blockers_remain_open',all(next(r for r in issues if r['issue_id']==i)['status']=='open' for i in ['P001','P002']))
    changed=subprocess.check_output(['git','diff','--name-only','afb4730'],cwd=ROOT,text=True).splitlines()
    ck('only_research_changed',all(p.startswith('research/') for p in changed))
    tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
    ck('no_public_originals',not any(p.startswith('private_sources/') or p.lower().endswith(('.pdf','.zip')) for p in tracked))
    ck('legacy_packs_preserved',not any(p.startswith('research/evidence/') for p in changed))
    result=dict(checks=len(checks),passed=sum(r['passed'] for r in checks),failed=[r for r in checks if not r['passed']],candidate_sha256=sha,body_cjk_prose_only=count,body_cjk_including_small_tables_and_headings=len(re.findall(r'[\u3400-\u9fff]',body)),footnotes=len(refs),source_records=len(ss),verified_source_claims=sum(c['status']=='claim_verified' for c in cs),hypotheses_and_conditional_reasoning=sum(c['status']!='claim_verified' for c in cs),figures=3,publication_ready=False,website_implementation_ready=False,independent_review_completed=False,publication_blockers=['P001','P002'],scope='Consistency, source SHA, values and editorial records; not external expert review')
    (OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    with (OUT/'validation_checks.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,list(checks[0]));w.writeheader();w.writerows(checks)
    print(json.dumps(result,ensure_ascii=False));return bool(result['failed'])
if __name__=='__main__':raise SystemExit(main())
