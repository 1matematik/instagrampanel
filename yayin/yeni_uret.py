#!/usr/bin/env python3
"""Mathlemur ortak sahne motoru (DSL) + yeni format üreticileri (Gün 6–18 planı, claude/yeni-formatlar-plani.md).
Her video bir 'V' nesnesiyle tarif edilir: cümleler (ses + altyazı) ve ekran öğeleri (b0 = hangi cümlede belirir, b1 = hangisinde kaybolur).
Kullanım: python3 yayin/yeni_uret.py asal            -> Asal Apartmanı (6 video)
Çıktı: icerik/<slug>/{sahne.html, ses.json, ses/metin.txt, post.json}   (durum 'taslak'; yayın için kullanıcı toplu onayı gerekir)"""
import os, sys, json, math, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import kok_uret as K
import mufredat_uret as MU

R = K.R
soz, cap = K.soz, K.cap
GOLD, CY, WH = '#f6c945', '#6ee7ff', '#f5f7fb'
YESIL, KIRMIZI = '#7be08a', '#ff6b6b'
ETIKET = ['keşfet', 'yapayzeka', 'teknoloji', 'izleöğren', 'mathlemur']

# ---------------------------------------------------------------- video tarif nesnesi
class V:
    def __init__(self, slug, baslik, seri, no):
        self.slug, self.baslik, self.seri, self.no = slug, baslik, seri, no
        self.ses, self.alt, self.items = [], [], []
    def line(self, ses, alt=None):
        self.ses.append(ses); self.alt.append(alt or ses); return len(self.ses) - 1
    def add(self, **kw):
        self.items.append(kw); return kw
    # kart: kural (yeşil), dikkat (kırmızı), sıra sende (camgöbeği)
    def kart(self, tip, b0, b1, satirlar, y=1040, baslik=None):
        col, fill, bas = {'kural': (YESIL, '#0f3a2a', 'KURAL'), 'dikkat': (KIRMIZI, '#4a1620', 'DİKKAT!'),
                          'sira': (CY, '#0f3050', 'SIRA SENDE'), 'bonus': (GOLD, '#3a3010', 'BONUS')}[tip]
        n = len(satirlar); H = 70 + 62 * n
        self.add(x=540, y=y, w=940, h=H, rx=34, fill=fill, stroke=col, sw=6, b0=b0, b1=b1)
        self.add(x=540, y=y - H / 2 + 38, txt=baslik or bas, s=34, c=col, b0=b0, b1=b1, d=.1)
        for i, (t, s, c) in enumerate([(a, 52, WH) if isinstance(a, str) else a for a in satirlar]):
            self.add(x=540, y=y - H / 2 + 100 + i * 62, txt=t, s=s, c=c, mw=880, b0=b0, b1=b1, d=.2 + .1 * i)
    def cfg(self):
        b, end = MU.beats(self.ses)
        c = b[-1]
        return dict(kind='dsl', accent=GOLD, label=f'BÖLÜM {self.no}', title=self.seri, beats=b, end=end, cta=round(c + .6, 2),
                    subs=self.alt, items=self.items, bursts=[[round(c + .1, 2), 540, 1180, GOLD]], rings=[])

# ---------------------------------------------------------------- JS (MU çerçevesine takılır)
ON = MU.JS[:MU.JS.index("let big,mini")]
ON = ON.replace("const tit=T('2028 RADARI',540,420,112,WH,{filter:'url(#glow)'});",
                "const tit=T(CFG.title,540,420,100,WH,{filter:'url(#glow)'}); {const w=tit.getComputedTextLength(); if(w>960)tit.setAttribute('font-size',100*960/w)}")
