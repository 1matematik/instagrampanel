#!/usr/bin/env python3
"""Mathlemur "TEK SAYILARIN SIRRI" serisi üretici (24 Kas kararı; fikir: 1+3+5+…+(2n−1) = n², L şekilleriyle).
Zincir: her bölüm "geçen cevap" + formül + yeni soru. Orman renkleri, doğal hareket sesleri, efektler kısık (muzik.py).
Kullanım: python3 yayin/tek_uret.py [tek-01 tek-02]
Çıktı: icerik/<slug>/{sahne.html, ses.json, ses/metin.txt, post.json}  (durum taslak)"""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import kok_uret as K
import mufredat_uret as MU
import duello_uret as D

R = K.R
soz = K.soz
GOLD, CY = '#f6c945', '#6ee7ff'
ETIKET = ['karesayılar', 'lgsmatematik', 'matematik', 'örüntü', 'keşfet']

def bolum(no):
    if no == 1:
        ses = ["Ben Matlemur! Tek sayıları art arda toplayınca hep tam kare çıkıyor. Neden?",
               f"Bir blokla başlıyorum. Toplam {soz(1)}.",
               f"Etrafına L şeklinde {soz(3)} blok ekle. Toplam {soz(4)}, yani {soz(2)} kere {soz(2)}!",
               f"{soz(5)} blok daha, toplam {soz(9)}. {soz(7)} blok daha, toplam {soz(16)}, {soz(4)} kere {soz(4)}!",
               f"Her L, bir satır, bir sütun ve bir köşe. O yüzden hep iki artıyor: {soz(1)}, {soz(3)}, {soz(5)}, {soz(7)}.",
               "Formül: n tane tek sayının toplamı, n kare!",
               f"Sıra sende! Bir artı üç artı beş, devam et, {soz(19)}a kadar. Kaç eder? Cevap sonraki videoda, takip et!"]
        alt = ["Ben Matlemur! Tek sayıları art arda toplayınca hep tam kare çıkıyor. Neden?", "1 blokla başlıyorum. Toplam 1.",
               "Etrafına L şeklinde 3 blok ekle. Toplam 4, yani 2 kere 2!", "5 blok daha, toplam 9. 7 blok daha, toplam 16, 4 kere 4!",
               "Her L, bir satır, bir sütun ve bir köşe. O yüzden hep 2 artıyor: 1, 3, 5, 7.", "Formül: n tane tek sayının toplamı, n kare!",
               "Sıra sende! 1 + 3 + 5 + … + 19 kaç eder? Cevap sonraki videoda, takip et!"]
        q = '1 + 3 + 5 + … + 19'
        cap = ("TEK SAYILARIN SIRRI • Bölüm 1 🧩\n\n1 + 3 + 5 + 7 + … toplamı neden hep tam kare çıkıyor?\n\n"
               "1 → 1²\n1 + 3 → 2²\n1 + 3 + 5 → 3²\n1 + 3 + 5 + 7 → 4²\n\nFormül: n tane tek sayının toplamı n² 📌\n\n"
               "SIRA SENDE: 1 + 3 + 5 + … + 19 kaç eder? Yoruma yaz, cevap sonraki videoda!\n\nKaydet, LGS matematik için lazım olur 📌\n\nHer gün matematik için takip et 👆")
        cfg_extra = dict(q=q)
    else:
        ses = ["Ben Matlemur! Geçen sorumuz: bir artı üç artı beş, on dokuza kadar. Cevap, yüz!",
               "Önce terim sayısını buluyoruz. n’inci tek sayı, iki n eksi bir.",
               f"{soz(19)} eşittir iki n eksi bir. Buradan n, {soz(10)}.",
               f"{soz(10)} tane tek sayı, {soz(10)} kare. Yani {soz(100)}!",
               f"Yeni soru: bir artı üç artı beş, devam et, {soz(39)}a kadar. Kaç eder?",
               "İpucu: önce terim sayısını bul, sonra karesini al!",
               "Yoruma yaz, cevap sonraki videoda. Kaydet ve takip et!"]
        alt = ["Ben Matlemur! Geçen sorumuz: 1 + 3 + 5 + … + 19. Cevap, 100!", "Önce terim sayısını buluyoruz. n’inci tek sayı, 2n − 1.",
               "19 = 2n − 1. Buradan n = 10.", "10 tane tek sayı, 10 kare. Yani 100!",
               "Yeni soru: 1 + 3 + 5 + … + 39 kaç eder?", "İpucu: önce terim sayısını bul, sonra karesini al!", "Yoruma yaz, cevap sonraki videoda. Kaydet ve takip et!"]
        q = '1 + 3 + 5 + … + 39'
        cap = ("TEK SAYILARIN SIRRI • Bölüm 2 🧩\n\nGeçen sorunun cevabı: 1 + 3 + 5 + … + 19 = 10² = 100 ✅\n\n"
               "Püf nokta: önce terim sayısı. n’inci tek sayı 2n − 1 olduğundan 19 = 2n − 1 → n = 10.\n\n"
               "YENİ SORU: 1 + 3 + 5 + … + 39 kaç eder? Yoruma yaz, cevap sonraki videoda!\n\nKaydet, LGS matematik için lazım olur 📌\n\nHer gün matematik için takip et 👆")
        cfg_extra = dict(q=q)
    b, end = MU.beats(ses)
    cfg = dict(kind=f'tek{no}', accent=GOLD, label=f'TEK SAYILARIN SIRRI • BÖLÜM {no}', beats=b, end=end, cta=round(b[-1] + .6, 2), subs=alt,
               bursts=[[b[5] + .35, 540, 860, GOLD]], rings=[[b[5] + .35, GOLD, 860]], **cfg_extra)
    return f'tek-{no:02d}', f'Tek Sayıların Sırrı {no}: 1+3+5+… neden kare?', cfg, ses, cap

