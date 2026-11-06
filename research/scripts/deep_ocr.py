"""本機OCR保留逐頁結果與頁面影像；不把辨識文字上傳。"""
import acquire as a
import fitz,json,sys
import numpy as np
from rapidocr_onnxruntime import RapidOCR
engine=RapidOCR(intra_op_num_threads=2,inter_op_num_threads=2)
for name in sys.argv[1:]:
    out=a.PRIVATE/('deep_'+name+'_ocr_pages.json')
    if out.exists():continue
    doc=fitz.open(a.PRIVATE/('deep_'+name+'.pdf'));pages=[]
    for i,page in enumerate(doc):
        pix=page.get_pixmap(matrix=fitz.Matrix(1.7,1.7));img=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)
        result,elapsed=engine(img)
        lines=[r[1] for r in result] if result else []
        pages.append(dict(pdf_page=i+1,text='\n'.join(lines),mean_confidence=float(np.mean([r[2] for r in result])) if result else 0))
        if i in [1,3,6,10]:pix.save(a.PRIVATE/f'deep_{name}_page{i+1}.png')
        print(name,i+1,'/',len(doc),flush=True)
    out.write_text(json.dumps(pages,ensure_ascii=False),encoding='utf-8')
