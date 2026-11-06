"""將已審閱中的00候選稿轉為網站預覽；不改其出版審查狀態。"""
from pathlib import Path
import shutil,hashlib,importlib.metadata
import markdown
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]
def main():
    src=ROOT/'research/editorial/lesson-00/candidate.md'
    text=src.read_text(encoding='utf-8')
    text=text.split('\n',1)[1].replace('> 教材候選稿。統計資料依文中所列年度與版本閱讀；本文尚非正式發布版本。','',1)
    md=markdown.Markdown(extensions=['extra','toc','sane_lists'],extension_configs={'toc':{'toc_depth':'2-2','permalink':False}})
    body=BeautifulSoup(md.convert(text),'html.parser')
    for table in body.find_all('table'):
        wrap=body.new_tag('div',attrs={'class':'table-scroll','tabindex':'0','aria-label':'可左右捲動的資料表'});table.wrap(wrap)
    for i,img in enumerate(body.find_all('img'),1):
        img['src']=img['src'].replace('figures/','assets/lesson-00/')
        img['loading']='lazy';img['decoding']='async'
        button=body.new_tag('button',attrs={'type':'button','class':'figure-expand','aria-label':f'放大圖{i}：'+img.get('alt','')});img.wrap(button)
    sha=hashlib.sha256(src.read_bytes()).hexdigest()
    html='''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="從一份早餐理解產業、企業、產品市場、價值鏈，以及全球與台灣產業結構。Lesson 00 教材候選稿，審閱中。">
<title>第00堂｜什麼是產業 · Industry Academy</title>
<link rel="stylesheet" href="./lesson-00.css?v=1"><script src="./lesson-00.js?v=1" defer></script>
</head><body><a class="skip-link" href="#lesson-content">直接閱讀正文</a>
<div class="reading-track" aria-hidden="true"><span id="reading-bar"></span></div>
<header class="reader-header"><a class="wordmark" href="./index.html">Industry Academy <small>產業與企業策略學院</small></a><a href="./index.html#lesson/0">← 返回課程導覽</a></header>
<div class="reader-layout"><aside class="reader-aside"><details id="lesson-toc"><summary>本堂目錄</summary><nav aria-label="本堂章節">'''+md.toc+'''</nav></details>
<div class="position-card"><span id="position-label" role="status">目前位置 0%</span><button id="resume-reading" type="button" hidden>回到上次位置</button><button id="mark-read" type="button">自行標記已讀</button><small>位置與標記僅保存在此瀏覽器；標記不代表測驗或審查通過。</small></div></aside>
<main id="lesson-content" class="reader" tabindex="-1"><div class="eyebrow">LESSON 00 · 基礎與工具</div><h1>什麼是產業</h1>
<p class="edition">2026年11月6日候選稿 · 約一萬字正文 · 可自由閱讀</p>
<div class="candidate-notice"><strong>教材候選稿・審閱中</strong><p>尚未完成獨立第二輪審讀；全球三項產業比率的加總口徑仍待核對，相關來源註記已保留。本頁供先行閱讀，尚未標示為正式發布。</p></div>
<p class="reader-hint">可由左側或上方目錄選讀；點按圖表可放大。無需完成測驗才能閱讀後續內容。</p>
<article class="lesson-text">'''+str(body)+'''</article>
<footer class="lesson-end"><a href="./index.html#lesson/0">← 返回第00堂導覽</a><a href="./lesson-01.html">延伸閱讀：第01堂 →</a></footer></main></div>
<dialog id="figure-viewer" aria-labelledby="figure-title"><form method="dialog"><button autofocus aria-label="關閉放大圖">關閉 ✕</button></form><h2 id="figure-title">圖表放大</h2><div class="zoom-scroll"><img id="zoom-image" alt=""></div></dialog>
<footer class="site-footer">Industry Academy · 全球與台灣的產業知識 · 教材候選稿</footer>
<!-- candidate-sha256: '''+sha+''' -->
</body></html>
'''
    (ROOT/'docs/lesson-00.html').write_bytes(html.encode('utf-8'))
    target=ROOT/'docs/assets/lesson-00';target.mkdir(parents=True,exist_ok=True)
    for p in src.parent.joinpath('figures').glob('*.svg'):shutil.copyfile(p,target/p.name)
    (ROOT/'research/requirements-site.txt').write_bytes(('Markdown=='+importlib.metadata.version('Markdown')+'\nbeautifulsoup4=='+importlib.metadata.version('beautifulsoup4')+'\n').encode())
    print('Built Lesson00 candidate reader; '+sha)
if __name__=='__main__':main()
