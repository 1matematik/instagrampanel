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
               f"Mesela bir artı üç artı beş, {soz(19)}a kadar. {soz(10)} tane tek sayı var, {soz(10)} kare, yani {soz(100)}! Kaydet ve takip et!"]
        alt = ["Ben Matlemur! Tek sayıları art arda toplayınca hep tam kare çıkıyor. Neden?", "1 blokla başlıyorum. Toplam 1.",
               "Etrafına L şeklinde 3 blok ekle. Toplam 4, yani 2 kere 2!", "5 blok daha, toplam 9. 7 blok daha, toplam 16, 4 kere 4!",
               "Her L, bir satır, bir sütun ve bir köşe. O yüzden hep 2 artıyor: 1, 3, 5, 7.", "Formül: n tane tek sayının toplamı, n kare!",
               "Mesela 1 + 3 + 5 + … + 19. 10 tane tek sayı var, 10 kare, yani 100! Kaydet ve takip et!"]
        cap = ("TEK SAYILARIN SIRRI 🧩\n\n1 + 3 + 5 + 7 + … toplamı neden hep tam kare çıkıyor?\n\n"
               "1 → 1²\n1 + 3 → 2²\n1 + 3 + 5 → 3²\n1 + 3 + 5 + 7 → 4²\n\nFormül: n tane tek sayının toplamı n² 📌\n\n"
               "Mesela 1 + 3 + 5 + … + 19 = 10² = 100 ✅\n\nKaydet, LGS matematik için lazım olur 📌\n\nHer gün matematik için takip et 👆")
        cfg = dict(kind='tek1', title='TEK SAYILARIN SIRRI', label='KARE SAYILAR • ÖRÜNTÜ', q='1 + 3 + 5 + … + 19')
        slug, baslik, et = 'tek-01', 'Tek Sayıların Sırrı: 1+3+5+… neden kare?', ['karesayılar', 'lgsmatematik', 'matematik', 'örüntü', 'keşfet']
    else:
        ses = ["Ben Matlemur! Bir artı iki artı dört, böyle ikiye katlayarak bin yirmi dörde kadar toplasak kaç eder? Tek tek toplamak çok uzun!",
               "Püf nokta: ödünç alma! Toplamın başına fazladan bir tane bir koyuyorum.",
               "Bir artı bir, iki. İki artı iki, dört. Dört artı dört, sekiz. Taşlar zincirleme ikiye katlanıyor!",
               f"Zincir sona kadar gidiyor. {soz(512)} artı {soz(512)}, {soz(1024)}. {soz(1024)} artı {soz(1024)}, {soz(2048)}!",
               f"Ama ben bir tane ödünç almıştım. Onu geri veriyorum: {soz(2048)} eksi bir.",
               f"Cevap, {soz(2047)}! Kural: ikinin kuvvetleri toplamı, bir sonraki kuvvet eksi bir!",
               "Kaydet ve takip et!"]
        alt = ["Ben Matlemur! 1 + 2 + 4 + … + 1024 kaç eder? Tek tek toplamak çok uzun!", "Püf nokta: ödünç alma! Başa fazladan bir tane 1 koyuyorum.",
               "1 + 1 = 2. 2 + 2 = 4. 4 + 4 = 8. Taşlar zincirleme ikiye katlanıyor!", "Zincir sona kadar gidiyor. 512 + 512 = 1024. 1024 + 1024 = 2048!",
               "Ama ben bir tane ödünç almıştım. Onu geri veriyorum: 2048 − 1.", "Cevap, 2047! Kural: ikinin kuvvetleri toplamı, bir sonraki kuvvet eksi bir!", "Kaydet ve takip et!"]
        cap = ("1 + 2 + 4 + … + 1024 kaç eder? 🧮\n\nTek tek toplamayın, ÖDÜNÇ ALMA yöntemi:\n"
               "Başa fazladan 1 ekle → 1 + 1 = 2, 2 + 2 = 4, 4 + 4 = 8 … zincirleme 2048 olur.\nÖdünç aldığın 1'i geri ver: 2048 − 1 = 2047 ✅\n\n"
               "Kural: 1 + 2 + 4 + … + 2ⁿ = 2ⁿ⁺¹ − 1 📌\n\nKaydet, LGS matematik için lazım olur 📌\n\nHer gün matematik için takip et 👆")
        cfg = dict(kind='kuv1', title='ÖDÜNÇ ALMA YÖNTEMİ', label='İKİNİN KUVVETLERİ • PRATİK TOPLAM', q='1 + 2 + 4 + … + 1024')
        slug, baslik, et = 'kuvvet-01', '1+2+4+…+1024 kaç eder? Ödünç alma yöntemi', ['ikininkuvvetleri', 'lgsmatematik', 'matematik', 'pratikçözüm', 'keşfet']
    b, end = MU.beats(ses)
    cfg.update(accent=GOLD, beats=b, end=end, cta=round(b[-1] + .6, 2), subs=alt, etiket=et,
               bursts=[[b[5] + .35, 540, 860, GOLD]], rings=[[b[5] + .35, GOLD, 860]])
    return slug, baslik, cfg, ses, cap

