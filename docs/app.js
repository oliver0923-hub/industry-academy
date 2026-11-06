"use strict";
// Industry Academy v2.0: course numbers and boundaries follow the project source document.
const MODULES=[
{title:"基礎與工具",short:"產業研究基礎",icon:"◈",range:[0,4],desc:"建立市場、企業、資料與策略的分析語言"},
{title:"初級產業、基礎資源與公共設施",short:"資源與公共設施",icon:"♧",range:[5,9],desc:"糧食、關鍵資源、能源與基礎服務"},
{title:"核心製造、材料與傳統產業",short:"核心製造與材料",icon:"⚙",range:[10,17],desc:"從食品紡織到機械、材料與零組件"},
{title:"半導體、資訊電子與數位技術",short:"科技與數位產業",icon:"▤",range:[18,24],desc:"晶片、電子設備、軟體、通訊與 AI"},
{title:"運輸、建築、商貿與通路",short:"運輸、建築與商貿",icon:"⌁",range:[25,30],desc:"交通系統、物流、營建、不動產與零售"},
{title:"金融、商業服務與專業服務",short:"金融與專業服務",icon:"▥",range:[31,36],desc:"銀行、證券、廣告、顧問與企業服務"},
{title:"媒體、內容、文化與休閒",short:"文化、媒體與休閒",icon:"◉",range:[37,41],desc:"內容平台、遊戲、旅遊、運動與餐飲"},
{title:"民生、社會與公共服務",short:"民生與公共服務",icon:"✳",range:[42,46],desc:"醫療、生技、教育、生活與公共行政"},
{title:"產業變革與策略整合",short:"產業轉型與整合",icon:"↗",range:[47,49],desc:"能源轉型、企業擴張與總整合"}
];
const TITLES=[
"學院導覽：何謂產業？SIC、NAICS、台灣行業統計分類、證交所分類的差異",
"產業如何賺錢：商業模式、成本結構、附加價值、利潤、產值與市場規模",
"全球產業體系：國際分工、貿易、全球價值鏈、跨國企業、地緣政治",
"產業競爭與策略：IO/SCP、Porter、RBV、TCE、規模、網絡與定價",
"產業研究實務：官方資料庫、財報、產業報告、分類代碼、比率與研究設計",
"農業、畜牧、農業科技及食品原料：糧食安全、農企、台灣農業",
"漁業、養殖、林業與自然資源供應鏈：永續、出口與地方產業",
"礦業、關鍵礦物、金屬原料與全球資源安全：稀土、銅、鋰與台灣進口依賴",
"石油、天然氣、化石燃料與石化上游：產油國、煉製、台灣能源結構",
"電力、燃氣、水務、廢棄物與環境服務：公用事業、電網、循環經濟",
"食品加工、飲料、民生消費品與品牌製造",
"紡織、成衣、鞋類、皮革：國際品牌、機能布與台灣供應鏈",
"木材、家具、紙品、印刷、包裝與居家製造",
"塑膠、橡膠、基礎化學與特用化學：材料鏈與轉型",
"鋼鐵、非鐵金屬、水泥、玻璃、陶瓷與基礎建材",
"工業機械、自動化、工具機、工廠設備與工業服務",
"電機設備、電線電纜、家電與能源設備製造",
"一般製造、精密零件、光學與跨產業零組件供應鏈",
"半導體I：IC設計、晶圓代工、記憶體、封裝測試",
"半導體II：材料、設備、EDA、先進封裝與產業政策",
"電子製造：EMS、ODM、OEM、品牌、伺服器與電子供應鏈",
"電腦、消費電子、光電、顯示、感測及通信設備",
"電信、通訊網路、5G/6G、衛星與基礎通訊設施",
"軟體、IT服務、雲端、資安、企業資訊系統與SaaS",
"人工智慧、資料中心、算力服務、平台與數位基礎設施",
"汽車與電動車：整車、零件、電池、充電與交通轉型",
"航空航太、造船、鐵路、無人機與其他運輸設備",
"海運、航空運輸、陸運、倉儲、物流與供應鏈服務",
"營造工程、基礎建設、建築材料應用與工程承攬",
"不動產開發、仲介、租賃、物業管理與不動產金融",
"批發、零售、超商、百貨、電商、品牌通路與平台",
"銀行、存放款、支付、信用與金融科技",
"保險、證券、資產管理、私募股權與資本市場服務",
"廣告、媒體購買、數位廣告、行銷科技與品牌傳播",
"管理顧問、法律、會計、稅務、稽核與企業專業服務",
"工程顧問、建築設計、研發服務、檢測認證與市場研究",
"人力派遣、招募、保全、商用清潔、客服與企業支援服務",
"出版、新聞、影視、音樂、串流與內容平台",
"遊戲、電競、動畫、IP授權與互動娛樂",
"運動、健身、展演、藝文、博物館與休閒設施",
"觀光、旅行社、旅館、民宿與旅遊平台",
"餐飲、連鎖服務、外送平台與餐飲加盟",
"醫療體系、醫院、診所、健康照護與社會工作服務",
"製藥、生技、醫療器材、CRO、CDMO與臨床研發",
"教育、補習、職業培訓、線上教育與EdTech",
"個人及家庭服務：美容、美髮、維修、洗衣、照護與生活服務",
"公共行政、國防與公共採購市場：政府如何塑造產業與需求",
"能源轉型與跨產業綠色供應鏈：再生能源、儲能、碳管理",
"企業集團、總部、控股、多角化、策略聯盟、併購與全球擴張",
"產業轉型總整合：全球與台灣比較、危機情境、CEO資源配置與研究設計"
];
const COURSES=TITLES.map((title,id)=>({id,title,module:MODULES.findIndex(m=>id>=m.range[0]&&id<=m.range[1])}));
const storageKey="industry-academy-v2-completed";
let completed=new Set();
try{const stored=JSON.parse(localStorage.getItem(storageKey)||"[]");if(Array.isArray(stored))completed=new Set(stored.filter(n=>Number.isInteger(n)&&n>=0&&n<50));}catch(_){}
const $=(id)=>document.getElementById(id);
const escapeHTML=(str)=>String(str).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const n2=(n)=>String(n).padStart(2,"0");
const moduleCourses=(i)=>COURSES.filter(c=>c.module===i);
const heroArt='<svg viewBox="0 0 520 420" role="img" aria-label="抽象全球產業和城市線條插畫"><defs><linearGradient id="sky" x1="0" x2="1"><stop stop-color="#b7ddf3"/><stop offset="1" stop-color="#7dbce0"/></linearGradient></defs><circle cx="299" cy="184" r="156" fill="none" stroke="#98cae7" stroke-width="1.5" stroke-dasharray="6 7"/><circle cx="299" cy="184" r="118" fill="none" stroke="#a5d3ed" stroke-width="1"/><path d="M80 312h425M112 312V221l60-30v121M184 312V160l69-26v178M267 312V110l76 29v173M358 312V200l52-35v147M425 312V239l45-19v92" fill="#d5ecf9" stroke="#82b9d8" stroke-width="2"/><path d="M198 181v119m19-126v126m19-134v134m50-158v157m22-149v149m22-142v142" stroke="#a0cbe3" stroke-width="3" stroke-dasharray="10 11"/><path d="M76 321l79-55 81 20 92-91 75 34 93-100" stroke="#51a4cf" stroke-width="3" fill="none"/><circle cx="155" cy="266" r="7" fill="#fff" stroke="#4f9fc7" stroke-width="3"/><circle cx="328" cy="195" r="7" fill="#fff" stroke="#4f9fc7" stroke-width="3"/><circle cx="496" cy="129" r="7" fill="#fff" stroke="#4f9fc7" stroke-width="3"/><path d="M105 365h351" stroke="#7db7db" stroke-width="1.5" stroke-dasharray="5 6"/></svg>';
function persist(){try{localStorage.setItem(storageKey,JSON.stringify([...completed].sort((a,b)=>a-b)));}catch(_){}}
function progress(){const count=completed.size;$("progress-count").textContent=count+" / 50";$("progress-fill").style.width=(count/50*100)+"%";$("progress-percent").textContent=Math.round(count/50*100)+"%";}
function renderSidebar(active){$("sidebar-modules").innerHTML=MODULES.map((m,i)=>'<a class="module-link '+(active==="module/"+i?"active":"")+'" href="#module/'+i+'"><span class="module-no">'+n2(m.range[0])+'</span><span>'+escapeHTML(m.short)+'</span></a>').join("");document.querySelectorAll(".quick-link").forEach(x=>x.classList.toggle("active",x.dataset.route===active));}
function moduleCard(m,i){return '<a class="module-card" href="#module/'+i+'"><div class="card-top"><span class="card-icon" aria-hidden="true">'+m.icon+'</span><span class="card-count">'+moduleCourses(i).length+' 堂課</span></div><h3>'+escapeHTML(m.short)+'</h3><p>'+escapeHTML(m.desc)+'</p><div class="card-bottom"><span>'+n2(m.range[0])+' — '+n2(m.range[1])+' / 課程</span><span class="card-arrow">↗</span></div></a>';}
function home(){return '<section class="hero"><div class="hero-content"><div class="eyebrow">THE INDUSTRY ACADEMY</div><h1>讀懂全球產業，<br/><em>看見台灣的競爭力。</em></h1><p>從一件商品、一筆交易，到全球供應鏈與企業策略。用 50 堂循序漸進的課，建立理解產業運作的完整視野。</p><div class="hero-actions"><a class="btn btn-primary" href="#catalog">探索全部課程 <span>↗</span></a><a class="btn btn-secondary" href="#lesson/0">從第 00 堂開始 →</a></div></div><div class="hero-art">'+heroArt+'</div></section><section class="stats-strip" aria-label="學院概要"><div class="stat"><strong>50</strong><small>跨產業核心課程</small></div><div class="stat"><strong>09</strong><small>主題學習群組</small></div><div class="stat"><strong>Global</strong><small>從全球市場出發</small></div><div class="stat"><strong>Taiwan</strong><small>走進在地企業策略</small></div></section><div class="section-heading"><div><div class="section-kicker">EXPLORE BY INDUSTRY</div><h2>從感興趣的產業開始</h2><p>不必按照固定順序。每個模組都連結全球市場、台灣產業與個別企業。</p></div><a class="see-all" href="#catalog">查看 50 堂完整目錄 ↗</a></div><div class="module-grid">'+MODULES.map(moduleCard).join("")+'</div><div class="feature-row"><div class="feature-panel"><div class="mini-label">OUR LEARNING METHOD</div><h3>全球視野 × 台灣脈絡 × 管理決策</h3><p>不是單純背誦產業排名，而是理解每個產業如何創造價值、如何競爭，以及企業面對不確定性時為何做出不同選擇。</p><div class="step-pills"><span>全球產業地圖</span><span>台灣產業位置</span><span>企業案例</span><span>策略模擬</span></div></div><div class="feature-panel"><div class="mini-label">START WITH THE BASICS</div><h3>不知道怎麼開始？</h3><p>先從第 00 堂認識產業分類，再到第 01 堂理解收入、成本與利潤，為後續所有產業建立共同語言。</p><a href="#lesson/0" class="btn btn-secondary">了解基礎課程 →</a></div></div>';}
function courseItem(c){return '<a class="course-item" href="#lesson/'+c.id+'"><span class="course-number">'+n2(c.id)+'</span><span><span class="course-title">'+escapeHTML(c.title)+'</span><span class="course-meta">'+escapeHTML(MODULES[c.module].title)+'</span></span><span class="course-status '+(completed.has(c.id)?"completed":"")+'">'+(completed.has(c.id)?"✓ 已標記":c.id===0?"候選稿・審閱中":c.id===1?"編輯審查中":"課程介紹")+'</span></a>';}
function catalog(filter="all",query=""){const filtered=COURSES.filter(c=>(filter==="all"||String(c.module)===filter)&&(!query||c.title.toLowerCase().includes(query.toLowerCase())||MODULES[c.module].title.toLowerCase().includes(query.toLowerCase())||n2(c.id).includes(query)));return '<section class="inner-hero"><div class="eyebrow">COURSE DIRECTORY</div><h1>完整課程目錄</h1><p>涵蓋製造、農業、資源、數位科技、金融、教育、醫療與公共服務。課程編號依 Industry Academy v2.0 規劃。</p></section><div class="catalog-tools"><label class="search-wrap"><input id="search" type="search" placeholder="搜尋產業、主題或課號…" value="'+escapeHTML(query)+'" aria-label="搜尋課程"></label><div class="filter-row"><button class="filter '+(filter==="all"?"active":"")+'" data-filter="all">全部 50 堂</button><button class="filter '+(filter==="0"?"active":"")+'" data-filter="0">基礎</button><button class="filter '+(filter==="3"?"active":"")+'" data-filter="3">科技</button><button class="filter '+(filter==="5"?"active":"")+'" data-filter="5">金融服務</button></div></div><div id="course-results" class="course-list">'+(filtered.length?filtered.map(courseItem).join(""):'<div class="empty">沒有符合條件的課程，試試其他關鍵字。</div>')+'</div>';}
function modulePage(i){const m=MODULES[i];return '<section class="inner-hero"><div class="eyebrow">MODULE '+n2(i+1)+' / INDUSTRY EXPLORATION</div><h1>'+escapeHTML(m.title)+'</h1><p>'+escapeHTML(m.desc)+'。本主題包含第 '+n2(m.range[0])+' 至 '+n2(m.range[1])+' 堂，可自由挑選單堂課。</p><a class="btn btn-secondary" href="#catalog">← 返回完整課程</a></section><div class="section-heading"><div><div class="section-kicker">COURSE LIST</div><h2>'+moduleCourses(i).length+' 堂課程</h2></div></div><div class="course-list">'+moduleCourses(i).map(courseItem).join("")+'</div>';}
function lessonPage(id){const c=COURSES[id],m=MODULES[c.module];return '<div class="course-detail"><section class="inner-hero"><div class="eyebrow">LESSON '+n2(id)+' / '+escapeHTML(m.short)+'</div><h1>'+escapeHTML(c.title)+'</h1><p>本堂將以全球產業為起點，連結台灣的產業結構、企業實務、競爭挑戰及相關學術研究。</p></section>' +(id===1?'<div class="notice"><h3>第 01 堂教材 · 編輯審查中</h3><p>已建立可閱讀的敘事型課文草稿：從便當的收入與成本出發，解釋市場規模、附加價值與 GDP 的差異，並比較食品、晶片及銀行的財報口徑。學術參考來源與教學情境已附於文末。企業多年趨勢、完整引用細查與出版級第二輪審讀仍待補足；目前不標記為正式出版。</p><a class="btn btn-primary" href="./lesson-01.html">閱讀第 01 堂課文草稿 →</a></div>':id===0?'<div class="notice"><h3>第 00 堂教材 · 編輯審查中</h3><p>從一份早餐出發，理解企業、產業分類、產品市場、價值鏈，以及全球與台灣產業結構。約一萬字候選稿附三張圖、來源與練習；獨立第二輪審讀及全球統計加總口徑仍待完成，尚未正式發布。</p><a class="btn btn-primary" href="./lesson-00-reading-v2.html">閱讀第 00 堂教材候選稿 →</a></div>':'<div class="notice"><h3>課程頁面已建立 · 正式教材編寫中</h3><p>目前是學院首頁與課程導覽的第一版。此頁尚未放入完整講義、可驗證的市場數據、學術引用、測驗或三回合決策模擬。後續完成內容時，將依照專案 v2.0 的 11 個必要段落逐堂發布。</p></div>')+'<div class="section-heading"><div><div class="section-kicker">LEARNING FRAMEWORK</div><h2>每堂課都會經過的三個視角</h2></div></div><div class="learning-points"><div class="learning-point"><b>01 · 全球產業</b>產業歷史、市場分工、價值鏈、需求與成本結構。</div><div class="learning-point"><b>02 · 台灣與企業</b>台灣的產業位置、公司案例、競爭與政策環境。</div><div class="learning-point"><b>03 · 管理與研究</b>決策情境、理論解釋、研究證據及反例。</div></div><div class="lesson-actions"><button id="toggle-complete" class="btn '+(completed.has(id)?"btn-secondary":"btn-primary")+'">'+(completed.has(id)?"✓ 已標記完成，點此取消":"標記已閱讀此課程介紹")+'</button><a class="btn btn-secondary" href="#module/'+c.module+'">返回模組課程 →</a></div><p style="font-size:11px;color:#89a0ad;line-height:1.9">「已閱讀」僅代表你查看了這份課程介紹，不代表已完成正式教材。學習狀態只儲存在目前瀏覽器。</p></div>';}
function pathways(){const paths=[{name:"第一次認識產業",course:"00 → 01 → 02 → 03 → 04",desc:"先理解產業如何分類、如何賺錢，以及國際分工和企業競爭。",start:0},{name:"台灣製造與科技競爭",course:"15 → 17 → 18 → 19 → 20 → 24",desc:"從工具機與零組件，連結半導體、電子製造與 AI 基礎設施。",start:15},{name:"服務業與商業模式",course:"30 → 31 → 33 → 37 → 40 → 41",desc:"追蹤通路、金融、廣告、媒體、觀光與餐飲的收入模式。",start:30}];return '<section class="inner-hero"><div class="eyebrow">LEARNING PATHWAYS</div><h1>依照你的好奇心安排學習</h1><p>這些是建議的跨產業學習順序，不是強制先修條件；也可以從任意產業直接開始。</p></section><div class="pathway-list">'+paths.map(p=>'<div class="pathway"><h3>'+p.name+'</h3><p>'+p.desc+'</p><p class="pathway-tags">第 '+p.course+' 堂</p><a href="#lesson/'+p.start+'" class="btn btn-secondary">開啟第一個課程 →</a></div>').join("")+'</div>';}
let catalogFilter="all",catalogQuery="";
function render(){const hash=decodeURIComponent(location.hash.slice(1)||"home");const main=$("main");let page="學院首頁",active="home";if(hash==="home"){main.innerHTML=home();}else if(hash==="catalog"){active="catalog";page="全部課程";main.innerHTML=catalog(catalogFilter,catalogQuery);}else if(hash==="pathways"){active="pathways";page="學習路徑";main.innerHTML=pathways();}else if(/^module\/\d+$/.test(hash)){const i=Number(hash.split("/")[1]);if(MODULES[i]){active="module/"+i;page=MODULES[i].short;main.innerHTML=modulePage(i);}else{location.hash="#catalog";return;}}else if(/^lesson\/\d+$/.test(hash)){const id=Number(hash.split("/")[1]);if(COURSES[id]){active="module/"+COURSES[id].module;page="第 "+n2(id)+" 堂";main.innerHTML=lessonPage(id);}else{location.hash="#catalog";return;}}else{location.hash="#home";return;}$("breadcrumb-page").textContent=page;renderSidebar(active);progress();document.body.classList.remove("menu-open");$("menu-button").setAttribute("aria-expanded","false");if(hash==="catalog"){const search=$("search");search.addEventListener("input",()=>{catalogQuery=search.value;updateCatalog()});document.querySelectorAll("[data-filter]").forEach(b=>b.addEventListener("click",()=>{catalogFilter=b.dataset.filter;updateCatalog();document.querySelectorAll("[data-filter]").forEach(x=>x.classList.toggle("active",x.dataset.filter===catalogFilter))}));}const toggle=$("toggle-complete");if(toggle){toggle.addEventListener("click",()=>{const id=Number(location.hash.split("/")[1]);if(completed.has(id))completed.delete(id);else completed.add(id);persist();render();});}}
function updateCatalog(){const result=$("course-results");if(!result)return;const filtered=COURSES.filter(c=>(catalogFilter==="all"||String(c.module)===catalogFilter)&&(!catalogQuery||c.title.toLowerCase().includes(catalogQuery.toLowerCase())||MODULES[c.module].title.toLowerCase().includes(catalogQuery.toLowerCase())||n2(c.id).includes(catalogQuery)));result.innerHTML=filtered.length?filtered.map(courseItem).join(""):'<div class="empty">沒有符合條件的課程，試試其他關鍵字。</div>';}
$("menu-button").addEventListener("click",()=>{const open=document.body.classList.toggle("menu-open");$("menu-button").setAttribute("aria-expanded",String(open));});$("sidebar-backdrop").addEventListener("click",()=>document.body.classList.remove("menu-open"));window.addEventListener("hashchange",()=>{render();window.scrollTo({top:0,behavior:"instant"});});render();