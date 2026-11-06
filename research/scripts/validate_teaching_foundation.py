"""核對研究包血緣、定位、原件雜湊與關鍵數字；不替代人工內容審查。"""
from pathlib import Path
import csv,hashlib,json,re,subprocess
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
PACK=ROOT/'research/evidence/teaching-foundation-2026-11-06'
def read(name):
    with (PACK/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def main():
    checks=[]
    def check(name,passed,detail=''):checks.append(dict(check=name,passed=bool(passed),detail=detail))
    cs=read('claims.csv'); ss=read('sources.csv');src={s['source_id']:s for s in ss}
    check('claim_ids_unique',len({c['claim_id'] for c in cs})==len(cs))
    check('source_ids_unique',len(src)==len(ss))
    allowed={'bibliography_only','abstract_verified','fulltext_downloaded','fulltext_read','claim_verified'}
    check('source_status_vocabulary',all(s['status'] in allowed and s['status']!='claim_verified' for s in ss))
    for c in cs:
        check('claim:'+c['claim_id'],c['source_id'] in src and all(c[k] for k in ['claim','source_name','original_url','publication_year','data_year','precise_locator','supporting_content','applicability_limit']) and c['verification_status']=='claim_verified')
        if c['origin']=='new_original_read':check('read_scope:'+c['claim_id'],src[c['source_id']]['status']=='fulltext_read')
    for s in ss:
        if s['local_private_path']:
            p=ROOT/s['local_private_path']
            check('private_original:'+s['source_id'],p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'])
    gaps=read('gap_reclassification.csv');req=read('priority_requirements.csv')
    check('legacy_450_preserved',len(gaps)==450 and len({r['legacy_gap_id'] for r in gaps})==450 and all(r['closed_by_this_mapping']=='false' for r in gaps))
    check('priority_63_requirements',len(req)==63 and len({r['requirement_id'] for r in req})==63)
    check('no_unsupported_ready_claim',all(r['ready_for_complete_draft']=='false' and r['publication_review_passed']=='false' for r in read('readiness.csv')))
    for l in ['00','01','05','18','25','30','31']:
        check('lesson_report:'+l,(PACK/f'lesson-{l}/teaching_readiness_report.md').exists() and (PACK/f'lesson-{l}/evidence_pack.md').exists())
    # 獨立重新解析關鍵頁，不用生成程式的數值當預期值。
    for filename,page,tokens in [('T_YULON24.pdf',86,['85,776,046','7,269,249']),('T_YULON24.pdf',87,['25,910,182','744,745']),('T_MOEA_RETAIL24.pdf',2,['48 530','2.6']),('T_MOEA_RETAIL24.pdf',3,['6 533','13.5']),('T_ROBOTS_JPE2020.pdf',16,['722']),('T_ROBOTS_JPE2020.pdf',50,['0.39','0.77','0:09','0:15'])]:
        text=PdfReader(ROOT/'private_sources/full-v2'/filename).pages[page-1].extract_text() or ''
        check(f'original_page:{filename}:{page}',all(t in text for t in tokens),'tokens='+','.join(tokens))
    # 僅檢查 public research 區；原始圖與快取全部私存。
    check('no_pack_originals',not any(p.suffix.lower() in {'.pdf','.png','.jpg','.html'} for p in PACK.rglob('*')))
    changed=subprocess.check_output(['git','diff','--name-only','9a5f648'],cwd=ROOT,text=True).splitlines()
    check('website_and_deployment_untouched',all(p.startswith('research/') for p in changed),','.join(p for p in changed if not p.startswith('research/')))
    result=dict(checks=len(checks),passed=sum(r['passed'] for r in checks),failed=[r for r in checks if not r['passed']],new_claims=sum(c['origin']=='new_original_read' for c in cs),inherited_claims=sum(c['origin']=='inherited_verified_observation' for c in cs),unique_claims=len(cs),new_journal_format_core_reads=1,new_author_manuscript_core_reads=1,complete_lessons_ready=0,scope='Structural consistency, SHA checks and six numerical page checks only; not independent publication review')
    (PACK/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    with (PACK/'validation_checks.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,list(checks[0]));w.writeheader();w.writerows(checks)
    print(json.dumps(result,ensure_ascii=False));return bool(result['failed'])
if __name__=='__main__':raise SystemExit(main())
