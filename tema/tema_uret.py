#!/usr/bin/env python3
"""Mısır sahnesini şablon alıp başka kültür temaları üretir.
Kullanım: python3 tema/tema_uret.py [asya mezopotamya amerika antarktika]"""
import sys, json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = open(f'{R}/icerik/misir-iki-kare-farki/sahne.html', encoding='utf-8').read()
POST = json.load(open(f'{R}/icerik/misir-iki-kare-farki/post.json', encoding='utf-8'))

T = {}
T['asya'] = dict(slug='asya-iki-kare-farki', slugtr='Asya',
 bg=['#2a0a12', '#7a1426', '#d9531e', '#f6b26b'], pagebg='#2a0a12',
 sun='<circle cx=540 cy=1560 r=250 fill="#e8362f" opacity="0.9"/>',
 pat='<path d="M0,48 Q12,24 24,48 Q36,24 48,48" fill=none stroke="#f4c95d" stroke-width=5/><path d="M0,34 Q12,10 24,34 Q36,10 48,34" fill=none stroke="#fff4e0" stroke-width=3 opacity=.8/>',
 col=dict(SAND='#f4c95d', AEG='#2f9e8f', TERRA='#e63946', NEUT='#fbeed3', MARB='#fff4e0', GOLD='#f4c95d'), dark='#2a0a12', cta='#fff4e0',
 header='ANTİK ASYA GEOMETRİSİ', sub='DOĞUNUN KADİM ÖLÇÜSÜ', tsub='Şekilden okunan matematik',
 sub0="Eski Asya’da şekil, formülden önce gelirdi", line1="Eski Asya'da şekil, formülden önce gelirdi!",
 icon="el('circle',{r:26,fill:'none',stroke:GOLD,'stroke-width':5},eye);el('circle',{r:9,fill:'#e63946'},eye);for(let i=0;i<8;i++){const a=i*Math.PI/4;el('line',{x1:Math.cos(a)*34,y1:Math.sin(a)*34,x2:Math.cos(a)*48,y2:Math.sin(a)*48,stroke:GOLD,'stroke-width':5,'stroke-linecap':'round'},eye)}",
 decor='''
const stars=document.getElementById('stars');
for(let i=0;i<40;i++){const x=(i*389)%1040+20,y=(i*241)%1300+260;el('ellipse',{cx:x,cy:y,rx:7,ry:4,fill:'#ffc6d0',opacity:.22+(i%4)*.1,transform:`rotate(${(i*37)%90} ${x} ${y})`},stars)}
const pyr=document.getElementById('pyr');
[[170,1740,560,330,'#5a1426'],[900,1740,520,280,'#5a1426'],[540,1740,640,200,'#7a1a30']].forEach(([cx,by,w,h,c])=>{el('polygon',{points:`${cx-w/2},${by} ${cx-w*.08},${by-h} ${cx+w*.08},${by-h} ${cx+w/2},${by}`,fill:c},pyr)});
function pagoda(x,by,sc,c){let y=by,w=150*sc;for(let i=0;i<4;i++){const h=62*sc,ww=w*(1-i*.17);el('rect',{x:x-ww*.34,y:y-h,width:ww*.68,height:h,fill:c},pyr);el('polygon',{points:`${x-ww/2-18*sc},${y-h} ${x+ww/2+18*sc},${y-h} ${x+ww*.3},${y-h-26*sc} ${x-ww*.3},${y-h-26*sc}`,fill:c},pyr);y-=h+20*sc}
 el('rect',{x:x-3*sc,y:y-70*sc,width:6*sc,height:70*sc,fill:c},pyr)}
pagoda(120,1740,1.15,'#2a0a12');pagoda(960,1740,1.0,'#2a0a12');
const cols=document.getElementById('cols');
[[75],[1005]].forEach(([x])=>{el('line',{x1:x,y1:190,x2:x,y2:300,stroke:'#f4c95d','stroke-width':3,opacity:.9},cols);el('ellipse',{cx:x,cy:350,rx:42,ry:58,fill:'#e63946',opacity:.95},cols);el('rect',{x:x-26,y:296,width:52,height:12,fill:'#f4c95d'},cols);el('rect',{x:x-26,y:394,width:52,height:12,fill:'#f4c95d'},cols);el('line',{x1:x,y1:406,x2:x,y2:460,stroke:'#f4c95d','stroke-width':4},cols)});
cols.setAttribute('opacity',.95);
const dn=document.getElementById('dunes');
el('path',{d:'M0,1790 Q270,1740 540,1790 T1080,1775 L1080,1920 L0,1920 Z',fill:'#3d0d1b'},dn);
el('path',{d:'M0,1850 Q300,1805 620,1850 T1080,1842 L1080,1920 L0,1920 Z',fill:'#220610'},dn);
''', caption="a² − b² neden (a + b)(a − b)? 🏮\nEski Asya'da şekil, formülden önce gelirdi!\nKareden küçük kareyi çıkar, kalanı köşegenden böl, parçaları yeniden diz: dikdörtgen!\n\nKaydet, sınavdan önce tekrar bak 📌", tag='antikasya')

