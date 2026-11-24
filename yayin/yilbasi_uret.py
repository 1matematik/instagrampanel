#!/usr/bin/env python3
"""Mathlemur "YENİ YILI KUTLUYOR" şablonu (24 Kas kararı; Aralık yayını için örnek).
Karekök yılbaşı ağacı: satır k = k(k-1) .. k(k+1)-1 arası sayıların kökleri (2k tane); 1. satırda sadece √1.
Altı satırdan sonra gövde algoritmik olarak süslerle dolar. Kural anlatılırken ağaç ekranda kalır ve süslenmeye devam eder.
Kullanım: python3 yayin/yilbasi_uret.py   → icerik/yilbasi-01/{sahne.html, ses.json, ses/metin.txt, post.json} (taslak)"""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import kok_uret as K
import mufredat_uret as MU

R = K.R
soz = K.soz
GOLD, CY = '#f6c945', '#6ee7ff'

def tanim():
    ses = ["Ben Matlemur! Yeni yılı karekökle kutluyorum. Bakalım kökten bir yılbaşı ağacı çıkacak mı?",
           f"Tepede kök bir. Altında kökü ikiye yakın sayılar: kök {soz(2)}, kök {soz(3)}, kök {soz(4)}, kök {soz(5)}.",
           f"Sonra kökü üçe yakın sayılar: {soz(6)}dan {soz(11)}e kadar. Her satır iki sayı daha geniş!",
           "Dördüncü ve beşinci satır, ağaç böyle büyüyor!",
           "Satırlar genişleyince gövdeyi toplarla, ışıklarla doldurduk. Ağaç süsleniyor!",
           f"Kural: her satır bir öncekinden iki sayı fazla. Dördüncü satır {soz(12)}yle başlar, {soz(19)}la biter!",
           "Mutlu yıllar! Kaydet ve takip et!"]
    alt = ["Ben Matlemur! Yeni yılı karekökle kutluyorum. Bakalım kökten bir yılbaşı ağacı çıkacak mı?",
           "Tepede kök 1. Altında kökü 2'ye yakın sayılar: √2, √3, √4, √5.", "Sonra kökü 3'e yakın sayılar: 6'dan 11'e kadar. Her satır 2 sayı daha geniş!",
           "Dördüncü ve beşinci satır, ağaç böyle büyüyor!", "Satırlar genişleyince gövdeyi toplarla, ışıklarla doldurduk. Ağaç süsleniyor!",
           "Kural: her satır bir öncekinden 2 sayı fazla. Dördüncü satır 12'yle başlar, 19'la biter!", "Mutlu yıllar! Kaydet ve takip et!"]
    cap = ("MATHLEMUR YENİ YILI KUTLUYOR 🎄\n\nKarekökten yılbaşı ağacı! Her satır, kökü o satır numarasına en yakın doğal sayılardan oluşuyor:\n"
           "√1\n√2 √3 √4 √5\n√6 √7 … √11\n√12 … √19 …\n\nKural: her satır bir öncekinden 2 sayı daha geniş. Örnek: 4. satır 12'den 19'a kadar, 8 sayı.\n\n"
           "Yeni yılın hepimize güzel matematikler getirmesi dileğiyle ✨\n\nKaydet, LGS matematik için lazım olur 📌\n\nHer gün matematik için takip et 👆")
    b, end = MU.beats(ses)
    cfg = dict(kind='yilbasi', accent=GOLD, title='YENİ YILI KUTLUYOR', label='KÖKLERLE YILBAŞI AĞACI', beats=b, end=end, cta=round(b[-1] + .6, 2), subs=alt,
               bursts=[[b[6] + .1, 540, 600, GOLD], [b[6] + .5, 300, 760, '#ff8fa3'], [b[6] + .8, 780, 760, CY]], rings=[[b[6] + .1, GOLD, 600]])
    return 'yilbasi-01', 'Mathlemur yeni yılı kutluyor: karekökten yılbaşı ağacı', cfg, ses, cap

ON = MU.JS[:MU.JS.index("let big,mini")]
ON = ON.replace("const tit=T('2028 RADARI',540,420,112,WH,{filter:'url(#glow)'});",
                "const tit=T(CFG.title,540,420,100,WH,{filter:'url(#glow)'}); {const w=tit.getComputedTextLength(); if(w>960)tit.setAttribute('font-size',100*960/w)}")