ARA = MU.JS[MU.JS.index("/*MASCOT*/"):MU.JS.index("function content(t){")]
SON = MU.JS[MU.JS.index("function mascot(t){"):]
ORTA = r"""
const IT=CFG.items.map(it=>{const g=el('g',{opacity:0});let r=null,tx=null;
 if(it.w) r=el('rect',{x:-it.w/2,y:-it.h/2,width:it.w,height:it.h,rx:it.rx==null?18:it.rx,fill:it.fill||'#12345e',stroke:it.stroke||'none','stroke-width':it.sw||4},g);
 if(it.txt!==undefined){tx=T(it.txt,0,(it.s||50)*.34,it.s||50,it.c||WH,{filter:it.glow?'url(#glow)':''},g);
  if(it.mw){const w=tx.getComputedTextLength(); if(w>it.mw) tx.setAttribute('font-size',(it.s||50)*it.mw/w)}}
 return {it,g,r,tx}});
"""
CONTENT = r"""
function content(t){
 IT.forEach(o=>{const it=o.it, a=B[it.b0]+(it.d||0), e=(it.b1==null?B[N-1]:B[it.b1]);
  const v=ramp(t,a,a+.35)*(1-ramp(t,e-.1,e+.25)), p=back(ramp(t,a,a+.5));
  let x=it.x,y=it.y;
  if(it.mv){const m0=B[it.mv[0]]+(it.mv[3]||0), q=eio(ramp(t,m0,m0+.6)); x=it.x+(it.mv[1]-it.x)*q; y=it.y+(it.mv[2]-it.y)*q}
  let sc=(.7+.3*p)*(it.k||1); if(it.pulse) sc*=1+.05*Math.sin(t*8)*ramp(t,a,a+.3);
  if(it.rc){const c0=B[it.rc[0]]+(it.rc[4]||0), k=ramp(t,c0,c0+.4);
   if(o.r){o.r.setAttribute('fill',mix(it.fill||'#12345e',it.rc[1],k)); o.r.setAttribute('stroke',mix(it.stroke||'#12345e',it.rc[2],k))}
   if(o.tx&&it.rc[3]) o.tx.setAttribute('fill',mix(it.c||WH,it.rc[3],k)); if(k>0&&k<1) sc*=1+.12*Math.sin(Math.PI*k)}
  o.g.setAttribute('opacity',v); o.g.setAttribute('transform',`translate(${x},${y}) scale(${sc})`)});
}
"""
JS_D = ON + ORTA + ARA + CONTENT + SON

def sahne_html(cfg):
    MU.JS = JS_D
    return MU.sahne_html(cfg)