T['mezopotamya'] = dict(slug='mezopotamya-iki-kare-farki', slugtr='Mezopotamya',
 bg=['#0f1f3d', '#3b4a6b', '#b5763a', '#e2b26a'], pagebg='#0f1f3d',
 sun='<circle cx=540 cy=1640 r=330 fill="url(#sun)"/>',
 pat='<path d="M0,0 L24,40 L48,0 Z" fill="#f0c15a"/><path d="M0,48 L24,12 L48,48 Z" fill="#2a5db0"/>',
 col=dict(SAND='#d9a441', AEG='#2a5db0', TERRA='#b5452a', NEUT='#efd9a7', MARB='#fff0d0', GOLD='#f0c15a'), dark='#0f1f3d', cta='#fff0d0',
 header='MEZOPOTAMYA GEOMETRİSİ', sub='KİL TABLETLERİN ÇAĞI', tsub='Kil tabletlerde şekille düşünürlerdi',
 sub0='Kil tabletler çağında formül yoktu, şekil vardı', line1='Kil tabletler çağında formül yoktu... şekil vardı!',
 icon="for(let i=0;i<3;i++){const x=(i-1)*34;el('polygon',{points:`${x-14},-22 ${x+14},-22 ${x},4`,fill:GOLD},eye);el('line',{x1:x,y1:4,x2:x,y2:34,stroke:GOLD,'stroke-width':6,'stroke-linecap':'round'},eye)}",
 decor='''
const stars=document.getElementById('stars');
for(let i=0;i<34;i++){const x=(i*397)%1040+20,y=(i*211)%560+210;el('circle',{cx:x,cy:y,r:(i%3)+1.2,opacity:.2+(i%4)*.15},stars)}
const pyr=document.getElementById('pyr');
function zig(cx,by,w,tiers,c){let y=by;for(let i=0;i<tiers;i++){const ww=w*(1-i*.2),h=70;el('rect',{x:cx-ww/2,y:y-h,width:ww,height:h,fill:c},pyr);el('rect',{x:cx-ww/2,y:y-h,width:ww,height:10,fill:'#000',opacity:.18},pyr);y-=h}
 el('polygon',{points:`${cx-28},${by-70*tiers-10} ${cx+28},${by-70*tiers-10} ${cx},${by-70*tiers-48}`,fill:c},pyr);
 el('polygon',{points:`${cx-w*.09},${by} ${cx+w*.09},${by} ${cx+w*.05},${by-70} ${cx-w*.05},${by-70}`,fill:'#000',opacity:.2},pyr)}
zig(380,1740,560,4,'#6b3a22');
function palm(x,by,h){el('path',{d:`M${x},${by} Q${x+14},${by-h/2} ${x+6},${by-h}`,stroke:'#2d1a10','stroke-width':14,fill:'none'},pyr);
 for(let i=0;i<7;i++){const a=-Math.PI/2+(i-3)*.5;el('path',{d:`M${x+6},${by-h} q${Math.cos(a)*70},${Math.sin(a)*40-10} ${Math.cos(a)*120},${Math.sin(a)*70+40}`,stroke:'#2d1a10','stroke-width':8,fill:'none','stroke-linecap':'round'},pyr)}}
palm(850,1740,300);palm(960,1740,240);
const cols=document.getElementById('cols');
[[75],[1005]].forEach(([x])=>{for(let r=0;r<9;r++)for(let k=0;k<2;k++){const y=300+r*150;el('polygon',{points:`${x-16+k*34-14},${y} ${x-16+k*34+14},${y} ${x-16+k*34},${y+26}`},cols);el('line',{x1:x-16+k*34,y1:y+26,x2:x-16+k*34,y2:y+80,stroke:'#fff0d0','stroke-width':5},cols)}});
cols.setAttribute('opacity',.2);
const dn=document.getElementById('dunes');
el('path',{d:'M0,1790 Q270,1760 540,1790 T1080,1785 L1080,1920 L0,1920 Z',fill:'#1d4f8c'},dn);
for(let i=0;i<6;i++)el('path',{d:`M${i*190-40},${1830+i%2*30} q40,-18 80,0 t80,0`,stroke:'#8fc0f0','stroke-width':5,fill:'none',opacity:.7},dn);
''', caption="a² − b² neden (a + b)(a − b)? 🏺\nKil tabletler çağında formül yoktu, şekil vardı!\nKareden küçük kareyi çıkar, kalanı köşegenden böl, parçaları yeniden diz: dikdörtgen!\n\nKaydet, sınavdan önce tekrar bak 📌", tag='mezopotamya')