# ---------------------------------------------------------------- sahne JS (mufredat_uret çerçevesi)
ON = MU.JS[:MU.JS.index("let big,mini")]
ON = ON.replace("const tit=T('2028 RADARI',540,420,112,WH,{filter:'url(#glow)'});",
                "const tit=T(CFG.title,540,420,100,WH,{filter:'url(#glow)'}); {const w=tit.getComputedTextLength(); if(w>960)tit.setAttribute('font-size',100*960/w)}")
ARA = MU.JS[MU.JS.index("/*MASCOT*/"):MU.JS.index("function content(t){")]
SON = MU.JS[MU.JS.index("function mascot(t){"):]
ORTA = r"""
const YESIL='#7be08a', TURUNCU='#ffb347', MOR='#d98bff', KIRMIZI='#ff6b6b';
const LAY=[GOLD,YESIL,CY,TURUNCU,MOR];
const KINT=CFG.kind;
let CE=[], plus=[], gridG, cnt, introT, hint, fG, qG;
let KCs=[], eqK, quesK, bigK, fK, backK;
if(KINT==='tek1'){
 // ---- örnek kartı (son cümle)
 qG=el('g',{opacity:0}); el('rect',{x:70,y:590,width:940,height:410,rx:46,fill:'rgba(10,50,25,.82)',stroke:GOLD,'stroke-width':6},qG);
 T('MESELA',540,675,46,GOLD,{'letter-spacing':10},qG); TF(CFG.q,540,790,120,WH,860,{filter:'url(#glow)'},qG); T('= 10² = 100',540,925,100,CY,{filter:'url(#glow)'},qG);
 const CSZ=96, GX=540-2*CSZ, GY=555;
 gridG=el('g',{opacity:0}); cnt=T('',540,1040,60,WH,{opacity:0});
 for(let k=1;k<=4;k++){
  const cells=[]; for(let i=1;i<=k;i++){cells.push([i,k])} for(let j=k-1;j>=1;j--){cells.push([k,j])}
  cells.forEach(([r,c],n)=>{const x=GX+(c-1)*CSZ, y=GY+(r-1)*CSZ;
   const rc=el('rect',{x:x+5,y:y+5,width:CSZ-10,height:CSZ-10,rx:16,fill:LAY[k-1],stroke:'rgba(255,255,255,.55)','stroke-width':3},gridG);
   CE.push({rc,k,n,r,c,cx:x+CSZ/2,cy:y+CSZ/2})});
  plus.push(T('+'+(2*k-1),GX+(k-1)*CSZ+CSZ/2,GY+(k-1)*CSZ+CSZ/2+16,40,'#06210f',{opacity:0,'font-weight':900},gridG));
 }
 plus[0].textContent='1';
 introT=TF('1 + 3 + 5 + 7 + … = ?',540,800,92,WH,900,{opacity:0,filter:'url(#glow)'}); hint=T('3 + 3 + 1 = 7',540,1118,64,WH,{opacity:0,filter:'url(#glow)'});
 fG=el('g',{opacity:0}); el('rect',{x:50,y:620,width:980,height:430,rx:46,fill:'rgba(10,50,25,.82)',stroke:GOLD,'stroke-width':6},fG);
 TF('1 + 3 + 5 + … + (2n − 1)',540,740,84,WH,900,{filter:'url(#glow)'},fG); T('=',540,845,80,GOLD,{},fG); T('n²',540,985,150,GOLD,{filter:'url(#glow)'},fG);
} else {
 const KV=[1,1,2,4,8,16,32,64,128,256,512,1024];
 quesK=TF(CFG.q+' = ?',540,530,70,WH,920,{opacity:0,filter:'url(#glow)'});
 KV.forEach((v,i)=>{const row=i<6?0:1, col=i%6, cx=140+col*160, cy=660+row*150;
  const g=el('g',{opacity:0}); const rc=el('rect',{x:cx-72,y:cy-58,width:144,height:116,rx:22,fill:i===0?'#5a1a1a':'#0e3a1c',stroke:i===0?KIRMIZI:'#7be08a','stroke-width':5},g);
  const tx=T(String(v),cx,cy+(String(v).length>3?16:20),String(v).length>3?50:60,WH,{'font-weight':900},g);
  if(i===0)T('ÖDÜNÇ',cx,cy-34,24,KIRMIZI,{},g);
  KCs.push({g,rc,tx,cx,cy,i})});
 eqK=T('',540,1010,92,WH,{opacity:0,filter:'url(#glow)'});
 bigK=T('2047',540,800,230,GOLD,{opacity:0,filter:'url(#glow)'});
 fK=el('g',{opacity:0}); el('rect',{x:50,y:900,width:980,height:150,rx:40,fill:'rgba(10,50,25,.82)',stroke:GOLD,'stroke-width':5},fK);
 TF('1 + 2 + 4 + … + 2ⁿ = 2ⁿ⁺¹ − 1',540,998,66,WH,900,{filter:'url(#glow)'},fK);
}
"""
CONTENT = r"""
function content(t){
 const fin=ramp(t,B[6]-.05,B[6]+.4), fo=1-fin;
 if(KINT==='tek1'){
  {const iv=ramp(t,.4,.9)*(1-ramp(t,B[1]-.1,B[1]+.2)); setT(introT,iv,.85+.15*back(ramp(t,.4,.9)),540,800)}
  const gA=ramp(t,B[1]-.1,B[1]+.3)*(1-ramp(t,B[5]-.1,B[5]+.3))*fo; gridG.setAttribute('opacity',gA);
  const LS=[B[1],B[2],B[3],B[3]+(B[4]-B[3])*.55];
  CE.forEach(o=>{const t0=LS[o.k-1]+o.n*.1, a=ramp(t,t0,t0+.4); const s=a>0?.4+.6*back(a):.4;
   o.rc.setAttribute('opacity',a); o.rc.setAttribute('transform',`translate(${o.cx},${o.cy}) scale(${s}) translate(${-o.cx},${-o.cy})`);
   const hl=ramp(t,B[4]+.2,B[4]+.8)*(1-ramp(t,B[5]-.1,B[5]+.3));
   if(o.k===4&&hl>0.5){o.rc.setAttribute('fill',(o.c===4&&o.r<4)?CY:(o.r===4&&o.c<4)?YESIL:GOLD)}else if(o.k===4){o.rc.setAttribute('fill',LAY[3])}});
  plus.forEach((p,k)=>{p.setAttribute('opacity',ramp(t,LS[k]+.5,LS[k]+.9)*(1-ramp(t,B[4]-.1,B[4]+.2)))});
  const kv=[0,1,4,9,16]; let m=0; for(let k=1;k<=4;k++){if(t>=LS[k-1]+.5)m=k}
  cnt.textContent=m?`${kv[m]} BLOK`:''; cnt.setAttribute('opacity',ramp(t,B[1]+.3,B[1]+.7)*(1-ramp(t,B[5]-.1,B[5]+.3))*fo);
  const hv=ramp(t,B[4]+.3,B[4]+.8)*(1-ramp(t,B[5]-.1,B[5]+.3))*fo; setT(hint,hv,.85+.15*back(ramp(t,B[4]+.3,B[4]+.8)),540,1118);
  const fv=ramp(t,B[5]+.1,B[5]+.6)*(1-ramp(t,B[6]-.05,B[6]+.3)); setT(fG,fv,.85+.15*back(ramp(t,B[5]+.1,B[5]+.7)),540,840);
  const qv=ramp(t,B[6]+.1,B[6]+.5); setT(qG,qv,.85+.15*back(qv),540,795);
 } else {
  const qa=ramp(t,.3,.8)*(1-ramp(t,B[5]-.1,B[5]+.3)); setT(quesK,qa,.9+.1*back(ramp(t,.3,.8)),540,530);
  // adım sayısı s: 0..11
  const A=B[2]+.5, Z=B[3]-.1; let s=0;
  if(t>=A&&t<B[3]) s=Math.min(3,1+Math.floor((t-A)/(Z-A)*3)); else if(t>=B[3]) s=Math.min(11,4+Math.floor(Math.max(0,t-B[3]-.1)/Math.max(.1,(B[4]-.25)-(B[3]+.1))*8));
  KCs.forEach(c=>{const a0=c.i===0?ramp(t,B[1],B[1]+.4):ramp(t,.6+c.i*.12,1.0+c.i*.12);
   const gone=c.i===0?ramp(t,B[4]+.3,B[4]+.8):0; const lit=(c.i>=1&&s>=c.i)||(c.i===0&&s>=1);
   const fade=1-ramp(t,B[5]-.05,B[5]+.35);
   c.g.setAttribute('opacity',a0*fade*(c.i===0?1-.6*gone:1));
   c.rc.setAttribute('fill',c.i===0?'#5a1a1a':(lit?'#1f7a3a':'#0e3a1c')); c.rc.setAttribute('stroke',lit&&c.i>0?'#fff':(c.i===0?KIRMIZI:'#7be08a'));
   const sc=(lit&&s===c.i)?1.12:1; c.g.setAttribute('transform',`translate(${c.cx},${c.cy}) scale(${sc}) translate(${-c.cx},${-c.cy})`)});
  const KV=[1,1,2,4,8,16,32,64,128,256,512,1024];
  let txt='', op=0;
  if(t<B[4]&&s>=1){const v=KV[s]===undefined?1024:(s===1?1:KV[s]); const vv=s===1?1:KV[s]; txt=`${vv} + ${vv} = ${2*vv}`; op=ramp(t,B[2]+.3,B[2]+.7)}
  else if(t>=B[4]&&t<B[5]+.1){txt='2048 − 1'; op=ramp(t,B[4]+.1,B[4]+.5)*(1-ramp(t,B[5]-.05,B[5]+.25))}
  eqK.textContent=txt; eqK.setAttribute('opacity',op);
  const bv=ramp(t,B[5]+.1,B[5]+.6)*fo; setT(bigK,bv,.7+.3*back(ramp(t,B[5]+.1,B[5]+.7)),540,760);
  const fv=ramp(t,B[5]+1.0,B[5]+1.5)*fo; setT(fK,fv,.9+.1*back(ramp(t,B[5]+1.0,B[5]+1.6)),540,975);
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
    no = 1 if slug.startswith('tek') else 2
    json.dump({'sure': cfg['end'], 'bpm': 128, 'sfx': sfx, 'sahne_basi': b, 'sahne_sonu': cfg['end'],
               'muzik_dosya': 'kutuphane/muzik/' + uzun[(no + 2) % len(uzun)], 'muzik_baslangic': 6}, open(d + '/ses.json', 'w', encoding='utf-8'), ensure_ascii=False)
    pj = f'{d}/post.json'; old = json.load(open(pj)) if os.path.exists(pj) else {}
    post = {'baslik': baslik, 'tur': 'özgün', 'sure': 60, 'fps': 30, 'caption': cap, 'hashtagler': cfg['etiket'],
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
