# -*- coding: utf-8 -*-
"""11.16.자 v2를 바탕으로: 의석은 한 줄, V(시사점·대응) 삭제, III(미국 관세·농업통상 전망)·IV(한국 농업 영향) 강화"""
import zipfile,re
from xml.sax.saxutils import escape
SRC='/root/.claude/uploads/11c21ea4-a26c-5e0c-8cef-cea08fc46b14/e9ad0847-CEO______2026.11.16.__________________v2.hwpx'
OUT='/home/user/-/ceo_brief/CEO_이슈브리프_2026.11.16_美중간선거_농업통상_v11.hwpx'
z=zipfile.ZipFile(SRC); order=z.namelist(); f={n:z.read(n) for n in order}
s=f['Contents/section0.xml'].decode('utf8'); h=f['Contents/header.xml'].decode('utf8')

# 글자모양 추가: 세부(14pt) 파랑 63, 빨강 64
def clone(src,new,color):
    m=re.search(r'<hh:charPr id="%d" .*?</hh:charPr>'%src,h,re.S).group(0)
    m=re.sub(r'id="\d+"','id="%d"'%new,m,count=1); return re.sub(r'textColor="#\w+"','textColor="%s"'%color,m,count=1)
h=h.replace('</hh:charProperties>',clone(46,63,'#0000FF')+clone(46,64,'#FF0000')+'</hh:charProperties>')
n=int(re.search(r'<hh:charProperties itemCnt="(\d+)"',h).group(1))
h=h.replace('<hh:charProperties itemCnt="%d"'%n,'<hh:charProperties itemCnt="%d"'%(n+2))
f['Contents/header.xml']=h.encode('utf8')

# 기존 조각 재사용: 머리(제목 영역)/빈줄/표 블록/출처
first=s.index('□ '); first=s.rfind('<hp:p ',0,first)
pre=s[:first]
spacer=re.search(r'<hp:p [^>]*paraPrIDRef="34"[^>]*>.*?</hp:p>',s,re.S).group(0)
cap_i=s.index('주요 쟁점별'); cap_start=s.rfind('<hp:p ',0,cap_i)
t1=s.index('<hp:tbl ',s.index('<hp:tbl ')+1); t_start=s.rfind('<hp:p ',0,t1)
t_end=s.index('</hp:p>',s.index('</hp:tbl>',t1))+7
caption=s[cap_start:t_start]; table=s[t_start:t_end]
src_i=s.index('출처 :'); src_start=s.rfind('<hp:p ',0,src_i); src_end=s.index('</hp:p>',src_i)+7
source=s[src_start:src_end]
source=re.sub(r'출처 :[^<]*','출처 : 미래전략연구소(2026.11.5.), Reuters, White House·KREI, 美 NTE(2026)',source)
source=re.sub(r'<hp:linesegarray>.*?</hp:linesegarray>','',source,flags=re.S)
caption=re.sub(r'<hp:linesegarray>.*?</hp:linesegarray>','',caption,flags=re.S)
spacer=re.sub(r'<hp:linesegarray>.*?</hp:linesegarray>','',spacer,flags=re.S)

def run(c,t): return '<hp:run charPrIDRef="%d"><hp:t>%s</hp:t></hp:run>'%(c,escape(t))
def P(pr,runs): return '<hp:p id="0" paraPrIDRef="%d" styleIDRef="18" pageBreak="0" columnBreak="0" merged="0">%s</hp:p>'%(pr,runs)
HD={'k':38,'r':39}; L1={'k':48,'b':49,'r':53}; L2={'k':46,'b':63,'r':64,'u':47}
def segs(t,m):
    o=''
    for x in re.split(r'(\[\[[brku]:.*?\]\])',t):
        if not x: continue
        k='k'
        if x.startswith('[['): k=x[2]; x=x[4:-2]
        o+=run(m[k],x)
    return o