def yaz(v, cap_txt, kaynak):
    cfg = v.cfg(); d = f'{R}/icerik/{v.slug}'; os.makedirs(d + '/ses', exist_ok=True)
    open(d + '/sahne.html', 'w', encoding='utf-8').write(sahne_html(cfg))
    open(d + '/ses/metin.txt', 'w', encoding='utf-8').write('\n'.join(v.ses) + '\n')
    b = cfg['beats']; sfx = [{'t': 0.3, 'tip': 'pop', 'g': .5}]
    for i, t in enumerate(b[1:-1], 1): sfx.append({'t': round(t + .3, 2), 'tip': 'tick', 'g': .3})
    sfx += [{'t': round(cfg['cta'] + .2, 2), 'tip': 'sparkle', 'g': .5}, {'t': round(cfg['cta'] + .6, 2), 'tip': 'pop', 'g': .5}]
    uzun = [m for m in K.MUZ if float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{R}/kutuphane/muzik/{m}']).decode()) >= 80]
    json.dump({'sure': cfg['end'], 'bpm': 128, 'sfx': sfx, 'sahne_basi': b, 'sahne_sonu': cfg['end'],
               'muzik_dosya': 'kutuphane/muzik/' + uzun[(v.no + hash(v.seri) % 7) % len(uzun)], 'muzik_baslangic': 6},
              open(d + '/ses.json', 'w', encoding='utf-8'), ensure_ascii=False)
    pj = f'{d}/post.json'; old = json.load(open(pj)) if os.path.exists(pj) else {}
    post = {'baslik': v.baslik, 'tur': 'özgün', 'sure': 60, 'fps': 30, 'caption': cap_txt, 'hashtagler': ETIKET, 'kaynak': kaynak,
            'durum': old.get('durum', 'taslak') if old.get('durum') in ('taslak', 'onay-bekliyor') else 'taslak', 'ana_izgara': False,
            'kayit': old.get('kayit', []) + ['yeni format taslağı üretildi (gün gelince kullanıcıdan toplu onay alınacak)']}
    json.dump(post, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); open(pj, 'a').write('\n')
    return v.slug, len(b), cfg['end']

SON_ETIKET = "\n\nKaydet, LGS'de lazım olur 📌\n\nHer gün matematik için takip et 👆"

# ================================================================ GÜN 6 · ASAL APARTMANI
def isp(n): return n > 1 and all(n % d for d in range(2, math.isqrt(n) + 1))
def bol(n):
    p = next(d for d in range(2, n + 1) if n % d == 0); return p, n // p

ASAL = [  # (sayılar, dikkat sayısı, sıra sende)
    ([2, 15, 23, 39, 41, 51], 51, 57),
    ([1, 17, 27, 31, 49, 53], 49, 91),
    ([3, 21, 37, 45, 57, 59], 57, 97),
    ([5, 33, 43, 63, 67, 91], 91, 89),
    ([7, 25, 47, 69, 71, 77], 77, 119),
    ([11, 35, 61, 81, 83, 87], 87, 121),
]

def asal_video(no):
    sayilar, dik, ss = ASAL[no - 1]
    v = V(f'asal-apt-{no:02d}', f'Asal Apartmanı {no}: hangi kapılar asal?', 'ASAL APARTMANI', no)
    # sol/sağ yerleşim 3x2
    xs = [240, 540, 840]; ys = [635, 845]
    b0 = v.line("Merhaba, ben Matlemur! Asal apartmanındayız, altı kapı çalacağım.")
    if no > 1:
        pn = ASAL[no - 2][2]; pc = 'asal' if isp(pn) else 'asal değil'
        if isp(pn): txt = f'{soz(pn)} asal! Kapıda oturur.'; alt = f'Geçen cevap: {pn} asal!'
        else: p, q = bol(pn); txt = f'{soz(pn)} asal değil: {soz(p)} çarpı {soz(q)}.'; alt = f'Geçen cevap: {pn} asal değil, {p} × {q}!'
        bg = v.line('Geçen cevap: ' + txt, alt)
        v.add(x=540, y=520, txt=alt, s=40, c=CY, mw=940, b0=bg, b1=bg + 1)
    bk = v.line("Kural: sadece bir'e ve kendine bölünen, birden büyük sayı asaldır.", "Kural: sadece 1'e ve kendine bölünen, 1'den büyük sayı asaldır.")
    v.kart('kural', bk, bk + 1, [("SADECE 1 VE KENDİNE BÖLÜNEN", 40, WH), ("1'DEN BÜYÜK SAYI = ASAL", 46, YESIL)])
    # önce kapılar (kural satırında belirsin)
    sat = []
    for i, n in enumerate(sayilar):
        sat.append(n)
    first = None
    nb = []   # her sayı için cümle indeksi
    for n in sayilar:
        if n == 1: s, a = "Bir: asal değil! Tek böleni kendisi.", "1: asal değil! Tek böleni kendisi."
        elif isp(n): s, a = f"{cap(soz(n))}: asal. Kapıda oturur!", f"{n}: asal. Kapıda oturur!"
        else:
            p, q = bol(n); s, a = f"{cap(soz(n))}: {soz(p)} çarpı {soz(q)}. Dışarı!", f"{n} = {p} × {q}. Dışarı!"
        nb.append(v.line(s, a))
    bd = v.line(f"Dikkat! {cap(soz(dik))} asal gibi durur, ama değil!" if dik != 1 else "Dikkat! Bir asal değildir.",
                f"Dikkat! {dik} asal gibi durur, ama değil!")
    bs = v.line(f"Sıra sende: {soz(ss)} asal mı? Cevabı yorumlara yaz!", f"Sıra sende: {ss} asal mı? Cevabı yorumlara yaz!")
    v.line("Yarın yine buluşalım!")
    # kapılar bk'dan itibaren görünsün, hepsi bs'ye kadar (sıra sende'de kaybolur)
    for i, n in enumerate(sayilar):
        x, y = xs[i % 3], ys[i // 3]; ok = isp(n)
        col, fil, tc = ((YESIL, '#14522e', '#9dffb0') if ok else (KIRMIZI, '#4a1620', '#ffb3b3'))
        v.add(x=x, y=y, w=290, h=130, rx=30, fill='#12345e', stroke='#6fa8ff', sw=5, txt=str(n), s=82, c=WH, b0=bk, d=.12 * i, b1=bs,
              rc=[nb[i], fil, col, tc], pulse=False)
        if n == 1: lab = 'ASAL DEĞİL'
        elif ok: lab = '✓ ASAL'
        else: p, q = bol(n); lab = f'= {p} × {q}'
        v.add(x=x, y=y + 100, txt=lab, s=40, c=col, b0=nb[i], d=.35, b1=bs)
    v.kart('dikkat', bd, bs, [(f"{dik} " + ('asal değil' if dik == 1 else '= %d × %d' % bol(dik)), 58, '#ffb3b3'), ("ASAL DEĞİL!", 44, WH)], y=1050)
    v.kart('sira', bs, bs + 1, [(f"{ss} asal mı?", 74, GOLD), ("Cevabı yorumlara yaz ↓", 36, WH)], y=1010)
    asallar = [n for n in sayilar if isp(n)]
    cap_txt = (f"ASAL APARTMANI • Bölüm {no} 🏢\n\nAltı kapı: {', '.join(map(str, sayilar))}\nAsal olanlar: {', '.join(map(str, asallar))} ✅\n"
               f"Dikkat: {dik} " + ("asal değil (tek böleni kendisi)" if dik == 1 else "asal gibi durur ama %d × %d" % bol(dik)) +
               f"\n\nSıra sende: {ss} asal mı? Cevabı yorumlara yaz!" + SON_ETIKET)
    return v, cap_txt, 'Asal sayı tanımı; özgün Mathlemur tasarımı ve sayı setleri'

GENEL = {'asal': lambda: [asal_video(i) for i in range(1, 7)]}

if __name__ == '__main__':
    secim = sys.argv[1:] or list(GENEL)
    for s in secim:
        for v, c, k in GENEL[s]():
            print(yaz(v, c, k))
