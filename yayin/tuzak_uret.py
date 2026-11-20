#!/usr/bin/env python3
"""Mathlemur Kök Avcısı - TUZAK bölümü üretici (yarım av).
Kurgu: önce küçük blokla "yarım av" (√48 = 2√12), kırmızı DİKKAT, sonra en büyük blokla tam av (√48 = 4√3).
Kullanım: python3 yayin/tuzak_uret.py  -> icerik/kok-avcisi-b07/"""
import os, sys, re, json
sys.path.insert(0, os.path.dirname(__file__))
import kok_uret as K

def tuzak(no, n, kucuk, prev, ss_n, ss_yanlis):
    """n: av sayısı, kucuk: yanlışlıkla seçilen küçük tam kare (ör. 4), prev: geçen bölümün sorusu,
    ss_n / ss_yanlis: sıra sende tuzak sorusu (ör. √72 = 36√2 ?)"""
    kk = int(kucuk ** .5); rk = n // kucuk          # yarım av: 2, 12
    k, r = K.ayir(n)                                 # tam av: 4, 3
    slug = K.bolum(no, n, n, ss_n, prev)
    d = f'{K.R}/icerik/{slug}'; p = d + '/sahne.html'; s = open(p).read()
    RED = '#ff4d5e'
    s = s.replace("const CS=Math.min(110,Math.floor(880/(r*k)),Math.floor(400/k)), bw=k*CS, W=r*bw, H=k*CS, X0=(1080-W)/2, Y0=500+(420-H)/2;",
      "const cols=Math.min(r,6), rows=Math.ceil(r/cols), GAPY=rows>1?100:0, CS=Math.min(110,Math.floor(880/(cols*k)),Math.floor((400-GAPY*(rows-1))/(rows*k))), bw=k*CS, W=cols*bw, H=k*CS, X0=(1080-W)/2, Y0=500+(420-rows*H-GAPY*(rows-1))/2;", 1)
    s = s.replace("for(let b=0;b<r;b++){const g=el('g',{},root), col=b%2?CY:GOLD, x0=X0+b*bw;",
      "for(let b=0;b<r;b++){const g=el('g',{},root), col=b%2?CY:GOLD, x0=X0+(b%cols)*bw, Yb=Y0+Math.floor(b/cols)*(H+GAPY);", 1)
    # blok içinde Y0 yerine satır yüksekliği Yb
    a = s.index("for(let b=0;b<r;b++){"); e = s.index("blocks.push(", a); e = s.index("\n", e)
    s = s[:a] + s[a:e].replace("Y0", "Yb").replace("Yb=Yb+", "Yb=Y0+") + s[e:]
    s = s.replace("blocks.forEach(b=>{el('line',{x1:b.c[0]-bw/2+6,y1:Y0+H+38,x2:b.c[0]+bw/2-6,y2:Y0+H+38,",
      "blocks.forEach(b=>{const yl=b.c[1]+H/2;el('line',{x1:b.c[0]-bw/2+6,y1:yl+38,x2:b.c[0]+bw/2-6,y2:yl+38,", 1)
    s = s.replace("T(String(k),b.c[0],Y0+H+92,", "T(String(k),b.c[0],yl+92,", 1)
    assert 'cols=' in s and 'yl+92' in s, 'ızgara yaması tutmadı'
    # 1. örnek: küçük bloklar (yarım av), 2. örnek: en büyük blok (tam av)
    s = s.replace(f"const E1=makeEx({k},{r},'{k*k}')", f"const E1=makeEx({kk},{rk},'{kucuk}')", 1)
    s = re.sub(r"const F1=fset\(.*\n", f"const F1=fset(0,[['√{n} = √(',WH],['{kucuk}',GOLD],[' · ',WH],['{rk}',CY],[')',WH]],[['√{n} = ',WH],['{kk}',GOLD],['√{rk}','{RED}']],'√{n}');\n", s)
    s = s.replace(f"const six=T('{k}',", f"const six=T('{kk}',", 1)
    # sıra sende: tuzak sorusu
    s = s.replace(f"T('√{ss_n} = ?',540,820,200", f"T('√{ss_n} = {ss_yanlis} ?',540,820,128", 1)
    # DİKKAT ve TAM AV rozetleri
    rozet = f"""// ---------- tuzak rozetleri
const RED='{RED}';
const dik=el('g',{{opacity:0}});
el('rect',{{x:120,y:560,width:840,height:200,rx:34,fill:'rgba(255,77,94,.16)',stroke:RED,'stroke-width':8}},dik);
T('⚠ DİKKAT! YARIM AV',540,645,60,RED,{{filter:'url(#glow)'}},dik);
dik.appendChild(TS([['{rk} = ',WH],['{kucuk}',GOLD],[' · ',WH],['{rk//kucuk}',CY],['  → hâlâ tam kare var!',WH]],540,720,44,{{}}));
const tam=el('g',{{opacity:0}});
el('rect',{{x:250,y:580,width:580,height:150,rx:34,fill:'rgba(110,231,255,.14)',stroke:CY,'stroke-width':6}},tam);
T('✓ TAM AV',540,680,84,GOLD,{{filter:'url(#glow)'}},tam);
function tuzakAnim(t){{
 const a=ramp(t,11.3,11.8)*(1-ramp(t,14.2,14.6)), sh=t>11.3&&t<12.3?6*Math.sin(t*60)*(1-ramp(t,11.3,12.3)):0;
 dik.setAttribute('opacity',a); dik.setAttribute('transform',`translate(${{sh}},0) translate(540,660) scale(${{.8+.2*K_back(ramp(t,11.3,11.8))}}) translate(-540,-660)`);
 const b=ramp(t,19.5,20.0)*(1-ramp(t,20.6,21.0));
 tam.setAttribute('opacity',b); tam.setAttribute('transform',`translate(540,655) scale(${{.7+.3*K_back(ramp(t,19.5,20.0))}}) translate(-540,-655)`);
}}
const K_back=back;
// ---------- sıra sende + final"""
    s = s.replace("// ---------- sıra sende + final", rozet, 1)
    s = s.replace(" extra(t);\n};", " tuzakAnim(t);\n extra(t);\n};", 1)
    SUB = [[0, 3.0, f'Geçen bölümün cevabı: √{prev} = {K.ayir(prev)[0]}√{K.ayir(prev)[1]}'],
           [3.2, 6.3, f'Tuzak avı! √{n} → {n} kare çiz'],
           [6.5, 9.1, f'Hızlı avcı {kucuk}\'lük blokları yakaladı: {rk} blok'],
           [9.3, 12.6, f'√{n} = {kk}√{rk} … DİKKAT! Yarım av!'],
           [12.8, 16.6, f'{rk}\'nin içinde {kucuk} var! Büyük blok: {k*k}'],
           [16.8, 20.6, f'Kenarı {k} → √{n} = {k}√{r}'],
           [20.8, 25.3, f'Sıra sende: √{ss_n} = {ss_yanlis} mi?'],
           [25.5, 28.6, 'Yarın yine buluşalım!']]
    s = re.sub(r"const SUB=\[.*\n", "const SUB=" + K.js(SUB) + ";\n", s)
    open(p, 'w').write(s)
    pk, pr = K.ayir(prev)
    sy = K.soz
    metin = [f"Merhaba, ben Matlemur! Geçen bölümün cevabı: kök {sy(prev)}, {sy(pk)} kök {sy(pr)}!",
             f"Bugün tuzak avı! Kök {sy(n)}. {K.cap(sy(n))} kare çiz!",
             f"Hızlı avcı {K.lik(sy(kucuk))} blokları yakaladı: {sy(rk)} blok!",
             f"{K.cap(sy(kk))} dışarı çıktı: {sy(kk)} kök {sy(rk)}. Dikkat! Bu yarım av!",
             f"{K.cap(sy(rk))}nin içinde hâlâ {sy(kucuk)} var! En büyük blok {sy(k*k)}, {sy(r)} blok!",
             f"Kenarı {sy(k)}! Yani kök {sy(n)}, eşittir, {sy(k)} kök {sy(r)}!",
             f"Sıra sende! Kök {sy(ss_n)}, {sy(int(ss_yanlis.split('√')[0]))} kök {sy(int(ss_yanlis.split('√')[1]))} mi? Cevabı yorumlara yaz!",
             "Yarın yine buluşalım!"]
    open(d + '/ses/metin.txt', 'w').write('\n'.join(metin) + '\n')
    post = json.load(open(d + '/post.json'))
    post['baslik'] = f"Mathlemur Kök Avcısı - Bölüm {no}: Tuzak! √{n}"
    post['caption'] = (f"Kök avı, Bölüm {no}: TUZAK 🦝⚠️\n√{n} = {kk}√{rk} ❌ yarım av!\n√{n} = {k}√{r} ✅ en büyük tam kareyi yakala\n\n"
                       f"Sıra sende: √{ss_n} = {ss_yanlis} mi? Cevabını yoruma yaz, bir sonraki bölümde birlikte kontrol edelim!\n\n"
                       "Kaydet, LGS'de lazım olur 📌\n\nHer gün matematik için takip et 👆")
    json.dump(post, open(d + '/post.json', 'w'), ensure_ascii=False, indent=1)
    return slug, metin

if __name__ == '__main__':
    slug, metin = tuzak(7, 48, 4, 242, 72, '36√2')
    print(slug); print('\n'.join(metin))
