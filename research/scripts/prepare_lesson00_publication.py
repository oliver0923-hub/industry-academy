"""產出Lesson00查核索引與原創圖；教材正文與審讀由人工編輯，不覆寫。"""
from pathlib import Path
import csv,json,hashlib,re
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'research/editorial/lesson-00'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    old={r['source_id']:r for r in read(ROOT/'research/evidence/teaching-foundation-2026-11-06/sources.csv')}
    tasks={r['task_id']:r for r in read(ROOT/'research/sources/acquisition_tasks.csv')}
    states={r['task_id']:r for r in read(ROOT/'research/sources/acquisition_state.csv')}
    sources=[]
    selections={
        'TW12':('V2_TW12_MANUAL','PDF4,6–10；68–69（分類定義）','2025-12-12 announcement;2026 effective'),
        'NAICS':('D_1cb5b0c805ae','PDF5–6；15–16 / printed3–4,13–14','2022'),
        'UN':('L00_UN_ISIC','Introduction paragraphs1–4；Revision5 first paragraphs','undated; accessed2026-11-06'),
        'TWSE':('L00_TWSE','2025-06-09 revision; points1–5','2025-06-09'),
        'FTC':('L00_FTC_MARKET','points2–7；9 final paragraph；revision date header','2023-11-22'),
        'GDP_DEF':('L00_DGBAS_CONCEPTS','PDF1–3 / printed94–96；PDF8–9 exports adjustments','113年年報；獨立出版日未列於分檔'),
        'TW_STRUCTURE':('L00_DGBAS_STRUCTURE','PDF1–3；structure paragraph and Figure4 PDF3','113年年報；獨立出版日未列於分檔'),
        'RETAIL':('T_MOEA_RETAIL24','PDF2–3 tables2–3 and statistical classification note','2025-01-23'),
        'TSMC98':('T_TSMC_1998','Company Profile entire substantive text','1998 report; HTML publication date not stated'),
        'WM_HISTORY':('T_WALMART_HISTORY','1962,1983,1988,1991 timeline entries','undated; accessed2026-11-06'),
        'WM_FIN':('D_F023','PDF43 / printed41 financial table and explanatory paragraph','2024'),
        'TYSON':('S_tyson_10k_2024','PDF4 / printed3 Item1 General；integrated chicken and contract farmers','2024'),
        'COASE':('S_coase_university','printed388–394 / PDF4–10; prior OCR and page images; core reread','1937'),
        'GVC':('S_gvc_journal_2005','printed83–87,97–99 / PDF6–10,20–22; prior card and selected core reread','2005'),
    }
    for k in ['AGR','IND','SRV']:
        selections['WDI_'+k]=('L00_WDI_'+k,'JSON metadata lastupdated; records(countryiso3code=WLD,date=2024)','2026-10-08 dataset update')
        selections['META_'+k]=('L00_META_'+k,'Indicator Name；Short/Long definition；Source；Aggregation method；Limitations；License','undated; accessed2026-11-06')
    for sid,(key,scope,pub) in selections.items():
        if key in states:
            r=states[key];t=tasks[key];title=t['title'];url=t['url'];path=r['local_path'];sha=r['sha256'];rights=t['license'];identity=t['issuer'];status=r['status']
        else:
            r=old[key];title=r['title'];url=r['url'];path=r['local_private_path'];sha=r['sha256'];rights=r['rights'];identity=r['identity'];status='reused_prior_original'
        if status not in ['downloaded','reused_existing','reused_prior_original']:raise ValueError((key,status))
        sources.append(dict(source_id=sid,repository_source_id=key,title=title,url=url,publication_or_version_date=pub,identity=identity,local_private_path=path,sha256=sha,status='fulltext_read',read_scope=scope,rights=rights,accessed_at='2026-11-06'))
    o=json.loads((ROOT/'private_sources/lesson00-qa/wdi-gdp-definition-origin.json').read_text(encoding='utf-8'))
    sources.append(dict(source_id='WDI_GDP_DEF',repository_source_id='lesson00_supplemental_metadata',title='World Bank GDP current US$ indicator metadata',url=o['url'],publication_or_version_date='metadata accessed2026-11-06',identity='World Bank WDI official API metadata',local_private_path=o['local_private_path'],sha256=o['sha256'],status='fulltext_read',read_scope='JSON[1][0].sourceNote: GDP three approaches and current-price meaning; no residual explanation inferred',rights='Public metadata; original private',accessed_at='2026-11-06'))
    # 逐主張標記事實、條件推論、假設例；anchor須在正文原樣存在。
    facts=[
        ('S06','F37','WDI_GDP_DEF','名目值（nominal value）','definition snapshot2026-11-06','JSON[1][0].sourceNote','current prices explicitly means no adjustment for price changes over time','不將此定義當世界三部門殘差分解；實質值說明為相對名目概念'),
        ('S02','F35','META_SRV','包含公共行政、教育與醫療等活動','metadata snapshot2026-11-06','Short/Long definition','服務活動含公共行政、教育醫療等，非僅上市公司','未用企業營收代替非市場服務衡量'),
        ('S02','F36','GDP_DEF','家庭內自給的育兒與家務服務','113年國民所得年報','PDF2 / printed95 國民所得統計之範圍','自給農產品估價，未付酬家庭家務與照顧服務未計入同範圍','統計生產邊界不是生活重要性的完整評分'),
        ('S02','F01','TW12','企業可以包含多個場所，而這些場所從事的主要活動可能相同','2026','PDF7–8 / printed2–3 統計單位','企業與場所區分，場所為主要活動分類基礎','不得把品牌、公司、集團當作相同統計單位'),
        ('S02','F02','TW12','主要經濟活動以附加價值最大者判斷','2026','PDF8–9 / printed3–4 行業判定','主要活動與產出、投入替代指標','零售買賣差價非直接等於完整附加價值'),
        ('S03','F03','FTC','需求替代是界定相關市場的主要考量','2023 revision','points2–4,7','功能特性用途價格、需求與供給替代，主要考量需求','具體市場需要個案證據；咖啡例非法律認定'),
        ('S03','F04','FTC','運輸成本、取得便利性、交易成本與相關法規','2023 revision','points3,5','地理市場及時間因素、法規與交易條件','沒有推定任何實際市場邊界'),
        ('S03','F05','FTC','轉換成本（switching costs）','2023 revision','point4(6)；point7','判斷替代性時考量轉換成本與個案事實','列舉的學習、資料搬移等為一般說明，非量化調查'),
        ('S04','F06','UN','最初版本於1948年採用','1948;2023','Introduction paragraph3；Revision5 paragraph1','ISIC起源及第五次修訂2023年認可','不把認可日當作所有國家共同實施日'),
        ('S04','F07','NAICS','1937年美國成立跨部會委員會','1937–1987','PDF15 / printed13 Background','1937委員會；1938製造及1939非製造清單；1987最後SIC修訂','歷史美國SIC；非所有同縮寫制度'),
        ('S04','F08','NAICS','美國統計於1997年首次使用','1997;2022','PDF15–16 / printed13–14','NAICS三國合作、供給／生產導向與首次統計實施','2022版本，未宣稱2027待實施版本已取代'),
        ('S04','F09','TW12','台灣於1967年參照國際分類及國情','1967;1971','PDF6 / printed1 前言','56年試行、60年第1次修訂擴為四層','民國年轉西元；不是台灣經濟活動1967才開始'),
        ('S04','F10','TW12','20個大類、88個中類、254個小類及530個細類','2026-01-01','PDF4行政院函；PDF6前言','第12次修正分類數及生效日期','舊版統計不自動重新編製'),
        ('S04','F11','TW12','改依商品種類歸類，並保留零售攤販的特定架構','2026','PDF7 / printed2 原則(四)','零售線上線下不再為主要分類方式，保留486小類','不是線上銷售消失或銷售方式無經濟差異'),
        ('S04','F12','TWSE','2025年6月9日修正版列有','2025-06-09','points1–5；page revision date','上市公司用途、33類及收入等分類考量、定期調整','未把簡述當成完整法規適用意見'),
        ('S04','F13','NAICS','北美三國能比較到的層級因行業而異','2022','PDF6 / printed4 comparability','有些只到2、3或4碼可比，不是全部5/6碼','沒有自造碼對碼crosswalk'),
        ('S04','F14','TW12','統計用途與行政管理','2026','PDF4 announcement point3；PDF7 first paragraph','非統計管制應依目的自行認定','不以統計碼決定勞動、投資等法規適用'),
        ('S05','F15','TYSON','育種、契約農戶、飼料生產、加工、行銷與運輸','FY2024-09-28','PDF4 / printed3 Item1 General','雞肉整合流程列contract farmers','雞肉而非全部肉品；不代表契約農場均自有'),
        ('S05','F16','COASE','尋找價格、協商及訂立契約本身有成本','theory1937','printed388–394 / PDF4–10','市場交易有成本，企業內協調也有邊際成本','理論不是本文假設店家的實際動機或量化估計'),
        ('S05','F17','GVC','交易的複雜度、資訊能否清楚編碼','theory2005','printed83–87,97–99 / PDF6–10,20–22','三變數與治理類型及動態限制','非因果估計，未把產業一律判成單一治理型'),
        ('S06','F18','GDP_DEF','產出價值減去中間消費','113年國民所得年報','PDF2–3 / printed95–96 production definitions','產出與中間消費、附加價值及毛額淨額','正文例是另造教學假設，不是官方例的實際估計'),
        ('S06','F19','GDP_DEF','生產、所得與支出相互連接的架構','113年國民所得年報','PDF1–3 / printed94–96','SNA架構與生產所得支出及毛額概念','不是公司收入或福利的完整衡量'),
        ('S06','F20','RETAIL','4兆8,530億元','2024','PDF2 表2；PDF3 表3；PDF1日期','零售48,530億元；網路6,533億元；13.5%','2025-01-23版本、TW11、營業額不是附加價值'),
        ('S06','F21','TW12','通路、付款技術與主要經濟活動','2026','PDF7–9 / printed2–4','營運方式及電子商務不自動決定主要活動','網路銷售不是僅電子購物及郵購業'),
        ('S06','F22','GDP_DEF','國民經濟會計另依常住性、所有權等原則調整','113年國民所得年報','PDF8–9 / printed101–102','國民經濟會計出口與海關貿易之調整','不能把所有跨境貨物當作同一國民帳出口'),
        ('S07','F23','WDI_AGR','農林漁業約為4.1%','2024','JSON[0].lastupdated;JSON[1] WLD/2024','raw4.07045929837122% rounded1decimal','世界加權彙總；非農產品產值比重'),
        ('S07','F24','WDI_IND','工業約25.4%','2024','JSON[0].lastupdated;JSON[1] WLD/2024','raw25.435604452787% rounded1decimal','工業包含營造；不可改名製造'),
        ('S07','F25','WDI_SRV','服務業約63.3%','2024','JSON[0].lastupdated;JSON[1] WLD/2024','raw63.3018068599679% rounded1decimal','未重算三系列至100%；不把差額自造為其他業'),
        ('S07','F26','META_IND','工業包括營造','metadata snapshot2026-11-06','Short/Long definition;Aggregation method','ISIC4 divisions05–43；weighted average','三系列世界彙總殘差未作逐項調和，明標待核對'),
        ('S07','F27','TW_STRUCTURE','2024年農業1.5%、工業40.4%、服務業58.1%','2015;2024','PDF3 Figure4及產業結構段','2015:1.8/36.3/62.0；2024:1.5/40.4/58.1；製造31.4→35.7','同年報圖4原口徑；與WDI不直接混作精確差額比較'),
        ('S08','F28','TW12','某些免費線上服務以廣告取得營收','2026','PDF9 / printed4 point3','收入代理指標可能誤分類；可看勞動與資本投入','不是所有廣告收入企業都一律歸某碼'),
        ('S08','F29','FTC','一群使用者如何影響另一群使用者取得的價值','2023 revision','point2(6)–(7);point4(4)','多邊市場與間接網路效應定義','不假定所有平台都天然形成壟斷'),
        ('S09','F30','TSMC98','公司於1987年在新竹成立','1987;1998','Company Profile opening and charter paragraphs','專業代工定位、章程自有品牌IC限制','1998公司自述；不是普遍法律義務或現今排名'),
        ('S09','F31','TSMC98','兩座六吋、三座八吋晶圓廠','1998','Company Profile fabrication facilities paragraph','年產能1.6million8-inch equivalent wafers','產能非出貨；不同尺寸不可直接加片數'),
        ('S09','F32','TSMC98','WaferTech開始量產','1998','Company Profile WaferTech paragraph','mid1998 volume production','新加坡2000為當時預期，故不寫成已發生'),
        ('S09','F33','WM_HISTORY','第一家店於1962年','1962;1983;1988;1991','History timeline four event years','Rogers首店、Sam’s Club、Supercenter、Cifra合作墨西哥','公司自述，不證明事件造成之績效'),
        ('S09','F34','WM_FIN','總營收648,125百萬美元、淨銷售642,637百萬美元','FY ended2024-01-31','PDF43 / printed41 table and first paragraph','收入兩列及會員與其他收益、營業利益27,012','全球合併USGAAP；不與台灣GDP直接比較'),
    ]
    sm={s['source_id']:s for s in sources};cs=[]
    for sec,cid,sid,anchor,year,loc,support,limit in facts:
        s=sm[sid];cs.append(dict(claim_id=cid,section_id=sec,candidate_anchor=anchor,claim_type='sourced_fact_or_theory',source_id=sid,source_name=s['title'],original_url=s['url'],publication_year=s['publication_or_version_date'],data_year=year,precise_locator=loc,supporting_content=support,status='claim_verified',scope_limit=limit))
    for sec,cid,anchor,kind,reason in [
        ('S01','E01','先想像一個教學情境','teaching_hypothesis','早餐人物、店家、原料品牌均未當作真實事件'),
        ('S03','E02','假設你原本打算買一杯咖啡','teaching_hypothesis','例示可能替代而非觀察資料或法律認定'),
        ('S05','E03','在一個假設的食品訂單中','teaching_hypothesis','付款、庫存和資金壓力取決於假設合約'),
        ('S06','E04','20、15、30與35元','teaching_hypothesis','假設沒有其他外購中間投入；20+15+30+35=100，並非官方實際資料'),
        ('S07','E05','名目生產從100增加到110','conditional_reasoning','占比下降不等於絕對值下降之比例例，未宣稱台灣某年如此'),
        ('S08','E06','平均成本便可能下降','conditional_reasoning','固定期間與品質條件；不宣稱任何產業特定成本係數'),
        ('S09','E07','可能讓顧客一次完成更多採買','conditional_reasoning','業態組合的分析問題，不把Walmart歷史作因果識別'),
        ('S10','E08','一家早餐店原本由顧客到店購買','teaching_hypothesis','課末假設情境不是真實企業紀錄')]:
        cs.append(dict(claim_id=cid,section_id=sec,candidate_anchor=anchor,claim_type=kind,source_id='AUTHOR_EXPOSITION',source_name='原創教學情境／條件推導',original_url='',publication_year='2026',data_year='not empirical',precise_locator=sec,supporting_content=reason,status=kind,scope_limit='不可轉述為實際統計、訪談或已識別因果關係'))
    write('sources.csv',sources);write('claim_to_source.csv',cs)
    obs=[]
    for k in ['AGR','IND','SRV']:
        r=states['L00_WDI_'+k];a=json.loads((ROOT/r['local_path']).read_text(encoding='utf-8'))
        for v in a[1]:obs.append(dict(observation_id='WDI_'+k+'_'+v['countryiso3code'],source_id='WDI_'+k,indicator=v['indicator']['id'],geography=v['countryiso3code'],data_year=v['date'],value='' if v['value'] is None else v['value'],unit='percent_of_GDP',version=a[0]['lastupdated'],status='missing_not_zero' if v['value'] is None else 'original_value_verified',scope_limit='industry includes construction; values not normalized; USA2024 null not replaced with another year'))
    for year,vals in [('2015',[1.8,36.3,62.0]),('2024',[1.5,40.4,58.1])]:
        for sector,val in zip(['agriculture','industry','services'],vals):obs.append(dict(observation_id='TW_'+sector+'_'+year,source_id='TW_STRUCTURE',indicator='yearbook_Figure4_'+sector,geography='Taiwan',data_year=year,value=val,unit='percent_yearbook_structure',version='113年國民所得年報 Figure4',status='original_value_verified',scope_limit='published chart basis and rounding; not reconciled to WDI denominator'))
    for year,val in [('2015',31.4),('2024',35.7)]:obs.append(dict(observation_id='TW_manufacturing_'+year,source_id='TW_STRUCTURE',indicator='yearbook_Figure4_manufacturing',geography='Taiwan',data_year=year,value=val,unit='percent_yearbook_structure',version='113年國民所得年報 Figure4',status='original_value_verified',scope_limit='manufacturing is a component of industry; not an additional sector'))
    write('observations.csv',obs)
    figures=[dict(figure_id='FIG1',file='figures/food-network.svg',kind='conceptual',purpose='食品活動與支援服務不只一條直線',sources='TW12;GVC',claim_ids='F01;F17',license='Original design; no third-party image copied',limitation='非特定公司供應網絡；非按流量比例'),dict(figure_id='FIG2',file='figures/value-added.svg',kind='teaching_hypothesis',purpose='分辨商品交易金額與新增價值',sources='GDP_DEF',claim_ids='F18;E04',license='Original design and hypothetical numbers',limitation='假設外購其他中間投入為零；非實際成本'),dict(figure_id='FIG3',file='figures/taiwan-structure.svg',kind='official_statistics_redrawn',purpose='台灣農工服務名目結構的兩年對照',sources='TW_STRUCTURE',claim_ids='F27',license='Original redrawing of factual values; cite DGBAS',limitation='不與WDI混合，不另加製造業，不消除四捨五入')]
    write('figure_plan.csv',figures)
    make_figures()
    print(json.dumps({'sources':len(sources),'verified_claims':len(facts),'hypotheses_and_reasoning':len(cs)-len(facts),'observations':len(obs),'figures':len(figures)}))

