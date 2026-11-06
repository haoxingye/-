# -*- coding: utf-8 -*-
"""11.2.자 CEO 이슈브리프 hwpx를 템플릿으로 본문·표만 교체해 새 hwpx 생성"""
import re, zipfile, sys
from xml.sax.saxutils import escape
TPL='/root/.claude/uploads/11c21ea4-a26c-5e0c-8cef-cea08fc46b14/0377e8e0-__CEO_____2026.11.2.__________.hwpx'
OUT='/home/user/-/ceo_brief/CEO_이슈브리프_2026.11.9_美중간선거_농업통상.hwpx'
z=zipfile.ZipFile(TPL); files={n:z.read(n) for n in z.namelist()}; order=z.namelist()
hdr=files['Contents/header.xml'].decode('utf8'); sec=files['Contents/section0.xml'].decode('utf8')

# ---- 글자모양 추가(빨강 15pt, 파랑/빨강 14pt, 빨강 표 12pt)
def clone(src,new,color):
    m=re.search(r'<hh:charPr id="%d" .*?</hh:charPr>'%src,hdr,re.S).group(0)
    m=re.sub(r'id="\d+"','id="%d"'%new,m,1); return re.sub(r'textColor="#\w+"','textColor="%s"'%color,m,1)
add=clone(49,58,'#FF0000')+clone(54,59,'#0000FF')+clone(54,60,'#FF0000')+clone(31,61,'#FF0000')
hdr=hdr.replace('</hh:charProperties>',add+'</hh:charProperties>')
n=int(re.search(r'<hh:charProperties itemCnt="(\d+)"',hdr).group(1))
hdr=hdr.replace('<hh:charProperties itemCnt="%d"'%n,'<hh:charProperties itemCnt="%d"'%(n+4))
files['Contents/header.xml']=hdr.encode('utf8')

# ---- 헬퍼
def run(c,t): return '<hp:run charPrIDRef="%d"><hp:t>%s</hp:t></hp:run>'%(c,escape(t))
def P(pr,runs): return '<hp:p id="0" paraPrIDRef="%d" styleIDRef="18" pageBreak="0" columnBreak="0" merged="0">%s</hp:p>'%(pr,runs)
# 글자 ID: 본문 □ (노랑 형광: 검정39/빨강40), ❍ (검정46/파랑49/빨강58), - (검정54/파랑59/빨강60)
HL={'k':39,'r':40}; L1={'k':46,'b':49,'r':58}; L2={'k':54,'b':59,'r':60}
def segs(text,m):
    out=''
    for t in re.split(r'(\[\[[br]:.*?\]\])',text):
        if not t: continue
        k='k'
        if t.startswith('[['): k=t[2]; t=t[4:-2]
        out+=run(m[k],t)
    return out
def head(t): return P(33,run(28,'□ ')+segs(t,HL))
def l1(t): return P(34,run(21,' ❍ ')+segs(t,L1))
def l2(t): return P(35,run(45,'   - ')+segs(t,L2))
def gap(): return P(35,'<hp:run charPrIDRef="55"/>')
def cap(t): return P(31,run(34,t))
def src(t): return P(32,run(32,t))
tid=[1231558400]
def table(rows,W,redfn):
    tid[0]+=1; H=2048; B=1800; tw=sum(W)
    x='<hp:p id="0" paraPrIDRef="32" styleIDRef="18" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="34"><hp:tbl id="%d" zOrder="%d" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="%d" colCnt="%d" cellSpacing="0" borderFillIDRef="9" noAdjust="0">'%(tid[0],tid[0]%100,len(rows),len(W))
    x+='<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/><hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="0" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/><hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:inMargin left="510" right="510" top="141" bottom="141"/>'%(tw,H+B*(len(rows)-1))
    for i,row in enumerate(rows):
        x+='<hp:tr>'
        for j,t in enumerate(row):
            if i==0: bf,pp,cp=16,29,31
            else: bf,pp,cp=15,31,(61 if redfn(j,t) else 32)
            h=H if i==0 else B
            x+='<hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="%d"><hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0"><hp:p id="0" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">%s</hp:p></hp:subList><hp:cellAddr colAddr="%d" rowAddr="%d"/><hp:cellSpan colSpan="1" rowSpan="1"/><hp:cellSz width="%d" height="%d"/><hp:cellMargin left="510" right="510" top="141" bottom="141"/></hp:tc>'%(bf,pp,run(cp,t),j,i,W[j],h)
        x+='</hp:tr>'
    return x+'</hp:tbl><hp:t> </hp:t></hp:run></hp:p>'

