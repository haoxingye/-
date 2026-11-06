from docx import Document
from docx.shared import Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import re

BLUE=RGBColor(0,0,0xFF); RED=RGBColor(0xFF,0,0); BLK=RGBColor(0,0,0)
H="HY견고딕"; B="KoPub돋움체 Bold"; M="KoPub돋움체 Medium"
d=Document(); s=d.sections[0]
s.page_width=Mm(210); s.page_height=Mm(297)
s.left_margin=s.right_margin=Mm(17); s.top_margin=Mm(10); s.bottom_margin=Mm(8)

def font(r,name,size,color=BLK,bold=False):
    r.font.name=name; r.font.size=Pt(size); r.font.color.rgb=color; r.font.bold=bold
    rpr=r._element.get_or_add_rPr(); rf=rpr.find(qn('w:rFonts'))
    for a in ('w:eastAsia','w:ascii','w:hAnsi'): rf.set(qn(a),name)
def para(after=0,before=0,line=1.25,align=None,indent=0,hang=0):
    p=d.add_paragraph(); f=p.paragraph_format
    f.space_after=Pt(after); f.space_before=Pt(before); f.line_spacing=line
    f.left_indent=Mm(indent); f.first_line_indent=Mm(-hang) if hang else None
    if align: p.alignment=align
    return p
def rich(p,text,name,size,hl=False):
    # [[b:..]] blue, [[r:..]] red
    for t in re.split(r'(\[\[[br]:.*?\]\])',text):
        if not t: continue
        c=BLK
        if t.startswith('[['):
            c=BLUE if t[2]=='b' else RED; t=t[4:-2]
        r=p.add_run(t); font(r,name,size,c)
        if hl: r.font.highlight_color=WD_COLOR_INDEX.YELLOW
def head(text):
    p=para(before=5,after=1,line=1.15); r=p.add_run('□ '); font(r,H,17)
    rich(p,text,H,17,hl=True)
def l1(text):
    p=para(line=1.2,indent=5.5,hang=5.5); r=p.add_run('❍ '); font(r,B,15)
    rich(p,text,B,15)
def l2(text,size=13.5):
    p=para(line=1.2,indent=9.5,hang=4); r=p.add_run('- '); font(r,M,size,RGBColor(0x40,0x40,0x40))
    rich(p,text,M,size)
def shade(cell,color):
    tcPr=cell._element.get_or_add_tcPr(); sh=OxmlElement('w:shd')
    sh.set(qn('w:val'),'clear'); sh.set(qn('w:fill'),color); tcPr.append(sh)


def table(rows,W,fs=11,redcol=None):
    t=d.add_table(rows=len(rows),cols=len(W)); t.style='Table Grid'; t.autofit=False; t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,row in enumerate(rows):
        for j,txt in enumerate(row):
            c=t.cell(i,j); c.width=Mm(W[j]); pp=c.paragraphs[0]; pp.paragraph_format.space_after=Pt(0); pp.paragraph_format.line_spacing=1.1
            pp.alignment=WD_ALIGN_PARAGRAPH.CENTER if (i==0 or j!=len(W)-1 and j!=0 or redcol is None and j>0) else WD_ALIGN_PARAGRAPH.LEFT
            col=RED if txt in('상',) or (txt.startswith('민주 ')) else BLK
            r=pp.add_run(txt); font(r,B if i==0 or j==0 or col==RED else M,fs,col)
            if i==0: shade(c,'D9D9D9')
    return t
def cap(txt,align=WD_ALIGN_PARAGRAPH.CENTER,size=12,before=2):
    p=para(line=1.0,before=before,after=1,align=align); r=p.add_run(txt); font(r,M,size)