head=lambda t:P(31,run(28,'□ ')+segs(t,HD))
l1=lambda t:P(32,run(21,' ❍ ')+segs(t,L1))
l2=lambda t:P(33,run(35,'   - ')+segs(t,L2))

B=''
B+=head('[[k:美 중간선거, ]][[r:민주당 3관왕 확실시]][[k:…트럼프 통상정책 견제 본격화]]')
B+=l1('민주당, [[b:상원 55석(총 100석)·하원 252석(총 435석)]]·주지사 29곳 내외 예측')
B+=l2('[[u:과반(상원 51·하원 218)]] 넘을 확률 99% 이상, 주지사는 약 80%')
B+=spacer
B+=head('[[k:민주당 견제에도 ]][[r:관세 철회는 어렵고]][[k:, 對韓 농업 시장접근 요구는 지속]]')
B+=l1('민주당, 상임위원장직 맡아 [[b:관세 면제·한일 대미 투자금 집행]] 조사 예상')
B+=l2('철회 표결 추진 예상이나 [[u:거부권 무력화에 양원 2/3 필요]], 2년 내 변경 어려움')
B+=l1('7.24. 강제노동 301조 관세로 대체, 韓 [[b:12.5% 관세]] 부과(최혜국세율 포함)')
B+=l2('301조 판정(’27.3.11.)·232조(품목관세) 추가 위험…[[u:15% 상한]]이 핵심')
B+=l1('농업통상은 무역대표부·농무부 행정 채널로 움직여 [[b:의회 구도와 무관]]')
B+=l2('’25.11. 팩트시트 후 감자 11개 주 허용(’26.1.) 등 개별 요구 이어짐')
B+=spacer
B+=head('[[k:관세보다 시장접근 요구 확대…]][[r:쌀·쇠고기·검역·LMO·GE 표시제]][[k: 부상]]')
B+=l1('美, 쌀 관세·TRQ(저율관세할당)·[[b:30개월령 이상 쇠고기 제한]] 문제 삼아 압박')
B+=l2('美산 쇠고기 수입 1위(54.6%)…월령 제한 풀리면 한우 가격 부담')
B+=l1('사과·배·체리 검역 적체 이유로 [[b:U.S. Desk(전담창구)]] 통해 단축 요구 예상')
B+=l1('밥쌀 공매량 확대(’26.7.)·[[b:대두 TRQ]] 운영 투명성 요구…쌀값 하락 압력')
B+=l2('대두 추가 쿼터(약 4만 톤) 종료로 美 수출 [[b:약 3만 톤 감소]] 지적')
B+=l1('LMO(유전자변형) 승인 점검, [[b:GE(GMO) 표시제]] 18개월 유예 요구')
B+=l2('韓 [[u:간장 ’26.12.31., 당류·식용유지 ’27.12.31.]] 시행…조정 압력')
B+=caption+table+source

s2=pre+B+'</hs:sec>'
f['Contents/section0.xml']=s2.encode('utf8')
txt=re.sub(r'<[^>]+>','\n',s2); f['Preview/PrvText.txt']='\n'.join(l.strip() for l in txt.split('\n') if l.strip()).encode('utf8')
with zipfile.ZipFile(OUT,'w') as o:
    for nme in order: o.writestr(nme,f[nme],zipfile.ZIP_STORED if nme=='mimetype' else zipfile.ZIP_DEFLATED)
# 검증
import xml.dom.minidom as md
md.parseString(s2); md.parseString(h)
print('ok; missing char:',set(re.findall(r'charPrIDRef="(\d+)"',s2))-set(re.findall(r'<hh:charPr id="(\d+)"',h)))
for p in re.findall(r'paraPrIDRef="(3[123])"[^>]*>(.*?)</hp:p>',s2):
    t=''.join(re.findall(r'<hp:t>([^<]*)</hp:t>',p[1]))
    if t.strip(): print(p[0],len(t),t)