T['amerika'] = dict(slug='amerika-iki-kare-farki', slugtr='Amerika (Maya)',
 bg=['#06201f', '#0d4d45', '#1d7a4a', '#f2a33a'], pagebg='#06201f',
 sun='<circle cx=540 cy=1600 r=330 fill="url(#sun)"/>',
 pat='<path d="M0,48 V24 H12 V36 H24 V12 H36 V24 H48" fill=none stroke="#f6c24b" stroke-width=6 /><path d="M0,48 H48" stroke="#2bb3a3" stroke-width=6 />',
 col=dict(SAND='#f2a33a', AEG='#2bb3a3', TERRA='#d9473b', NEUT='#f1e4c3', MARB='#fff3d6', GOLD='#f6c24b'), dark='#06201f', cta='#fff3d6',
 header='KADİM AMERİKA GEOMETRİSİ', sub='MAYA VE İNKA DİYARI', tsub='Taş piramitlerin geometrisi',
 sub0='Maya çağında formül yoktu, şekil vardı', line1='Maya çağında formül yoktu... şekil vardı!',
 icon="el('circle',{r:22,fill:GOLD},eye);el('circle',{r:9,fill:'#06201f'},eye);for(let i=0;i<12;i++){const a=i*Math.PI/6;el('polygon',{points:`${Math.cos(a-.14)*30},${Math.sin(a-.14)*30} ${Math.cos(a+.14)*30},${Math.sin(a+.14)*30} ${Math.cos(a)*50},${Math.sin(a)*50}`,fill:GOLD},eye)}",
 decor='''
const stars=document.getElementById('stars');
for(let i=0;i<36;i++){const x=(i*389)%1040+20,y=(i*233)%640+210;el('circle',{cx:x,cy:y,r:(i%3)+1.2,opacity:.25+(i%4)*.15},stars)}
const pyr=document.getElementById('pyr');
function step(cx,by,w,tiers,c){let y=by;const th=56;for(let i=0;i<tiers;i++){const ww=w*(1-i/(tiers+.6));el('rect',{x:cx-ww/2,y:y-th,width:ww,height:th,fill:c},pyr);el('rect',{x:cx-ww/2,y:y-th,width:ww,height:8,fill:'#000',opacity:.2},pyr);y-=th}
 el('rect',{x:cx-34,y:y-46,width:68,height:46,fill:c},pyr);el('rect',{x:cx-12,y:y-34,width:24,height:34,fill:'#06201f'},pyr);
 el('polygon',{points:`${cx-22},${by} ${cx+22},${by} ${cx+10},${by-th*tiers} ${cx-10},${by-th*tiers}`,fill:'#000',opacity:.25},pyr)}
step(540,1740,700,6,'#2a3b2e');
function leaf(x,by,s,fl){for(let i=0;i<6;i++){const a=-Math.PI/2+(i-2.5)*.42*fl;el('ellipse',{cx:x+Math.cos(a)*90*s,cy:by+Math.sin(a)*110*s,rx:26*s,ry:78*s,fill:'#052a1c',transform:`rotate(${a*180/Math.PI+90} ${x+Math.cos(a)*90*s} ${by+Math.sin(a)*110*s})`},pyr)}}
leaf(80,1730,1.5,1);leaf(1010,1730,1.5,1);leaf(240,1760,1,1);leaf(860,1760,1,1);
const cols=document.getElementById('cols');
[[30],[960]].forEach(([x])=>{el('rect',{x:x+10,y:260,width:70,height:1440,rx:6},cols);for(let r=0;r<10;r++){el('rect',{x:x+22,y:300+r*140,width:46,height:46,fill:'#06201f'},cols);el('circle',{cx:x+45,cy:323+r*140,r:10,fill:'#fff3d6'},cols)}});
cols.setAttribute('opacity',.16);
const dn=document.getElementById('dunes');
el('path',{d:'M0,1790 Q270,1740 540,1790 T1080,1775 L1080,1920 L0,1920 Z',fill:'#0b2e1b'},dn);
el('path',{d:'M0,1850 Q300,1805 620,1850 T1080,1842 L1080,1920 L0,1920 Z',fill:'#04170e'},dn);
''', caption="a² − b² neden (a + b)(a − b)? 🌴\nMaya çağında formül yoktu, şekil vardı!\nKareden küçük kareyi çıkar, kalanı köşegenden böl, parçaları yeniden diz: dikdörtgen!\n\nKaydet, sınavdan önce tekrar bak 📌", tag='maya')