ARA = MU.JS[MU.JS.index("/*MASCOT*/"):MU.JS.index("function content(t){")]
SON = MU.JS[MU.JS.index("function mascot(t){"):]
ORTA = r"""
const YESIL='#7be08a', TURUNCU='#ffb347', MOR='#d98bff', KIRMIZI='#ff6b6b', PEMBE='#ff8fa3';
const ORN=[KIRMIZI,GOLD,CY,TURUNCU,MOR];
const RC=['#fff1b0','#7be08a','#6ee7ff','#ffb347','#d98bff','#ff8fa3'];
function rad(n,cx,cy,s,col,parent){
 const g=el('g',{opacity:0},parent); const txt=T(String(n),0,cy,s,col,{'text-anchor':'start','font-weight':900},g);
 const w=txt.getComputedTextLength(), tot=.56*s+w+.1*s, x0=cx-tot/2, yt=cy-.8*s; txt.setAttribute('x',x0+.56*s);
 el('path',{d:`M${x0},${cy-.36*s} L${x0+.1*s},${cy-.42*s} L${x0+.28*s},${cy+.1*s} L${x0+.5*s},${yt} L${x0+tot},${yt}`,stroke:col,'stroke-width':Math.max(3,.075*s),fill:'none','stroke-linejoin':'round','stroke-linecap':'round'},g);
 return g}
const treeG=el('g',{}), ROWS=[], PIT=100, S=46, Y0=660, DY=84;
for(let k=1;k<=5;k++){
 const lo=k===1?1:k*k-k, hi=k*k+k-1, items=[], cnt=hi-lo+1;
 for(let n=lo,i=0;n<=hi;n++,i++){const cx=540+(i-(cnt-1)/2)*PIT, cy=Y0+(k-1)*DY; items.push({g:rad(n,cx,cy,S,RC[k-1],treeG),cx,cy})}
 ROWS.push({k,items,cnt})}
// yıldız
const star=el('g',{opacity:0},treeG); el('path',{d:'M540,478 L554,526 L602,540 L554,554 L540,602 L526,554 L478,540 L526,526 Z',fill:GOLD,stroke:'#fff1b0','stroke-width':4,'stroke-linejoin':'round',filter:'url(#glow)'},star);
// gövde süs satırları (algoritmik doldurma)
const BODY=[]; for(let j=0;j<3;j++){const cnt=16, cy=1045+j*46; for(let i=0;i<cnt;i++){const cx=540+(i-(cnt-1)/2)*62+(j%2?31:0)*0; const c=el('circle',{cx,cy,r:15,fill:ORN[(i+j)%5],stroke:'rgba(255,255,255,.7)','stroke-width':3,opacity:0},treeG); BODY.push({c,cx,cy,j,i,ph:(i*37+j*91)%100/100*6.28})}}
const trunk=el('rect',{x:505,y:1166,width:70,height:30,rx:8,fill:'#8b5a2b',stroke:'#5a3a1a','stroke-width':4,opacity:0},treeG);
// satır araları toplar (kural anlatılırken eklenir)
const BALLS=[]; ROWS.forEach(r=>{for(let i=0;i<r.cnt-1;i++){ if((i+r.k)%3!==0) continue; const x=(r.items[i].cx+r.items[i+1].cx)/2, y=r.items[i].cy-62; BALLS.push({c:el('circle',{cx:x,cy:y,r:9,fill:ORN[(i+r.k)%5],stroke:'#fff','stroke-width':2,opacity:0},treeG),x,y,k:r.k,i})}});
BALLS.sort((a,b)=>(a.k*10+a.i)-(b.k*10+b.i));
// kar
const SNOW=[]; for(let i=0;i<40;i++){const x=(i*173)%1080, ph=(i*57)%100/100; SNOW.push({c:el('circle',{r:3+(i%4),fill:'#fff',opacity:0},main),x,ph,sp:60+(i%5)*22})}
// kural + tebrik
const kuralG=el('g',{opacity:0}); T('KURAL',540,330,40,GOLD,{'letter-spacing':10},kuralG); TF('her satır 2 sayı daha geniş',540,405,60,WH,940,{filter:'url(#glow)'},kuralG); T('4. satır: 12 … 19 (8 sayı)',540,470,46,CY,{},kuralG);
const mutlu=T('MUTLU YILLAR!',540,420,110,GOLD,{opacity:0,filter:'url(#glow)'}); {const w=mutlu.getComputedTextLength(); if(w>960)mutlu.setAttribute('font-size',110*960/w)}
"""
CONTENT = r"""
function content(t){
 const T6=B[3]+(B[4]-B[3]);
 const RS=[B[1]+.9,B[2],B[3],B[3]+(B[4]-B[3])*.45]; 
 setT(star,ramp(t,B[1]-.1,B[1]+.5),.4+.6*back(ramp(t,B[1]-.1,B[1]+.6)),540,540);
 ROWS.forEach((r,ri)=>{r.items.forEach((o,i)=>{const t0=(ri===0?B[1]+.3:RS[ri-1])+i*.16, a=ramp(t,t0,t0+.35); setT(o.g,a,.5+.5*back(a),o.cx,o.cy)})});
 BODY.forEach(o=>{const t0=B[4]+o.j*.5+o.i*.04, a=ramp(t,t0,t0+.3); const tw=(t>B[4]+1.5)?(.75+.25*Math.sin(t*4+o.ph)):1; o.c.setAttribute('opacity',a*tw); o.c.setAttribute('r',15*(.5+.5*back(a)))});
 trunk.setAttribute('opacity',ramp(t,B[4]+1.4,B[4]+1.9));
 BALLS.forEach((o,n)=>{const t0=B[5]+.3+n*.09, a=ramp(t,t0,t0+.3); o.c.setAttribute('opacity',a); o.c.setAttribute('r',(9+(t>t0?1.5*Math.sin(t*5+n):0))*(.4+.6*back(a)))});
 SNOW.forEach((o,i)=>{const a=ramp(t,B[3]-.5+ (i%10)*.2,B[3]+.3+(i%10)*.2); const y=((t*o.sp+o.ph*1900)%1900); o.c.setAttribute('opacity',.8*a*(1-ramp(t,END-.5,END))); o.c.setAttribute('cx',o.x+25*Math.sin(t*1.3+i)); o.c.setAttribute('cy',y)});
 // başlık → kural → tebrik
 const tOff=1-ramp(t,B[5]-.15,B[5]+.25); setT(tag,tOff*(1-ramp(t,B[5],B[5]+.01)*0),1,540,300); setT(tit,tOff,1,540,420);
 const kv=ramp(t,B[5]+.2,B[5]+.65)*(1-ramp(t,B[6]-.1,B[6]+.3)); setT(kuralG,kv,.9+.1*back(ramp(t,B[5]+.2,B[5]+.7)),540,400);
 const mv=ramp(t,B[6]+.1,B[6]+.6); setT(mutlu,mv,.7+.3*back(mv),540,400);
}
"""
JS_Y = ON + ORTA + ARA + CONTENT + SON