# ---- 헤더
p=para(align=WD_ALIGN_PARAGRAPH.RIGHT,line=1.0); r=p.add_run('새로운 대한민국 농업  NH'); font(r,M,8,RGBColor(0x1E,0x6E,0xB4))
p=para(align=WD_ALIGN_PARAGRAPH.CENTER,line=1.1,after=0)
r=p.add_run('週刊 '); font(r,H,24,RGBColor(0,0x80,0)); r=p.add_run('CEO 이슈 브리프'); font(r,H,26)
p=para(line=1.1,after=2)
from docx.enum.text import WD_TAB_ALIGNMENT as TA
p.paragraph_format.tab_stops.add_tab_stop(Mm(88),TA.CENTER); p.paragraph_format.tab_stops.add_tab_stop(Mm(176),TA.RIGHT)
p.alignment=WD_ALIGN_PARAGRAPH.LEFT
r=p.add_run('\t(2026. 11. 9.)\t미래전략연구소'); font(r,M,12)

# ---- 본문
head('[[r:美 중간선거]] 민주당 3관왕 확실시…관세 철회는 난망')
l1('민주당 [[b:상원 55석·하원 252석·주지사 29곳]] 전망')
l2('다수 확률 상·하원 99%↑, 주지사 약 80%…사실상 확정')
l2('거부권 무력화에 양원 2/3 필요, [[b:2년 내 관세율 대폭 변경 어려움]]')
cap('〈美 중간선거 의석 전망〉')
table([('구분','현재','예측','민주당 다수 확률'),('상원(100석)','공화 53 / 민주 47','민주 55'+'(53~56)','99% 이상'),('하원(435석)','공화 219 / 민주 214','민주 252(245~260)','99% 이상'),('주지사(50명)','공화 26 / 민주 24','민주 29(27~30)','약 80%')],[36,48,48,44],11)
l1('7.24. 301조 대체, [[b:韓 MFN 포함 12.5%]] 부과 중')
l2('301조 판정기한 [[r:\'27.3.11.]], 232조 추가 위험…[[b:15% 상한]]이 핵심')
l2('민주당 상원 재정위원장직 확보 시 관세 철회 표결 추진 예상')
l2('골드만삭스, 美 실효관세율 약 2%p 상승 전망')

head('[[r:농업통상]]은 의회와 무관, 비관세 압박 지속')
l1('압박 중심은 [[b:검역·LMO·TRQ]] 등 비관세 분야')
l2('USTR·USDA 행정채널로 움직여 [[b:의회 구도와 관계없이 지속]] 전망')
l2('\'25.11 팩트시트(U.S. Desk) → [[b:\'26.1 11개 주 감자 허용]]')
l2('\'26.7 밥쌀 공매 확대 요구, 사과·배 검역 완화 압박')

head('[[r:쟁점 품목별 피해]] 사전 대비 필요')
rows=[('쟁점','美 요구·동향','영향','국내 파급'),
('쌀·쇠고기','관세·월령 제한 제기','중~상','美 쇠고기 수입 1위(54.6%)'),
('원예작물(사과·배·체리)','검역 절차 단축 요구','상','과수농가 소득 감소 우려'),
('LMO 승인','승인 효율화·적체 해소','상','안전성 심사 신뢰 필요'),
('밥쌀 공매·대두 TRQ','공매량·TRQ 확대','중~상','쌀값 하락, 직불제 충돌'),
('GE(GMO) 표시제','시행 18개월 유예 요구','중~상','간장 \'26.12.·당류 \'27.12. 시행')]
cap('〈쟁점별 영향 강도〉')
table(rows,[38,46,16,80],10.5)
p=para(line=1.0,before=1,after=2,align=WD_ALIGN_PARAGRAPH.RIGHT); r=p.add_run('출처 : 미래전략연구소(2026.11.5.), USTR·USDA, KREI'); font(r,M,9)
l1('[[b:15% 관세상한 사수]], 쌀·쇠고기(30개월령↑) [[r:양보 불가]]')
l2('검역·LMO는 절차 준수, [[b:처리 일정 공개]]로 \'지연\' 주장 대응')
l2('밥쌀 공매는 수확기 회피, 대두 TRQ는 직불제 연계 논리')
l1('GMO 완전표시제 [[r:\'26.12.31.]] 시행, [[b:국산·수입품 동일 적용]] 원칙 고수')
l2('소비자 정보 제공 목적 강조, 시행 일정 조정 압박에 대비')
d.save('/home/user/-/ceo_brief/CEO_이슈브리프_2026.11.9_美중간선거_농업통상.docx')