T['antarktika'] = dict(slug='antarktika-iki-kare-farki', slugtr='Antarktika',
 bg=['#04122e', '#0a3a5e', '#1d7d9a', '#bfeaf5'], pagebg='#04122e',
 sun='<circle cx=540 cy=1660 r=300 fill="#bfeaf5" opacity="0.22"/>',
 pat='<path d="M0,48 L24,6 L48,48 Z" fill="#e9f8ff"/><path d="M12,48 L24,26 L36,48 Z" fill="#7fdcf0"/>',
 col=dict(SAND='#7fdcf0', AEG='#7aa7ff', TERRA='#ff7a6b', NEUT='#e9f8ff', MARB='#ffffff', GOLD='#8be9ff'), dark='#04122e', cta='#e9f8ff',
 header='ANTARKTİKA GEOMETRİSİ', sub='KUTUP GECESİNİN IŞIĞI', tsub='Buzun üstünde şekille düşün',
 sub0='Buzullar diyarında formül yoktu, şekil vardı', line1='Buzullar diyarında formül yoktu... şekil vardı!',
 icon="for(let i=0;i<6;i++){const a=i*Math.PI/3;el('line',{x1:0,y1:0,x2:Math.cos(a)*44,y2:Math.sin(a)*44,stroke:GOLD,'stroke-width':5,'stroke-linecap':'round'},eye);el('line',{x1:Math.cos(a)*26-Math.sin(a)*12,y1:Math.sin(a)*26+Math.cos(a)*12,x2:Math.cos(a)*34,y2:Math.sin(a)*34,stroke:GOLD,'stroke-width':4},eye);el('line',{x1:Math.cos(a)*26+Math.sin(a)*12,y1:Math.sin(a)*26-Math.cos(a)*12,x2:Math.cos(a)*34,y2:Math.sin(a)*34,stroke:GOLD,'stroke-width':4},eye)}",
 decor='''
const stars=document.getElementById('stars');
for(let i=0;i<50;i++){const x=(i*397)%1040+20,y=(i*211)%760+200;el('circle',{cx:x,cy:y,r:(i%3)+1.2,opacity:.3+(i%4)*.15},stars)}
[['#3df5a5',.34,0],['#7a6cff',.26,90],['#3df5a5',.22,200]].forEach(([c,o,dy])=>{el('path',{d:`M-20,${420+dy} C200,${300+dy} 360,${560+dy} 560,${400+dy} S900,${300+dy} 1100,${470+dy} L1100,${560+dy} C900,${420+dy} 760,${660+dy} 560,${520+dy} S200,${420+dy} -20,${540+dy} Z`,fill:c,opacity:o},stars)});
const pyr=document.getElementById('pyr');
[[170,1740,520,320,'#cfeefa'],[900,1740,460,260,'#bfe6f5'],[540,1740,420,170,'#e9f8ff']].forEach(([cx,by,w,h,c])=>{el('polygon',{points:`${cx-w/2},${by} ${cx-w*.18},${by-h*.8} ${cx-w*.05},${by-h*.62} ${cx+w*.06},${by-h} ${cx+w*.22},${by-h*.5} ${cx+w/2},${by}`,fill:c},pyr);el('polygon',{points:`${cx+w*.06},${by-h} ${cx+w*.22},${by-h*.5} ${cx+w/2},${by} ${cx+w*.1},${by}`,fill:'#6aa8c8',opacity:.45},pyr)});
const cols=document.getElementById('cols');
[[75],[1005]].forEach(([x])=>{el('polygon',{points:`${x-30},1700 ${x+30},1700 ${x+14},330 ${x},250 ${x-14},330`},cols)});
cols.setAttribute('opacity',.14);
const dn=document.getElementById('dunes');
el('path',{d:'M0,1790 Q270,1750 540,1790 T1080,1778 L1080,1920 L0,1920 Z',fill:'#e9f8ff'},dn);
el('path',{d:'M0,1850 Q300,1815 620,1850 T1080,1845 L1080,1920 L0,1920 Z',fill:'#bfe6f5'},dn);
function peng(x,y,s){el('ellipse',{cx:x,cy:y,rx:30*s,ry:48*s,fill:'#0b1b2e'},dn);el('ellipse',{cx:x+3*s,cy:y+8*s,rx:19*s,ry:34*s,fill:'#ffffff'},dn);el('circle',{cx:x,cy:y-40*s,r:19*s,fill:'#0b1b2e'},dn);el('polygon',{points:`${x+12*s},${y-40*s} ${x+30*s},${y-34*s} ${x+12*s},${y-30*s}`,fill:'#ff9a3d'},dn);el('circle',{cx:x+5*s,cy:y-44*s,r:3*s,fill:'#fff'},dn)}
peng(250,1830,1.1);peng(330,1850,.85);peng(820,1835,1.05);
''', caption="a² − b² neden (a + b)(a − b)? 🐧\nBuzullar diyarında formül yoktu, şekil vardı!\nKareden küçük kareyi çıkar, kalanı köşegenden böl, parçaları yeniden diz: dikdörtgen!\n\nKaydet, sınavdan önce tekrar bak 📌", tag='antarktika')

