"""依官方第12次修正系統表建立階層；只輸出標籤，不冒充全文定義。"""
import re,json
from collections import Counter
from pypdf import PdfReader
import acquire as a

def main():
    pdf=a.PRIVATE/'full-v2/V2_TW12_MANUAL.pdf';doc=PdfReader(pdf)
    text=doc.pages[3].extract_text()
    assert '一百十五年一月一日生效' in text and '20個大' in text
    url='https://ws.dgbas.gov.tw/001/Upload/463/ebook/ebook_356166/pdf/full.pdf'
    rows={};section=division=group=''
    for n in range(21,38):
        for line in (doc.pages[n-1].extract_text() or '').splitlines():
            m=re.match(r'^((?:(?:[A-T]|\d{2}-\d{2}|\d{2,4})\s+)+)(.+)$',line.strip())
            if not m:continue
            codes=m[1].split();label=m[2].strip()
            for code in codes:
                level='section' if code.isalpha() else '2' if '-' in code else str(len(code))
                parent='' if level=='section' else section if level=='2' else division if level=='3' else group
                rows[code]=dict(system='TW_SIC',version='12',code=code,label=label,definition='',url=url,accessed_at='2026-11-06',level=level,parent_code=parent,verification_status='official_system_table_label_parsed',valid_from='2026-01-01',valid_to='',version_status='current_effective_at_2026-11-06',locator=f'PDF{n}/printed{n-5}')
                if level=='section':section=code
                elif level=='2':division=code
                elif level=='3':group=code
    counts=Counter(r['level'] for r in rows.values());assert counts=={'section':20,'2':88,'3':254,'4':530},counts
    old=a.read_csv('registries/classification_master.csv');old=[r for r in old if not(r['system']=='TW_SIC' and r['version']=='12')]
    for r in old:
        for f in ['valid_from','valid_to','version_status','locator']:r.setdefault(f,'')
        if r['system']=='TW_SIC' and r['version']=='11':r.update(valid_to='2025-12-31',version_status='historical_not_current')
    a.write_csv('registries/classification_master.csv',old+list(rows.values()))
    cross=a.read_csv('registries/classification_crosswalk.csv');existing={(r['from_system'],r['from_version'],r['from_code'],r['to_system'],r['to_version'],r['to_code']) for r in cross}
    pairs=[(c,c) for c in 'ABCDEFGHI']+[('J','J'),('J','K')]+[(c,chr(ord(c)+1)) for c in 'KLMNOPQRS']
    for oldcode,newcode in pairs:
        key=('TW_SIC','11',oldcode,'TW_SIC','12',newcode)
        if key in existing:continue
        cross.append(dict(zip(['from_system','from_version','from_code','to_system','to_version','to_code'],key),verified='true',confidence='official_section_change_only',notes='Official PDF18/printed13: J split into J/K and subsequent sections shifted. Section relation only; not a fine-code crosswalk.',url=url))
    a.write_csv('registries/classification_crosswalk.csv',cross)
    p=a.R/'audit/full-acquisition-v2/tw12_verification.md'
    p.write_text('# 第12次分類核對\n\n官方原文PDF4行政院函：2026-01-01生效，20大類、88中類、254小類、530細類；PDF21–37分類系統表逐行解析，共892列。45-46與47-48保留原始合併中類，不拆造。\n\nPDF18/印刷13：原J拆為J出版及影音等內容傳播、K電信及資訊服務，後續大類遞移；例如銀行由歷史K變為現行L，教育由P變Q。只新增大類對照，細類一對多重分仍待完整官方crosswalk。\n\n標籤不是定義，definition留空；統計單位及主要活動原則已讀PDF4、6–9。第11次原資料不刪除，明確標記historical_not_current。\n',encoding='utf-8')
    print(json.dumps(dict(rows=len(rows),counts=dict(counts),crosswalk_sections=len(pairs))))

if __name__=='__main__':main()