def sahne_html(cfg):
    MU.JS = JS_Y
    h = MU.sahne_html(cfg)
    for a, b in [('#06162e', '#04200f'), ('#10386c', '#14502a'), ('#071a33', '#06210f'), ('#8fb8ff', '#a6e8b0')]:
        h = h.replace(a, b)
    return h

def yaz(slug, baslik, cfg, ses, cap):
    d = f'{R}/icerik/{slug}'; os.makedirs(d + '/ses', exist_ok=True)
    open(d + '/sahne.html', 'w', encoding='utf-8').write(sahne_html(cfg))
    open(d + '/ses/metin.txt', 'w', encoding='utf-8').write('\n'.join(ses) + '\n')
    b = cfg['beats']; sfx = [{'t': 0.3, 'tip': 'pop', 'g': .5}]
    for i, t in enumerate(b):
        if i: sfx.append({'t': round(t + .05, 2), 'tip': 'whoosh_kisa', 'g': .6})
    sfx += [{'t': round(b[1] + .1, 2), 'tip': 'sparkle', 'g': .5}, {'t': round(b[4] + .4, 2), 'tip': 'pop', 'g': .6},
            {'t': round(b[5] + .3, 2), 'tip': 'ding', 'g': .55}, {'t': round(b[6] + .1, 2), 'tip': 'sparkle', 'g': .6}, {'t': round(cfg['cta'] + .3, 2), 'tip': 'pop', 'g': .6}]
    sfx.sort(key=lambda e: e['t'])
    uzun = [m for m in K.MUZ if float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{R}/kutuphane/muzik/{m}']).decode()) >= 80]
    json.dump({'sure': cfg['end'], 'bpm': 128, 'sfx': sfx, 'sahne_basi': b, 'sahne_sonu': cfg['end'],
               'muzik_dosya': 'kutuphane/muzik/' + uzun[0], 'muzik_baslangic': 6}, open(d + '/ses.json', 'w', encoding='utf-8'), ensure_ascii=False)
    post = {'baslik': baslik, 'tur': 'özgün', 'sure': 60, 'fps': 30, 'caption': cap, 'hashtagler': ['yeniyıl', 'yılbaşı', 'matematik', 'karekök', 'keşfet'],
            'kaynak': 'Karekök yılbaşı ağacı şablonu; özgün Mathlemur tasarımı (kullanıcı fikri)', 'durum': 'taslak', 'ana_izgara': False,
            'kayit': ['yılbaşı şablonu taslağı üretildi (Aralık yayını; tarihi kullanıcı belirleyecek)']}
    json.dump(post, open(f'{d}/post.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2); open(f'{d}/post.json', 'a').write('\n')
    return slug

if __name__ == '__main__':
    print(yaz(*tanim()))