def build(k):
    t = T[k]; s = BASE
    # arka plan degradesi + desen
    s = re.sub(r'<linearGradient id=bg.*?</linearGradient>',
        '<linearGradient id=bg x1=0 y1=0 x2=0 y2=1>'+''.join(f'<stop offset={o} stop-color="{c}"/>' for o,c in zip(['0','.42','.8','1'],t['bg']))+'</linearGradient>', s, flags=re.S)
    s = re.sub(r'<pattern id=mea.*?</pattern>', '<pattern id=mea width=48 height=48 patternUnits=userSpaceOnUse>'+t['pat']+'</pattern>', s, flags=re.S)
    s = s.replace('<circle cx=540 cy=1650 r=360 fill="url(#sun)"/>', t['sun'])
    s = s.replace('background:#1b0f2e', 'background:'+t['pagebg'])
    # dekor
    a = s.index('// yıldızlar'); b = s.index('// renkler')
    s = s[:a] + '// tema dekoru' + t['decor'] + s[b:]
    # renkler
    c = t['col']
    s = re.sub(r"const SAND=.*?;\n", "const SAND='%(SAND)s', AEG='%(AEG)s', TERRA='%(TERRA)s', NEUT='%(NEUT)s', MARB='%(MARB)s', GOLD='%(GOLD)s';\n" % c, s, count=1)
    s = s.replace("'#2b0f3a'", "'"+t['dark']+"'").replace("fill:'#fff1cf'},cta)", "fill:'"+t['cta']+"'},cta)")
    # simge
    a = s.index("const eye="); b = s.index("\nconst header=")
    s = s[:a] + "const eye=el('g',{opacity:0});" + t['icon'] + s[b:]
    # metinler
    s = s.replace('ANTİK MISIR GEOMETRİSİ', t['header']).replace('PİRAMİTLERİN ÇAĞI', t['sub'])
    s = s.replace('Piramit çağında şekil konuşurdu', t['tsub']).replace('Piramit çağında formül yoktu, şekil vardı', t['sub0'])
    s = s.replace("T(%r,540,290,40,GOLD,{'letter-spacing':4})" % t['header'], "T(%r,540,290,38,GOLD,{'letter-spacing':3})" % t['header'])
    d = f"{R}/icerik/{t['slug']}"; os.makedirs(d+'/ses', exist_ok=True)
    open(d+'/sahne.html','w',encoding='utf-8').write(s)
    open(d+'/ses.json','w').write(open(f'{R}/icerik/misir-iki-kare-farki/ses.json').read())
    lines = open(f'{R}/icerik/misir-iki-kare-farki/ses/metin.txt',encoding='utf-8').read().split('\n')
    lines[0] = t['line1']; open(d+'/ses/metin.txt','w',encoding='utf-8').write('\n'.join(lines))
    p = dict(POST); p.update(baslik=f"İki kare farkı özdeşliği: {t['slugtr']} temalı şekille kanıt", caption=t['caption'],
        hashtagler=POST['hashtagler'][:-2]+[t['tag'],'öğretmen'], durum='taslak', kayit=['2026-11-17 oluşturuldu ('+t['slugtr']+' teması)'],
        kaynak='Kullanıcının gönderdiği ders kitabı görseli; '+t['slugtr']+' temalı özgün yeniden tasarım')
    json.dump(p, open(d+'/post.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
    print('üretildi:', t['slug'])
for k in (sys.argv[1:] or list(T)): build(k)
