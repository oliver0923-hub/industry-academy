"""唯一補充請求：WDI當期價格定義。與全庫狀態寫入分離，保留原件及血緣。"""
from pathlib import Path
import requests,json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[2]
URL='https://api.worldbank.org/v2/indicator/NY.GDP.MKTP.CD?format=json'
def main():
    p=ROOT/'private_sources/lesson00-qa/wdi-gdp-definition.json';p.parent.mkdir(exist_ok=True,parents=True)
    origin=p.with_name('wdi-gdp-definition-origin.json')
    if p.exists():
        a=json.loads(p.read_text(encoding='utf-8'))
        if origin.exists():print('reused_existing_verified_json');return
        status='reused_existing'
    else:
        r=requests.get(URL,timeout=40);r.raise_for_status();a=r.json()
        if len(r.content)>1000000 or a[1][0]['id']!='NY.GDP.MKTP.CD':raise ValueError('Unexpected source content')
        p.write_bytes(r.content);status='downloaded'
    meta=dict(url=URL,local_private_path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,status=status,fetched_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),format='json',source_id='WDI_GDP_DEF',parse_status='parsed')
    origin.write_text(json.dumps(meta),encoding='utf-8');print(json.dumps(meta))
if __name__=='__main__':main()
