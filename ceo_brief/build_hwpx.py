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
add=clone(49,58,'#FF0000')+clone(54,59,'#0000FF')+clone(54,60,'#FF0000')+clone(31,61,'#FF0000')+clone(31,62,'#FFFFFF')+clone(31,63,'#0000FF')
hdr=hdr.replace('</hh:charProperties>',add+'</hh:charProperties>')
n=int(re.search(r'<hh:charProperties itemCnt="(\d+)"',hdr).group(1))
hdr=hdr.replace('<hh:charProperties itemCnt="%d"'%n,'<hh:charProperties itemCnt="%d"'%(n+6))
def bf(new,color):
    m=re.search(r'<hh:borderFill id="16".*?</hh:borderFill>',hdr,re.S).group(0)
    m=m.replace('id="16"','id="%d"'%new,1); return re.sub(r'faceColor="#\w+"','faceColor="%s"'%color,m,1)
nb=int(re.search(r'<hh:borderFills itemCnt="(\d+)"',hdr).group(1))
hdr=hdr.replace('</hh:borderFills>',bf(18,'#1F4E79')+bf(19,'#FFEED8')+'</hh:borderFills>')
hdr=hdr.replace('<hh:borderFills itemCnt="%d"'%nb,'<hh:borderFills itemCnt="%d"'%(nb+2))
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
def table(rows,W,style,RH=2300,HH=2300):
    tid[0]+=1; tw=sum(W)
    x='<hp:p id="0" paraPrIDRef="32" styleIDRef="18" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="34"><hp:tbl id="%d" zOrder="%d" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="%d" colCnt="%d" cellSpacing="0" borderFillIDRef="9" noAdjust="0">'%(tid[0],tid[0]%100,len(rows),len(W))
    x+='<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/><hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="0" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/><hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:inMargin left="510" right="510" top="141" bottom="141"/>'%(tw,HH+RH*(len(rows)-1))
    for i,row in enumerate(rows):
        x+='<hp:tr>'
        for j,t in enumerate(row):
            bfid,cp=style(i,j,t); h=HH if i==0 else RH
            x+='<hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="%d"><hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0"><hp:p id="0" paraPrIDRef="31" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">%s</hp:p></hp:subList><hp:cellAddr colAddr="%d" rowAddr="%d"/><hp:cellSpan colSpan="1" rowSpan="1"/><hp:cellSz width="%d" height="%d"/><hp:cellMargin left="510" right="510" top="141" bottom="141"/></hp:tc>'%(bfid,run(cp,t),j,i,W[j],h)
        x+='</hp:tr>'
    return x+'</hp:tbl><hp:t> </hp:t></hp:run></hp:p>'
def st_elect(i,j,t):
    if i==0: return 18,62
    if j==0: return 16,31
    return 15,(61 if t.startswith('민주') or t.endswith('이상') else 32)
def st_issue(i,j,t):
    if i==0: return 18,62
    if j==0: return 16,31
    if j==2: return (19,61) if t=='상' else (19,63)
    return 15,32

# ---- 본문
body=gap()
body+=head('[[r:美 중간선거]] 민주당 3관왕 확실시…대통령 거부권에 관세 철회는 난망')
body+=l1('민주당 [[b:상원 55석·하원 252석·주지사 29곳]] 장악 전망, 사실상 확정')
body+=l2('출구조사·예측시장·여론조사 종합, 상·하원 다수 확률 [[b:99% 이상]]')
body+=cap('〈美 중간선거 의석 전망〉')
body+=table([('구분','현재','예측(민주당)','예측 범위','다수 확률'),
 ('상원(100석)','공화 53 / 민주 47','민주 55석','53~56석','99% 이상'),
 ('하원(435석)','공화 219 / 민주 214','민주 252석','245~260석','99% 이상'),
 ('주지사(50명)','공화 26 / 민주 24','민주 29곳','27~30곳','약 80%')],
 [8200,11300,9200,9100,10388],st_elect,RH=1900,HH=1900)
body+=gap()
body+=l1('관세 철회는 난망, 거부권 무력화에 [[b:양원 2/3]] 필요…2년 내 변경 어려움')
body+=l2('7.24. 301조 대체로 [[b:韓 MFN 포함 12.5%]] 부과, 실효세율 2%p↑ 전망')
body+=l2('301조 판정(\'27.3.11.)·232조 추가 위험…[[b:15% 상한 유지]]가 핵심')
body+=gap()
body+=head('[[r:농업통상]]은 의회 구도와 무관, 검역·LMO·TRQ 등 비관세 압박 지속')
body+=l1('對韓 압박은 [[b:검역·LMO·TRQ·GE 표시제]] 4대 비관세 분야에 집중')
body+=l2('USTR·USDA 행정채널로 움직여 관세 협상과 별개로 요구 이어질 전망')
body+=l1('팩트시트(\'25.11) 후 [[b:11개 주 감자 허용(\'26.1)]] 등 개별 요구 지속')
body+=l2('\'26.7 밥쌀 공매 확대, 사과·배 검역 완화 등 압박 계속')
body+=gap()
body+=head('쌀·쇠고기·사과·배 등 [[r:쟁점 품목별 피해]] 미리 추정, 협상 대비 필요')
body+=cap('〈쟁점별 美 요구와 영향 강도〉')
body+=table([('쟁점','美 요구·동향','영향','국내 파급'),
 ('쌀·쇠고기','쌀 관세·TRQ, 30개월령↑ 월령 제한 제기','중~상','美산 쇠고기 수입 1위(54.6%)'),
 ('사과·배 등','U.S. Desk 통한 검역 절차 단축','상','과수농가 소득 감소 우려'),
 ('LMO 승인','팩트시트 따른 승인 효율화·적체 해소','상','안전성 심사 신뢰 확보 필요'),
 ('밥쌀·대두 TRQ','밥쌀 공매 확대, 대두 쿼터 복원 요구','중~상','쌀값 하락, 전략작물직불제 충돌'),
 ('GE(GMO) 표시','과학적 근거 부족·18개월 유예 요구','중~상','간장 \'26.12.·당류 \'27.12. 시행')],
 [7600,17400,4200,18988],st_issue,RH=2000,HH=1900)
body+=src('출처 : 미래전략연구소(2026.11.5.), USTR·USDA, KREI')
body+=l1('[[b:15% 관세상한 사수]], 쌀·30개월령↑ 쇠고기는 [[r:양보 불가선]]으로 설정')
body+=l2('검역·LMO는 과학적 절차 준수하되 [[b:처리 일정 공개]]로 \'지연\' 주장 대응')
body+=l2('밥쌀 공매는 수확기 회피, 대두 TRQ는 직불제와 충돌 없게 마련')

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
