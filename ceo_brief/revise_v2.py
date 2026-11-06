# 사용자 11.16.자 v2 hwpx를 바탕으로: PIIE 줄 삭제, 강조 정리, ☞ 결론 줄 추가
import zipfile,re
SRC='/root/.claude/uploads/11c21ea4-a26c-5e0c-8cef-cea08fc46b14/e9ad0847-CEO______2026.11.16.__________________v2.hwpx'
OUT='/home/user/-/ceo_brief/CEO_이슈브리프_2026.11.16_美중간선거_농업통상_v3.hwpx'
z=zipfile.ZipFile(SRC); order=z.namelist(); f={n:z.read(n) for n in order}
s=f['Contents/section0.xml'].decode('utf8')
# 1) PIIE 줄 삭제
a=s.index('의회 견제로 다른 정책이 막히면 '); a=s.rfind('<hp:p ',0,a); b=s.index('</hp:p>',a)+7
s=s[:a]+s[b:]
# 2) 301조 줄: 빨강 날짜를 일반 글자로(파랑 한 곳만 강조)
old='<hp:run charPrIDRef="60"><hp:t>’27.3.11.</hp:t></hp:run>'
assert old in s; s=s.replace(old,'<hp:run charPrIDRef="48"><hp:t>’27.3.11.</hp:t></hp:run>')
# 3) ☞ 결론 줄 추가(마지막 문단 뒤)
new=('<hp:p id="0" paraPrIDRef="32" styleIDRef="18" pageBreak="0" columnBreak="0" merged="0">'
 '<hp:run charPrIDRef="21"><hp:t> ☞ </hp:t></hp:run>'
 '<hp:run charPrIDRef="52"><hp:t>관세 협상과 별개로 </hp:t></hp:run>'
 '<hp:run charPrIDRef="49"><hp:t>쌀·쇠고기·사과·배 비관세 요구 지속</hp:t></hp:run>'
 '<hp:run charPrIDRef="52"><hp:t>, 품목별 대응 필요</hp:t></hp:run></hp:p>')
s=s.replace('</hs:sec>',new+'</hs:sec>'); assert new in s
f['Contents/section0.xml']=s.encode('utf8')
t=f['Preview/PrvText.txt'].decode('utf8')
t=re.sub(r'\n   - 의회 견제로[^\n]*','',t); f['Preview/PrvText.txt']=t.encode('utf8')
with zipfile.ZipFile(OUT,'w') as o:
    for n in order: o.writestr(n,f[n],zipfile.ZIP_STORED if n=='mimetype' else zipfile.ZIP_DEFLATED)
print('ok')