# ---- 본문
body=gap()
body+=head('[[r:美 중간선거]] 민주당 3관왕 확실시…관세 철회는 난망')
body+=l1('민주당 [[b:상원 55석·하원 252석·주지사 29곳]] 전망')
body+=l2('다수 확률 상·하원 99%↑, 주지사 약 80%…사실상 확정')
body+=l2('거부권 무력화에 양원 2/3 필요, [[b:2년 내 관세율 대폭 변경 어려움]]')
body+=cap('〈美 중간선거 의석 전망〉')
body+=table([('구분','현재','예측(범위)','민주당 다수 확률'),
 ('상원(100석)','공화 53 / 민주 47','민주 55(53~56)','99% 이상'),
 ('하원(435석)','공화 219 / 민주 214','민주 252(245~260)','99% 이상'),
 ('주지사(50명)','공화 26 / 민주 24','민주 29(27~30)','약 80%')],
 [9000,13000,13000,13188],lambda j,t:t.startswith('민주 '))
body+=l1('7.24. 301조 대체, [[b:韓 MFN 포함 12.5%]] 부과 중')
body+=l2('301조 판정기한 [[r:\'27.3.11.]], 232조 추가 위험…[[b:15% 상한]]이 핵심')
body+=l2('민주당 상원 재정위원장직 확보 시 관세 철회 표결 추진 예상')
body+=l2('골드만삭스, 美 실효관세율 약 2%p 상승 전망')
body+=gap()
body+=head('[[r:농업통상]]은 의회와 무관, 비관세 압박 지속')
body+=l1('압박 중심은 [[b:검역·LMO·TRQ]] 등 비관세 분야')
body+=l2('USTR·USDA 행정채널로 움직여 [[b:의회 구도와 관계없이 지속]] 전망')
body+=l2('\'25.11 팩트시트(U.S. Desk) → [[b:\'26.1 11개 주 감자 허용]]')
body+=l2('\'26.7 밥쌀 공매 확대 요구, 사과·배 검역 완화 압박')
body+=gap()
body+=head('[[r:쟁점 품목별 피해]] 사전 대비 필요')
body+=cap('〈쟁점별 영향 강도〉')
body+=table([('쟁점','美 요구·동향','영향','국내 파급'),
 ('쌀·쇠고기','관세·월령 제한 제기','중~상','美 쇠고기 수입 1위(54.6%)'),
 ('원예작물(사과·배·체리)','검역 절차 단축 요구','상','과수농가 소득 감소 우려'),
 ('LMO 승인','승인 효율화·적체 해소','상','안전성 심사 신뢰 필요'),
 ('밥쌀 공매·대두 TRQ','공매량·TRQ 확대','중~상','쌀값 하락, 직불제 충돌'),
 ('GE(GMO) 표시제','시행 18개월 유예 요구','중~상','간장 \'26.12.·당류 \'27.12. 시행')],
 [9500,12500,4400,21788],lambda j,t:t=='상')
body+=src('출처 : 미래전략연구소(2026.11.5.), USTR·USDA, KREI')
body+=l1('[[b:15% 관세상한 사수]], 쌀·쇠고기(30개월령↑) [[r:양보 불가]]')
body+=l2('검역·LMO는 절차 준수, [[b:처리 일정 공개]]로 \'지연\' 주장 대응')
body+=l2('밥쌀 공매는 수확기 회피, 대두 TRQ는 직불제 연계 논리')
body+=l1('GMO 완전표시제 [[r:\'26.12.31.]] 시행, [[b:국산·수입품 동일 적용]] 원칙 고수')
body+=l2('소비자 정보 제공 목적 강조, 시행 일정 조정 압박에 대비')

i=sec.index('<hp:p id="2147483648" paraPrIDRef="28"')
sec=sec[:i]+body+'</hs:sec>'
sec=sec.replace('(2026. 11. 2.)','(2026. 11. 9.)')
files['Contents/section0.xml']=sec.encode('utf8')
txt=re.sub(r'<[^>]+>','\n',sec); 
files['Preview/PrvText.txt']='\n'.join(l.strip() for l in txt.split('\n') if l.strip()).encode('utf8')
with zipfile.ZipFile(OUT,'w') as o:
    for nme in order:
        o.writestr(zipfile.ZipInfo(nme) if False else nme, files[nme], zipfile.ZIP_STORED if nme=='mimetype' else zipfile.ZIP_DEFLATED)
print('ok',OUT)