def make_figures():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    from matplotlib.patches import FancyBboxPatch
    font=Path('C:/Windows/Fonts/msjh.ttc')
    if font.exists():fm.fontManager.addfont(str(font));family=fm.FontProperties(fname=str(font)).get_name()
    else:family='Noto Sans CJK TC'
    plt.rcParams.update({'font.family':family,'svg.fonttype':'path','svg.hashsalt':'industry-academy-lesson00-v1','axes.unicode_minus':False})
    out=OUT/'figures';out.mkdir(exist_ok=True)
    qa=ROOT/'private_sources/lesson00-qa';qa.mkdir(exist_ok=True)
    def save(fig,name):
        fig.savefig(out/(name+'.svg'),bbox_inches='tight',facecolor='white',metadata={'Date':None,'Creator':'Industry Academy original redraw'})
        svg=out/(name+'.svg')
        svg.write_bytes(b'\n'.join(line.rstrip() for line in svg.read_bytes().splitlines())+b'\n')
        fig.savefig(qa/(name+'.png'),bbox_inches='tight',dpi=140,facecolor='white');plt.close(fig)
    def box(ax,x,y,text,w=1.5,h=.65):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.05',fc='#edf4f7',ec='#24536b'));ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=12)
    fig,ax=plt.subplots(figsize=(11,3.9));ax.set(xlim=(0,10),ylim=(0,3));ax.axis('off')
    ax.text(5,2.8,'食物相關活動與支援服務',ha='center',fontsize=18,weight='bold')
    for i,t in enumerate(['原料生產','加工製作','物流配送','零售／餐飲','消費者']):
        x=.3+i*1.95;box(ax,x,1,t)
        if i<4:ax.annotate('',xy=(x+1.85,1.32),xytext=(x+1.52,1.32),arrowprops={'arrowstyle':'->','color':'#24536b'})
    box(ax,.3,.1,'設備、能源、金融與資訊等支援活動',w=9.3,h=.55)
    for x in [1.05,3.2,5.2,7.2]:ax.annotate('',xy=(x,.95),xytext=(x,.7),arrowprops={'arrowstyle':'->','color':'#718592'})
    ax.text(5,2.12,'概念示意：箭頭僅表示活動連接，非交易量與利潤比例',ha='center',fontsize=10,color='#46545a')
    save(fig,'food-network')
    fig,ax=plt.subplots(figsize=(11,4.0));ax.set(xlim=(0,10),ylim=(0,3.2));ax.axis('off')
    ax.text(5,2.95,'同一件商品，不能把沿途收入都當作新增價值',ha='center',fontsize=16,weight='bold')
    for i,(t,v,inc) in enumerate(zip(['原料','加工','烘焙','零售'],[20,35,65,100],[20,15,30,35])):
        x=.3+i*2.5;box(ax,x,1.3,t+'\n交易 '+str(v)+' 元',w=1.9,h=.9);ax.text(x+.95,.85,'新增 '+str(inc)+' 元',ha='center',fontsize=13,color='#15655d')
        if i<3:ax.annotate('',xy=(x+2.38,1.75),xytext=(x+1.95,1.75),arrowprops={'arrowstyle':'->','color':'#24536b'})
    ax.text(5,.35,'教學假設｜新增價值合計 100 元；其他外購中間投入等已省略',ha='center',fontsize=11)
    save(fig,'value-added')
    fig,ax=plt.subplots(figsize=(10,4.8));ys=[2,1,0];a=[1.8,36.3,62];b=[1.5,40.4,58.1]
    ax.barh([y+.18 for y in ys],a,height=.3,label='2015',color='#92acba');ax.barh([y-.18 for y in ys],b,height=.3,label='2024',color='#24536b')
    for vals,offset in [(a,.18),(b,-.18)]:
        for y,v in zip(ys,vals):ax.text(v+.7,y+offset,f'{v:.1f}%',va='center',fontsize=11)
    ax.set(yticks=ys,yticklabels=['農業','工業（含製造業）','服務業'],xlim=(0,72),xlabel='年報圖4之名目產業結構比重（%）',title='台灣產業結構：2015 與 2024')
    ax.legend(loc='lower right');ax.spines[['right','top']].set_visible(False);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    fig.text(.14,-.04,'來源：主計總處113年國民所得年報〈國內生產與結構變動〉PDF3，圖4。\n自行重繪；製造業已含於工業；沿用年報版本，非與WDI調和後的跨國比較。',fontsize=10)
    save(fig,'taiwan-structure')

if __name__=='__main__':main()
