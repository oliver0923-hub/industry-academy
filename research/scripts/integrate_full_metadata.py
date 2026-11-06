"""將本批原始書目回傳與文件身份接回既有主索引；不自動填研究發現。"""
import json
from pathlib import Path
from bs4 import BeautifulSoup
import acquire as a
import full_acquisition as f

def main():
    state={r['task_id']:r for r in f.read(f.STATE)};tasks={r['task_id']:r for r in f.read(f.TASKS)}
    lit=a.read_csv('registries/literature_master.csv');matrix=a.read_csv('registries/industry_lesson_matrix.csv')
    pairs=[('ROBOT','V2_NBER_ROBOTS','F_ROBOTS_2017'),('EDTECH','V2_NBER_EDTECH','F_TUTORING_2024'),('TOURISM','V2_TOURISM_RESEARCH','F_TOURISM_2024')]
    for key,tid,pid in pairs:
        cr=state.get('V2_CR_'+key,{})
        if cr.get('status') not in f.SUCCESS:continue
        m=json.loads(f.safe(cr['local_path']).read_text(encoding='utf-8'))['message'];t=tasks[tid];s=state.get(tid,{})
        r=next((r for r in lit if r['paper_id']==pid),None)
        if r is None:r={k:'' for k in lit[0]};lit.append(r)
        r.update(paper_id=pid,authors='; '.join(' '.join([x.get('given',''),x.get('family','')]).strip() for x in m.get('author',[])),year=str(m.get('published',m.get('issued',{})).get('date-parts',[['']])[0][0]),title='; '.join(m.get('title',[])),journal_or_publisher='; '.join(m.get('container-title',[])) or m.get('publisher',''),publication_type=m.get('type',''),peer_reviewed='false' if key in ['ROBOT','EDTECH'] else 'journal_article_status_from_publisher',doi=m['DOI'].lower(),landing_url='https://doi.org/'+m['DOI'],oa_url=t['url'],access_status='fulltext_downloaded' if s.get('status') in f.SUCCESS else s.get('status','identified'),license=t['license'],lesson_ids=t['lesson_ids'],bibliographic_verified='true',fulltext_verified='false',review_status='identity_and_cover_checked_not_full_study_reviewed',notes='Crossref plus original cover/title checked; NBER versions are working papers, not final journal articles. Findings/method/sample need original sections; do not infer from search snippet. Original abstract stays in private metadata JSON, not republished here.',abstract='',oa_status='public_readable_not_redistribution_permission',local_path=s.get('local_path',''),sha256=s.get('sha256',''),fetched_at=s.get('fetched_at',''),last_checked=cr.get('fetched_at',''),volume=m.get('volume',''),issue=m.get('issue',''),pages=m.get('page',''),metadata_url=cr['url'])
        card=a.R/'notes/theory_cards'/f'{pid}.md'
        card.write_text(f'# {r["title"]}\n\n作者：{r["authors"]}；{r["year"]}；{r["journal_or_publisher"]}；DOI {r["doi"]}。\n\n版本及存取：{r["publication_type"]}；{r["access_status"]}。封面／題名與書目已核對；不表示已完成原研究內容核讀。\n\n- 研究問題：待核讀原文相關段落。\n- 理論機制：候選適用於第{r["lesson_ids"]}堂，逐課適用性仍待驗證。\n- 實際資料／方法／結果：本輪未完成研究段落核對，不填估計係數或樣本。\n- 限制：NBER工作稿不是已同行評審的正式期刊版；Granger預測先後性也不能直接當作政策介入因果效果。\n- 引用定位：PDF封面／首頁身份；研究內容頁碼仍待核讀。\n- 來源：[原始文件]({t["url"]})；[書目回傳]({cr["url"]})。\n',encoding='utf-8')
        for lesson in t['lesson_ids'].split(';'):
            if not any(x['lesson_id']==lesson and x['reference_id']==pid for x in matrix):matrix.append(dict(lesson_id=lesson,reference_id=pid,reference_type='paper',source_role='theory',confidence='industry_relevance_candidate',verified_at=cr['fetched_at'],status='fulltext_downloaded_study_review_pending',source_id=pid,section_topic='industry mechanism',evidence_claim_id='',verification_status='metadata_verified',last_checked=cr['fetched_at']))
    hs=state.get('V2_HOSPITAL_REVIEW',{})
    if hs.get('status') in f.SUCCESS:
        soup=BeautifulSoup(f.safe(hs['local_path']).read_bytes(),'html.parser')
        values=lambda name:[m.get('content','') for m in soup.select('meta[name="'+name+'"]')]
        pid='F_HOSPITAL_REVIEW_2024';r=next((r for r in lit if r['paper_id']==pid),None)
        if r is None:r={k:'' for k in lit[0]};lit.append(r)
        r.update(paper_id=pid,authors='; '.join(values('citation_author')),year='2024',title=values('citation_title')[0],journal_or_publisher=values('citation_journal_title')[0],publication_type='journal-article',peer_reviewed='journal_article_status_from_publisher',doi=values('citation_doi')[0],landing_url='https://doi.org/'+values('citation_doi')[0],oa_url=tasks['V2_HOSPITAL_REVIEW']['url'],access_status='fulltext_downloaded',license='PMC copyright/license must be checked before republication',lesson_ids='42',bibliographic_verified='true',fulltext_verified='false',review_status='PMC_citation_metadata_checked_study_review_pending',notes='Original PMC citation metadata/title/authors/date/DOI checked; not Crossref reverified this run. Review methods/inclusion studies and findings not yet audited.',local_path=hs['local_path'],sha256=hs['sha256'],fetched_at=hs['fetched_at'],last_checked=hs['fetched_at'],volume=values('citation_volume')[0],issue=values('citation_issue')[0],pages=values('citation_firstpage')[0],metadata_url=tasks['V2_HOSPITAL_REVIEW']['url'])
        (a.R/'notes/theory_cards'/f'{pid}.md').write_text(f'# {r["title"]}\n\n{r["authors"]}（2024），Healthcare12(22)，article2218；DOI {r["doi"]}。\n\n原文HTML可讀，已核對NLM/PMC引用身份，未完成研究內容核讀。\n\n研究問題／理論機制：醫院競爭與醫療品質的文獻回顧候選，尚須逐段確認範圍。實際資料／方法、主要發現、限制及引用定位：待核讀納入標準、原始研究與評估方法，不將review當作單一因果效果。對應第42堂。\n',encoding='utf-8')
        if not any(m['lesson_id']=='42' and m['reference_id']==pid for m in matrix):matrix.append(dict(lesson_id='42',reference_id=pid,reference_type='paper',source_role='theory',confidence='industry_relevance_candidate',verified_at=hs['fetched_at'],status='fulltext_downloaded_study_review_pending',source_id=pid,section_topic='hospital competition',evidence_claim_id='',verification_status='metadata_verified',last_checked=hs['fetched_at']))
    a.write_csv('registries/literature_master.csv',lit)
    # 新公司文件只完成身份核對；不是完整公司案例，也不填未讀財務表。
    filings=a.read_csv('registries/company_filings.csv')
    tid='V2_MCD24';s=state.get(tid,{})
    if s.get('status') in f.SUCCESS:
        r=next((r for r in filings if r['source_url']==tasks[tid]['url']),None)
        if r is None:r={k:'' for k in filings[0]};filings.append(r)
        r.update(filing_id='FULL_MCD_2024',issuer="McDonald's Corporation",ticker='MCD',fiscal_year='2024',source_url=tasks[tid]['url'],geography='Global',lesson_ids='29;30;41;48',status='annual_cover_verified_body_encoding_issue',notes='Original PDF82pages; readable shareholder letter PDF2; main body font encoding corrupt in extracted text. Financial figures NOT verified; requires OCR/manual view.',local_path=s['local_path'],sha256=s['sha256'],fetched_at=s['fetched_at'],last_checked=s['fetched_at'],source_date='2025',event_date='',evidence_vs_interpretation='company self-report; no independent causal claim')
        for lesson in r['lesson_ids'].split(';'):
            if not any(x['lesson_id']==lesson and x['reference_id']==r['filing_id'] for x in matrix):matrix.append(dict(lesson_id=lesson,reference_id=r['filing_id'],reference_type='filing',source_role='firm',confidence='original_issuer_identity',verified_at=s['fetched_at'],status='document_identity_verified_figures_pending',source_id=r['filing_id'],section_topic='franchise business',evidence_claim_id='',verification_status='identity_verified',last_checked=s['fetched_at']))
        p=a.R/'notes/company_cases/MCD_2024.md';p.parent.mkdir(exist_ok=True)
        p.write_text("# McDonald's 2024年度文件身份與待核對事項\n\n原始年報82頁，PDF2股東信可讀；內文大部分文字層有字型編碼問題，不當作已取得可搜尋正確財務數字。\n\n|event_date|source_date|company|evidence_vs_interpretation|定位|\n|---|---|---|---|---|\n|1955-04|2024年度年報／2025股東信|McDonald's|公司回顧Kroc在Des Plaines開店；僅為公司敘事，不能據此斷言全球第一家McDonald's始於1955或忽略創業前史|PDF2|\n\n策略、結果、反證與完整發展時間線仍待獨立歷史來源及可讀財務表。不得以Systemwide sales取代公司合併營收。\n",encoding='utf-8')
    a.write_csv('registries/company_filings.csv',filings);a.write_csv('registries/industry_lesson_matrix.csv',matrix)

if __name__=='__main__':main()