# ---------------------------------------------------------------- sahne JS (mufredat_uret çerçevesi)
ON = MU.JS[:MU.JS.index("let big,mini")]
ON = ON.replace("const tit=T('2028 RADARI',540,420,112,WH,{filter:'url(#glow)'});",
                "const tit=T('TEK SAYILARIN SIRRI',540,420,100,WH,{filter:'url(#glow)'}); {const w=tit.getComputedTextLength(); if(w>960)tit.setAttribute('font-size',100*960/w)}")
ARA = MU.JS[MU.JS.index("/*MASCOT*/"):MU.JS.index("function content(t){")]
SON = MU.JS[MU.JS.index("function mascot(t){"):]
ORTA = r"""
const YESIL='#7be08a', TURUNCU='#ffb347', MOR='#d98bff';
const LAY=[GOLD,YESIL,CY,TURUNCU,MOR];
const KINT=CFG.kind;
// ---- ortak: soru kartı
const qG=el('g',{opacity:0}); el('rect',{x:70,y:590,width:940,height:410,rx:46,fill:'rgba(10,50,25,.82)',stroke:GOLD,'stroke-width':6},qG);
T('SIRA SENDE',540,675,46,GOLD,{'letter-spacing':10},qG); TF(CFG.q,540,800,120,WH,860,{filter:'url(#glow)'},qG); T('KAÇ EDER?',540,925,88,CY,{filter:'url(#glow)'},qG);
// ---- Bölüm 1: blok ızgarası
const CSZ=96, GX=540-2*CSZ, GY=555, CE=[];
const gridG=el('g',{opacity:0}), cnt=T('',540,1040,60,WH,{opacity:0}), plus=[];
for(let k=1;k<=4;k++){
 const cells=[]; for(let i=1;i<=k;i++){cells.push([i,k])} for(let j=k-1;j>=1;j--){cells.push([k,j])}   // (satır,sütun)
 cells.forEach(([r,c],n)=>{const x=GX+(c-1)*CSZ, y=GY+(r-1)*CSZ;
  const rc=el('rect',{x:x+5,y:y+5,width:CSZ-10,height:CSZ-10,rx:16,fill:LAY[k-1],stroke:'rgba(255,255,255,.55)','stroke-width':3},gridG);
  CE.push({rc,k,n,r,c,cx:x+CSZ/2,cy:y+CSZ/2})});
 const ex=cells[Math.floor(cells.length/2)]; plus.push(T('+'+(2*k-1),GX+(k-1)*CSZ+CSZ/2+(k>1?CSZ*.0:0),GY+(k-1)*CSZ+CSZ/2+16,40,'#06210f',{opacity:0,'font-weight':900},gridG));
}
plus[0].textContent='1';
const brace=el('g',{opacity:0}); T('3',GX+4*CSZ+36,GY+1.5*CSZ+14,52,CY,{},brace); T('3',GX+1.5*CSZ+8,GY+4*CSZ+62,52,YESIL,{},brace); T('+1',GX+3.5*CSZ,GY+3.5*CSZ+60,0,GOLD,{},brace);
const introT=TF('1 + 3 + 5 + 7 + … = ?',540,800,92,WH,900,{opacity:0,filter:'url(#glow)'}); const hint=T('3 + 3 + 1 = 7',540,1118,64,WH,{opacity:0,filter:'url(#glow)'});
const fG=el('g',{opacity:0}); el('rect',{x:50,y:620,width:980,height:430,rx:46,fill:'rgba(10,50,25,.82)',stroke:GOLD,'stroke-width':6},fG);
TF('1 + 3 + 5 + … + (2n − 1)',540,740,84,WH,900,{filter:'url(#glow)'},fG); T('=',540,845,80,GOLD,{},fG); T('n²',540,985,150,GOLD,{filter:'url(#glow)'},fG);
// ---- Bölüm 2: denklem satırları
const e2=[['Geçen soru',CFG.q.replace('39','19'),0],['n. tek sayı','2n − 1',1],['19 = 2n − 1',' n = 10',2],['10² =','100',3]];
const E2=el('g',{opacity:0});
T('GEÇEN CEVAP',540,640,50,CY,{'letter-spacing':10},E2); const cevapB=TF('1 + 3 + 5 + … + 19 = ?',540,730,84,WH,900,{},E2); const cevapV=T('100',540,900,170,GOLD,{filter:'url(#glow)',opacity:0},E2);
const ipucuG=el('g',{opacity:0}); T('ÖNCE TERİM SAYISI',540,700,66,YESIL,{filter:'url(#glow)'},ipucuG); T('n’inci tek sayı',540,830,56,'#cfe8d4',{},ipucuG); T('2n − 1',540,960,150,GOLD,{filter:'url(#glow)'},ipucuG);
const eqG=el('g',{opacity:0}); T('19 = 2n − 1',540,740,110,WH,{filter:'url(#glow)'},eqG); const eqN=T('n = 10',540,900,150,YESIL,{filter:'url(#glow)',opacity:0},eqG);
const sonG=el('g',{opacity:0}); T('10 TANE TEK SAYI',540,700,60,CY,{'letter-spacing':4},sonG); TF('10² = 100',540,880,170,GOLD,900,{filter:'url(#glow)'},sonG);
const ipG=el('g',{opacity:0}); T('İPUCU',540,700,48,GOLD,{'letter-spacing':10},ipG); T('1) TERİM SAYISINI BUL',540,810,56,WH,{},ipG); T('2) KARESİNİ AL',540,910,56,YESIL,{},ipG);
"""
CONTENT = r"""
function content(t){
 const fin=ramp(t,B[6]-.05,B[6]+.4), fo=1-fin;
 if(KINT==='tek1'){
  {const iv=ramp(t,.4,.9)*(1-ramp(t,B[1]-.1,B[1]+.2)); setT(introT,iv,.85+.15*back(ramp(t,.4,.9)),540,800)}
  const gA=ramp(t,B[1]-.1,B[1]+.3)*(1-ramp(t,B[5]-.1,B[5]+.3))*fo; gridG.setAttribute('opacity',gA);
  const LS=[B[1],B[2],B[3],B[3]+(B[4]-B[3])*.55];
  let tot=0;
  CE.forEach(o=>{const t0=LS[o.k-1]+o.n*.1, a=ramp(t,t0,t0+.4); const s=a>0?.4+.6*back(a):.4;
   o.rc.setAttribute('opacity',a); o.rc.setAttribute('transform',`translate(${o.cx},${o.cy}) scale(${s}) translate(${-o.cx},${-o.cy})`);
   if(a>.95)tot++;
   const hl=ramp(t,B[4]+.2,B[4]+.8)*(1-ramp(t,B[5]-.1,B[5]+.3)); if(o.k===4&&hl>0){const arm=(o.c===4&&o.r<4)?CY:(o.r===4&&o.c<4)?YESIL:GOLD; o.rc.setAttribute('fill',hl>.5?arm:LAY[3]); o.rc.setAttribute('stroke',hl>.5?'#fff':'rgba(255,255,255,.55)')}else if(o.k===4){o.rc.setAttribute('fill',LAY[3])}});
  plus.forEach((p,k)=>{const a=ramp(t,LS[k]+.5,LS[k]+.9)*(1-ramp(t,B[4]-.1,B[4]+.2)); p.setAttribute('opacity',a)});
  const kv=[0,1,4,9,16]; let m=0; for(let k=1;k<=4;k++){if(t>=LS[k-1]+.5)m=k}
  cnt.textContent=m?`${kv[m]} BLOK`:''; cnt.setAttribute('opacity',ramp(t,B[1]+.3,B[1]+.7)*(1-ramp(t,B[5]-.1,B[5]+.3))*fo);
  const hv=ramp(t,B[4]+.3,B[4]+.8)*(1-ramp(t,B[5]-.1,B[5]+.3))*fo; hint.setAttribute('opacity',hv); setT(hint,hv,.85+.15*back(ramp(t,B[4]+.3,B[4]+.8)),540,1118);
  const fv=ramp(t,B[5]+.1,B[5]+.6)*fo; setT(fG,fv,.85+.15*back(ramp(t,B[5]+.1,B[5]+.7)),540,840);
  setT(qG,fin,.85+.15*back(fin),540,795);
 } else {
  const cv=ramp(t,.3,.8)*(1-ramp(t,B[1]-.1,B[1]+.3)); E2.setAttribute('opacity',cv); setT(E2,cv,.9+.1*eo(ramp(t,.3,.8)),540,800);
  cevapV.setAttribute('opacity',ramp(t,B[0]+3.2,B[0]+3.8)); setT(cevapV,ramp(t,B[0]+3.2,B[0]+3.8),.6+.4*back(ramp(t,B[0]+3.2,B[0]+3.9)),540,880);
  const iv=ramp(t,B[1]+.1,B[1]+.5)*(1-ramp(t,B[2]-.05,B[2]+.25)); setT(ipucuG,iv,.85+.15*back(ramp(t,B[1]+.1,B[1]+.6)),540,830);
  const qv=ramp(t,B[2]+.05,B[2]+.45)*(1-ramp(t,B[3]-.05,B[3]+.25)); setT(eqG,qv,.85+.15*back(ramp(t,B[2]+.05,B[2]+.55)),540,820);
  eqN.setAttribute('opacity',ramp(t,B[2]+1.6,B[2]+2.1));
  const sv=ramp(t,B[3]+.1,B[3]+.5)*(1-ramp(t,B[4]-.05,B[4]+.25)); setT(sonG,sv,.85+.15*back(ramp(t,B[3]+.1,B[3]+.6)),540,800);
  const pv=ramp(t,B[5]+.1,B[5]+.5)*(1-ramp(t,B[6]-.05,B[6]+.25)); setT(ipG,pv,.9+.1*back(ramp(t,B[5]+.1,B[5]+.5)),540,810);
  const qq=ramp(t,B[4]+.1,B[4]+.5)*(1-ramp(t,B[5]-.05,B[5]+.25)); setT(qG,Math.max(qq,fin),.85+.15*back(Math.max(qq,fin)),540,850);
 }
}
"""
JS_T = ON + ORTA + ARA + CONTENT + SON

