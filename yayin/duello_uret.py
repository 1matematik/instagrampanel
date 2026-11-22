#!/usr/bin/env python3
"""Mathlemur "ÜSLÜ SAYI DÜELLOSU" serisi üretici (22 Kas kararı; fikir: iki üslü ifadenin kök alınarak karşılaştırılması).
Mathlemur hakem; "kök, ikisini de biraz daha küçültür". Orman/Kök Avcısı renkleri, doğal hareket sesleri (kısık).
Kullanım: python3 yayin/duello_uret.py [duello-01 duello-02]
Çıktı: icerik/<slug>/{sahne.html, ses.json, ses/metin.txt, post.json}  (durum taslak; yayın zamanını kullanıcı belirler)"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import kok_uret as K
import mufredat_uret as MU

R = K.R
soz = K.soz
GOLD, CY = '#f6c945', '#6ee7ff'
YESIL, TURUNCU = '#7be08a', '#ffb347'
SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
sup = lambda n: str(n).translate(SUP)
ETIKET = ['üslüsayılar', 'lgsmatematik', 'matematik', 'kökler', 'keşfet']

# (slug, baslik, sol, sag, kok, kazanan_idx, ek_not, sesler, altyazilar, sonraki)
def duello(no):
    if no == 1:
        L = dict(b='2', e0=300, e1=3, v=8); Rr = dict(b='3', e0=200, e1=2, v=9); win = 1; nxt = '2¹⁰⁰⁰ vs 10³⁰⁰'; fark = None
        ses = ["Ben Matlemur, düellonun hakemiyim! Üslü sayı düellosu başlıyor!",
               f"İki üzeri {soz(300)} mü büyük, üç üzeri {soz(200)} mü? Tahminini yoruma yaz!",
               f"Kural: kök, ikisini de biraz daha küçültür! İkisinin de {soz(100)}üncü kökünü alıyorum.",
               f"İki üzeri {soz(300)}, kökten sonra iki üzeri üç. Üç üzeri {soz(200)}, kökten sonra üç üzeri iki.",
               "İki üzeri üç sekiz. Üç üzeri iki dokuz.",
               "Sekiz, dokuzdan küçük! Kazanan üç üzeri iki yüz!",
               "Kaydet ve takip et, sıradaki düello çok yakın!"]
        alt = ["Ben Matlemur, düellonun hakemiyim! Üslü sayı düellosu başlıyor!", "2³⁰⁰ mü büyük, 3²⁰⁰ mü? Tahminini yoruma yaz!",
               "Kural: kök, ikisini de biraz daha küçültür! İkisinin de 100. kökünü alıyorum.", "2³⁰⁰ → 2³ ve 3²⁰⁰ → 3²",
               "2³ = 8 ve 3² = 9", "8 < 9! Kazanan 3²⁰⁰!", "Kaydet ve takip et, sıradaki düello çok yakın!"]
    else:
        L = dict(b='2', e0=1000, e1=10, v=1024); Rr = dict(b='10', e0=300, e1=3, v=1000); win = 0; nxt = None; fark = 'KÖKLERDE FARK SADECE 24!'
        ses = ["Ben Matlemur, düellonun hakemiyim! Üslü sayı düellosu, ikinci bölüm!",
               f"İki üzeri {soz(1000)} mi büyük, on üzeri {soz(300)} mü? Tahminini yoruma yaz!",
               f"Kural: kök, ikisini de biraz daha küçültür! İkisinin de {soz(100)}üncü kökünü alıyorum.",
               f"İki üzeri {soz(1000)}, kökten sonra iki üzeri on. On üzeri {soz(300)}, kökten sonra on üzeri üç.",
               f"İki üzeri on, {soz(1024)}. On üzeri üç, {soz(1000)}.",
               f"{soz(1024).capitalize()}, binden büyük! Kazanan iki üzeri {soz(1000)}! Köklerde fark sadece {soz(24)}, kıl payı!",
               "Kaydet ve takip et, yeni düellolar yolda!"]
        alt = ["Ben Matlemur, düellonun hakemiyim! Üslü sayı düellosu, ikinci bölüm!", "2¹⁰⁰⁰ mi büyük, 10³⁰⁰ mü? Tahminini yoruma yaz!",
               "Kural: kök, ikisini de biraz daha küçültür! İkisinin de 100. kökünü alıyorum.", "2¹⁰⁰⁰ → 2¹⁰ ve 10³⁰⁰ → 10³",
               "2¹⁰ = 1024 ve 10³ = 1000", "1024 > 1000! Kazanan 2¹⁰⁰⁰! Köklerde fark sadece 24, kıl payı!", "Kaydet ve takip et, yeni düellolar yolda!"]
    L['c'], Rr['c'] = YESIL, TURUNCU
    b, end = MU.beats(ses)
    eq = [f"{x['b']}{sup(x['e1'])} = {x['v']}" for x in (L, Rr)]
    W = (L, Rr)[win]
    cfg = dict(kind='duello', accent=GOLD, label=f'ÜSLÜ SAYI DÜELLOSU • BÖLÜM {no}', beats=b, end=end, cta=round(b[-1] + .6, 2), subs=alt,
               f=[L, Rr], win=win, eq=eq, root=100, wintxt=f"{W['b']}{sup(W['e0'])}", fark=fark, nxt=nxt,
               sign='<' if L['v'] < Rr['v'] else '>',
               bursts=[[b[5] + .35, 540, 930, GOLD], [b[5] + .8, 540, 800, '#fff1b0']], rings=[[b[5] + .35, GOLD, 930]])
    cap = (f"ÜSLÜ SAYI DÜELLOSU • Bölüm {no} ⚔️\n\n{L['b']}{sup(L['e0'])} mi büyük, {Rr['b']}{sup(Rr['e0'])} mü? Tahminini yoruma yaz!\n\n"
           f"Hakem Mathlemur'un kuralı: kök, ikisini de biraz daha küçültür.\n100. kökü alınca:\n{eq[0]}   ve   {eq[1]}\n"
           f"Kazanan: {cfg['wintxt']} 🏆\n\nKaydet, LGS matematik için lazım olur 📌\n\nHer gün matematik için takip et 👆")
    return f'duello-{no:02d}', f'Üslü Sayı Düellosu {no}: {L["b"]}^{L["e0"]} mi {Rr["b"]}^{Rr["e0"]} mü?', cfg, ses, cap

# ---------------------------------------------------------------- sahne JS (mufredat_uret çerçevesini kullanır)
ON = MU.JS[:MU.JS.index("let big,mini")]
ON = ON.replace("const tit=T('2028 RADARI',540,420,112,WH,{filter:'url(#glow)'});", "const tit=T('ÜSLÜ SAYI DÜELLOSU',540,420,100,WH,{filter:'url(#glow)'}); {const w=tit.getComputedTextLength(); if(w>960)tit.setAttribute('font-size',100*960/w)}")
ARA = MU.JS[MU.JS.index("/*MASCOT*/"):MU.JS.index("function content(t){")]
SON = MU.JS[MU.JS.index("function mascot(t){"):]
ORTA = r"""
const YESIL='#7be08a';
const COLORS=[CFG.f[0].c,CFG.f[1].c], CY0=930;
const arena=el('g',{opacity:0});
el('ellipse',{cx:540,cy:975,rx:480,ry:108,fill:'#0e3a1c',stroke:'#7be08a','stroke-width':8},arena);
el('ellipse',{cx:540,cy:975,rx:405,ry:82,fill:'none',stroke:'#7be08a','stroke-width':3,'stroke-dasharray':'14 12',opacity:.55},arena);
for(let i=0;i<15;i++){const a=Math.PI*(.08+.84*i/14), x=540+455*Math.cos(a), y=975+100*Math.sin(a); el('path',{d:`M${x},${y} q-7,-26 -15,-34 M${x},${y} q2,-30 4,-42 M${x},${y} q9,-24 17,-30`,stroke:'#5fcf72','stroke-width':5,fill:'none','stroke-linecap':'round'},arena)}
const FG=[], BX=[290,790];
CFG.f.forEach((f,s)=>{
 const g=el('g',{opacity:0}), cx=0, big=f.b.length>1;
 const bs=big?150:190, es=big?72:90, col=f.c;
 const base=T(f.b,0,CY0,bs,col,{'text-anchor':'start',filter:'url(#glow)'},g);
 const ex=T(String(f.e0),0,CY0-bs*.56,es,WH,{'text-anchor':'start'},g);
 const bw=base.getComputedTextLength(), ew=ex.getComputedTextLength(), W=bw+8+ew, x0=cx-W/2;
 base.setAttribute('x',x0); ex.setAttribute('x',x0+bw+8);
 const rg=el('g',{opacity:0},g);
 el('path',{d:`M${x0-64},${CY0-bs*.34} l16,-6 l18,${bs*.34+14} l22,-${bs*.98+4} H${x0+W+14}`,stroke:GOLD,'stroke-width':9,fill:'none','stroke-linejoin':'round','stroke-linecap':'round'},rg);
 T(String(CFG.root),x0-86,CY0-bs*.34-10,40,GOLD,{},rg);
 const vs=String(f.v).length>3?104:170, val=T(String(f.v),cx,CY0+4,vs,col,{filter:'url(#glow)',opacity:0},g);
 const bar=el('g',{opacity:0}), bx=BX[s]; T('ÜS',bx,1130,32,'#cfe8d4',{},bar);
 el('rect',{x:bx-165,y:1142,width:330,height:22,rx:11,fill:'rgba(255,255,255,.12)'},bar);
 const fill=el('rect',{x:bx-165,y:1142,width:330,height:22,rx:11,fill:col},bar);
 FG.push({g,f,ex,rg,val,bar,fill,cx:0,base,W})});
{const K=Math.min(1,900/(FG[0].W+FG[1].W+240)); FG.forEach(o=>o.k=K); FG[0].cx=Math.max(290,40+K*(96+FG[0].W/2)); FG[1].cx=Math.min(790,1040-K*(FG[1].W/2+14))}
const vsG=el('g',{opacity:0}); el('circle',{cx:540,cy:880,r:60,fill:INK,stroke:GOLD,'stroke-width':7},vsG); T('VS',540,903,56,GOLD,{filter:'url(#glow)'},vsG);
const soruT=T('HANGİSİ BÜYÜK?',540,640,92,GOLD,{filter:'url(#glow)',opacity:0});
const kuralG=el('g',{opacity:0}); T('KURAL',540,552,44,YESIL,{'letter-spacing':10},kuralG); T('KÖK, İKİSİNİ DE',540,625,62,WH,{},kuralG); T('BİRAZ DAHA KÜÇÜLTÜR',540,695,62,CY,{filter:'url(#glow)'},kuralG);
const eqT=[0,1].map(s=>T(CFG.eq[s],BX[s],1150,62,COLORS[s],{filter:'url(#glow)',opacity:0}));
const signG=el('g',{opacity:0}); el('circle',{cx:540,cy:900,r:70,fill:INK,stroke:GOLD,'stroke-width':8},signG); T(CFG.sign,540,938,100,GOLD,{filter:'url(#glow)'},signG);
const winG=el('g',{opacity:0}); T('KAZANAN',540,640,64,CY,{'letter-spacing':8},winG); TF(CFG.wintxt,540,770,130,GOLD,900,{filter:'url(#glow)'},winG);
if(CFG.fark){var farkT=T(CFG.fark,540,1130,46,WH,{opacity:0})}
const nxtG=el('g',{opacity:0}); if(CFG.nxt){T('SIRADAKİ DÜELLO',540,700,64,GOLD,{filter:'url(#glow)'},nxtG); TF(CFG.nxt,540,840,100,WH,920,{filter:'url(#glow)'},nxtG)} else {T('YENİ DÜELLOLAR',540,720,76,GOLD,{filter:'url(#glow)'},nxtG); T('YOLDA!',540,830,100,WH,{filter:'url(#glow)'},nxtG)}
"""
CONTENT = r"""
function content(t){
 const ap=ramp(t,.5,1.1);
 const fin=ramp(t,B[6]-.05,B[6]+.4), fo=1-fin;           // CTA'da düello alanı kapanır
 arena.setAttribute('opacity',ap*fo);
 vsG.setAttribute('opacity',ramp(t,.9,1.3)*(1-ramp(t,B[2]+.1,B[2]+.5))*fo);
 setT(vsG,parseFloat(vsG.getAttribute('opacity')),.6+.4*back(ramp(t,.9,1.4)),540,880);
 FG.forEach((o,s)=>{
  const a=ramp(t,.7+s*.2,1.3+s*.2), pulse=(t>B[1]&&t<B[2])?1+.04*Math.sin(t*9+s*3):1;
  // üs küçülmesi
  const p=eio(ramp(t,B[3]+.3,B[4]-.45)); const e=Math.round(o.f.e0+(o.f.e1-o.f.e0)*p); o.ex.textContent=String(e);
  const kr=ramp(t,B[2]+.5,B[2]+1.1)*(1-ramp(t,B[4]+.1,B[4]+.4));
  const expr=a*(1-ramp(t,B[4]+.05,B[4]+.4)), valv=ramp(t,B[4]+.25,B[4]+.8)*fo;
  const lose=t>=B[5]&&s!==CFG.win, win=t>=B[5]&&s===CFG.win;
  o.g.setAttribute('opacity',(a*(1-ramp(t,B[6]-.05,B[6]+.3)))*(lose?1-.55*ramp(t,B[5],B[5]+.5):1));
  const vx=valv>0?BX[s]:o.cx; o.g.setAttribute('transform',`translate(${vx},${CY0-60}) scale(${o.k*(valv>0?1:1)*pulse*(.7+.3*back(a))*(win?1+.12*eo(ramp(t,B[5],B[5]+.5)):1)*(lose?1-.15*ramp(t,B[5],B[5]+.5):1)}) rotate(${lose?-5*ramp(t,B[5],B[5]+.6):0}) translate(0,${-(CY0-60)})`);
  // bu grubun içinde ifade, kök ve değer ayrı opaklık
  [o.base,o.ex].forEach(x=>x.setAttribute('opacity',expr)); o.rg.setAttribute('opacity',kr);
  o.val.setAttribute('opacity',valv); o.val.setAttribute('transform',`translate(0,${CY0-60}) scale(${.6+.4*back(ramp(t,B[4]+.25,B[4]+.85))/o.k}) translate(0,${-(CY0-60)})`);
  o.bar.setAttribute('opacity',ap*(1-ramp(t,B[4]+.05,B[4]+.4))*fo);
  o.fill.setAttribute('width',330*(e/Math.max(CFG.f[0].e0,CFG.f[1].e0)));
  eqT[s].setAttribute('opacity',ramp(t,B[4]+.5,B[4]+1.0)*(1-ramp(t,B[5],B[5]+.4))*fo)});
 const sv=ramp(t,B[1],B[1]+.4)*(1-ramp(t,B[2]-.1,B[2]+.2)); setT(soruT,sv,.8+.2*back(ramp(t,B[1],B[1]+.5)),540,640);
 const kv=ramp(t,B[2],B[2]+.45)*(1-ramp(t,B[4]-.1,B[4]+.2)); setT(kuralG,kv,.85+.15*back(ramp(t,B[2],B[2]+.5)),540,670);
 const sg=ramp(t,B[5]+.1,B[5]+.55)*fo; setT(signG,sg,.5+.5*back(ramp(t,B[5]+.1,B[5]+.7)),540,900);
 const wv=ramp(t,B[5]+.5,B[5]+1.0)*fo; setT(winG,wv,.8+.2*back(ramp(t,B[5]+.5,B[5]+1.1)),540,720);
 if(typeof farkT!=='undefined')farkT.setAttribute('opacity',ramp(t,B[5]+1.8,B[5]+2.3)*fo);
 setT(nxtG,fin,.85+.15*back(fin),540,780);
}
"""
JS_D = ON + ORTA.replace('/*MASCOT*/', '') + ARA + CONTENT + SON

def sahne_html(cfg):
    MU.JS = JS_D
    h = MU.sahne_html(cfg)
    # orman renkleri
    for a, b in [('#06162e', '#04200f'), ('#10386c', '#14502a'), ('#071a33', '#06210f'), ('#8fb8ff', '#a6e8b0')]:
        h = h.replace(a, b)
    return h

def yaz(slug, baslik, cfg, ses, cap):
    d = f'{R}/icerik/{slug}'; os.makedirs(d + '/ses', exist_ok=True)
    open(d + '/sahne.html', 'w', encoding='utf-8').write(sahne_html(cfg))
    open(d + '/ses/metin.txt', 'w', encoding='utf-8').write('\n'.join(ses) + '\n')
    b = cfg['beats']; sfx = [{'t': 0.3, 'tip': 'pop', 'g': .5}]
    for i, t in enumerate(b):
        if i: sfx.append({'t': round(t + .05, 2), 'tip': 'whoosh_kisa', 'g': .6})          # toprak sıçrayışı (muzik.py doğal ses)
    sfx += [{'t': round(b[2] + .5, 2), 'tip': 'swish', 'g': .6}, {'t': round(b[3] + 1.2, 2), 'tip': 'tick', 'g': .35},
            {'t': round(b[4] + .3, 2), 'tip': 'pop', 'g': .6}, {'t': round(b[5] + .35, 2), 'tip': 'ding', 'g': .55},
            {'t': round(b[5] + .45, 2), 'tip': 'sparkle', 'g': .5},
            {'t': round(cfg['cta'] + .2, 2), 'tip': 'sparkle', 'g': .6}, {'t': round(cfg['cta'] + .6, 2), 'tip': 'pop', 'g': .6}]
    sfx.sort(key=lambda e: e['t'])
    import subprocess
    uzun = [m for m in K.MUZ if float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{R}/kutuphane/muzik/{m}']).decode()) >= 80]
    no = int(slug.split('-')[1])
    json.dump({'sure': cfg['end'], 'bpm': 128, 'sfx': sfx, 'sahne_basi': b, 'sahne_sonu': cfg['end'],
               'muzik_dosya': 'kutuphane/muzik/' + uzun[(no + 4) % len(uzun)], 'muzik_baslangic': 6}, open(d + '/ses.json', 'w', encoding='utf-8'), ensure_ascii=False)
    pj = f'{d}/post.json'; old = json.load(open(pj)) if os.path.exists(pj) else {}
    post = {'baslik': baslik, 'tur': 'özgün', 'sure': 60, 'fps': 30, 'caption': cap, 'hashtagler': ETIKET,
            'kaynak': 'Üslü sayı karşılaştırma (kök alma) yöntemi; özgün Mathlemur tasarımı',
            'durum': old.get('durum', 'taslak') if old.get('durum') in ('taslak', 'onay-bekliyor') else 'taslak', 'ana_izgara': False,
            'kayit': old.get('kayit', []) + ['düello taslağı üretildi (yayın zamanını kullanıcı belirleyecek)']}
    json.dump(post, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); open(pj, 'a').write('\n')
    return slug

if __name__ == '__main__':
    secim = set(sys.argv[1:])
    for no in (1, 2):
        v = duello(no)
        if secim and v[0] not in secim: continue
        print(yaz(*v), f'beats={len(v[2]["beats"])} end={v[2]["end"]}')
