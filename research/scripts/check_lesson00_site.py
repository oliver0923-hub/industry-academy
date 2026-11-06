"""閱讀頁端到端檢查；僅本機瀏覽器標記，不改伺服器資料。"""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8876');args=parser.parse_args();base=args.url.rstrip('/')
    out=ROOT/'private_sources/lesson00-web-qa';out.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(base+'/lesson-00.html');page.wait_for_load_state('networkidle')
        assert page.locator('article h2').count()==11
        assert page.locator('.footnote li').count()==27
        assert page.locator('.figure-expand').count()==3
        assert '尚未完成獨立' in page.locator('.candidate-notice').inner_text()
        assert page.locator('body').evaluate('(e)=>e.scrollWidth <= innerWidth')
        page.screenshot(path=str(out/'desktop.png'))
        page.locator('.figure-expand').first.click();assert page.locator('dialog').evaluate('(e)=>e.open')
        page.keyboard.press('Escape');assert not page.locator('dialog').evaluate('(e)=>e.open')
        page.locator('#mark-read').click();assert page.locator('#mark-read').get_attribute('aria-pressed')=='true'
        page.evaluate('window.scrollTo(0,5000)');page.wait_for_timeout(200);page.reload();page.wait_for_load_state('networkidle')
        assert page.locator('#resume-reading').is_visible();page.locator('#resume-reading').click();assert page.evaluate('window.scrollY')>1000
        page.goto(base+'/index.html#lesson/0');assert page.get_by_role('link',name='閱讀第 00 堂教材候選稿 →').count()==1
        page.goto(base+'/index.html#lesson/1');assert page.locator('a[href="./lesson-01.html"]').count()==1
        page.goto(base+'/lesson-01.html');assert '01' in page.title()
        mobile=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
        mobile.goto(base+'/lesson-00.html');mobile.wait_for_load_state('networkidle');mobile.screenshot(path=str(out/'mobile.png'))
        assert mobile.locator('body').evaluate('(e)=>e.scrollWidth <= innerWidth')
        mobile.locator('#lesson-toc summary').click();assert mobile.locator('#lesson-toc').get_attribute('open') is not None
        assert not errors
        result=dict(url=base,desktop=True,mobile=True,footnotes=27,figures=3,zoom_escape=True,resume=True,self_mark=True,lesson01_preserved=True,page_errors=errors)
        (out/'result.json').write_text(json.dumps(result),encoding='utf-8');print(json.dumps(result));browser.close()
if __name__=='__main__':main()