def sahne_html(cfg):
    MU.JS = JS_T
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
    sfx += [{'t': round(b[1] + .2, 2), 'tip': 'pop', 'g': .6}, {'t': round(b[2] + .2, 2), 'tip': 'pop', 'g': .6},
            {'t': round(b[3] + .2, 2), 'tip': 'pop', 'g': .6}, {'t': round(b[5] + .3, 2), 'tip': 'ding', 'g': .55},
            {'t': round(b[5] + .4, 2), 'tip': 'sparkle', 'g': .5},
            {'t': round(cfg['cta'] + .2, 2), 'tip': 'sparkle', 'g': .6}, {'t': round(cfg['cta'] + .6, 2), 'tip': 'pop', 'g': .6}]
    sfx.sort(key=lambda e: e['t'])
    uzun = [m for m in K.MUZ if float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{R}/kutuphane/muzik/{m}']).decode()) >= 80]
    no = int(slug.split('-')[1])
    json.dump({'sure': cfg['end'], 'bpm': 128, 'sfx': sfx, 'sahne_basi': b, 'sahne_sonu': cfg['end'],
               'muzik_dosya': 'kutuphane/muzik/' + uzun[(no + 2) % len(uzun)], 'muzik_baslangic': 6}, open(d + '/ses.json', 'w', encoding='utf-8'), ensure_ascii=False)
    pj = f'{d}/post.json'; old = json.load(open(pj)) if os.path.exists(pj) else {}
    post = {'baslik': baslik, 'tur': 'özgün', 'sure': 60, 'fps': 30, 'caption': cap, 'hashtagler': ETIKET,
            'kaynak': '1+3+5+…+(2n−1)=n² (L şekilli ispat); özgün Mathlemur tasarımı',
            'durum': old.get('durum', 'taslak') if old.get('durum') in ('taslak', 'onay-bekliyor') else 'taslak', 'ana_izgara': False,
            'kayit': old.get('kayit', []) + ['tek sayılar taslağı üretildi (yayın zamanını kullanıcı belirleyecek)']}
    json.dump(post, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); open(pj, 'a').write('\n')
    return slug

if __name__ == '__main__':
    secim = set(sys.argv[1:])
    for no in (1, 2):
        v = bolum(no)
        if secim and v[0] not in secim: continue
        print(yaz(*v), f'beats={len(v[2]["beats"])} end={v[2]["end"]}')
