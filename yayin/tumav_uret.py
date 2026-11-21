#!/usr/bin/env python3
"""Mathlemur "TÜM AV" mini serisi üretici.
Fikir (kullanıcı): √n = k√r ise k'nın her pozitif böleni d için √n = d·√(n/d²) yazılır.
Yazılış sayısı = en büyük katsayının (k) pozitif bölen sayısı. En büyük katsayı = tam av.
Şimdilik 4 yazılışlı sayılar (k'nın 4 böleni var) için kurgu: 1 → ham ızgara, sonraki 3 bölen → blok ızgaraları.
Kullanım: python3 yayin/tumav_uret.py  -> icerik/tum-av-01/"""
import os, sys, re, json, shutil
sys.path.insert(0, os.path.dirname(__file__))
import kok_uret as K

def ek_lik(x): w = K.soz(x); return K.lik(w)[len(w):]
def ek_in(x):
    w = K.soz(x); v = [c for c in w if c in 'aeıioöuü'][-1]; h = {'a':'ı','ı':'ı','e':'i','i':'i','o':'u','u':'u','ö':'ü','ü':'ü'}[v]
    return ('n' if w[-1] in 'aeıioöuü' else '') + h + 'n'
def bolenler(k): return [d for d in range(1, k + 1) if k % d == 0]

def izgara_yamasi(s, gapy=24):
    s = s.replace("const CS=Math.min(110,Math.floor(880/(r*k)),Math.floor(400/k)), bw=k*CS, W=r*bw, H=k*CS, X0=(1080-W)/2, Y0=500+(420-H)/2;",
      f"let cols=1, bestCS=0; for(let c=1;c<=r;c++){{const rw=Math.ceil(r/c), gy=rw>1?{gapy}:0, cs=Math.min(110,Math.floor(880/(c*k)),Math.floor((400-gy*(rw-1))/(rw*k))); if(cs>bestCS){{bestCS=cs; cols=c}}}} const rows=Math.ceil(r/cols), GAPY=rows>1?{gapy}:0, CS=Math.max(8,bestCS), bw=k*CS, W=cols*bw, H=k*CS, X0=(1080-W)/2, Y0=500+(420-rows*H-GAPY*(rows-1))/2;", 1)
    s = s.replace("for(let b=0;b<r;b++){const g=el('g',{},root), col=b%2?CY:GOLD, x0=X0+b*bw;",
      "for(let b=0;b<r;b++){const g=el('g',{},root), col=b%2?CY:GOLD, x0=X0+(b%cols)*bw, Yb=Y0+Math.floor(b/cols)*(H+GAPY);", 1)
    a = s.index("for(let b=0;b<r;b++){"); e = s.index("blocks.push(", a); e = s.index("\n", e)
    s = s[:a] + s[a:e].replace("Y0", "Yb").replace("Yb=Yb+", "Yb=Y0+") + s[e:]
    assert 'cols=' in s, 'ızgara yaması tutmadı'
    return s

def tumav(seri_no, n, ss_n, ss_ipucu):
    k, r = K.ayir(n); D = bolenler(k)
    assert len(D) == 4, f'bu kurgu 4 yazılış ister, √{n} için {len(D)}'
    F = [(d, n // (d * d)) for d in D]               # (katsayı, kök içi)
    slug = K.bolum(90, 50, 50, ss_n, None)           # v4 şablonu (geçici klasör; E1/E2 kullanılmaz)
    tmp = f'{K.R}/icerik/{slug}'; yeni = f'tum-av-{seri_no:02d}'; d = f'{K.R}/icerik/{yeni}'
    if os.path.exists(d): shutil.rmtree(d)
    os.rename(tmp, d)
    p = d + '/sahne.html'; s = open(p).read()
    s = s.replace("'BÖLÜM 90'", f"'TÜM AV {seri_no}'", 1)
    s = izgara_yamasi(s)
    # ana örnek animasyonlarını kapat (kendi zaman çizelgemiz var)
    for pat in [r" animEx\(E1,t,.*\n", r" animEx\(E2,t,.*\n", r" animF\(F1,t,.*animF\(F2,t,.*\n",
                r" setT\(six,.*\n", r" setT\(five,.*\n"]:
        s, c = re.subn(pat, "", s, count=1); assert c == 1, pat
    _, (d2, r2), (d3, r3), (d4, r4) = F
    kod = f"""// ---------- TÜM AV
const G0=el('g',{{opacity:0}}), C0=[];
{{let nc=12, cs=0; for(let c=8;c<=70;c++){{const rw=Math.ceil({n}/c), q=Math.min(56,Math.floor(880/c),Math.floor(420/rw)); if(q>cs){{cs=q; nc=c}}}} const X=(1080-nc*cs)/2, Y=520, gp=cs>=30?3:1.5; for(let i=0;i<{n};i++){{const x=X+(i%nc)*cs, y=Y+Math.floor(i/nc)*cs;
 C0.push(el('rect',{{x:x+gp,y:y+gp,width:cs-2*gp,height:cs-2*gp,rx:Math.max(2,cs/7),fill:mix(CELL,CY,.75),stroke:'#d8f8ff','stroke-width':2}},G0))}}}}
const X1=makeEx({d2},{r2},'{d2*d2}'), X2=makeEx({d3},{r3},'{d3*d3}'), X3=makeEx({d4},{r4},'{d4*d4}');
[X1,X2,X3].forEach(E=>E.bl.setAttribute('display','none'));
X1.cnt.textContent='{n} kare'; X2.cnt.textContent='{n} kare'; X3.cnt.textContent='{n} kare';
const soru=el('g',{{opacity:0}}); T('√{n} = a√b',540,720,150,WH,{{filter:'url(#glow)'}},soru); T('KAÇ YOL?',540,880,96,GOLD,{{filter:'url(#glow)'}},soru);
const FM=[TS([['1 · 1 = 1  →  ',WH],['√{n}',CY]],540,985,62,{{opacity:0}}),
 TS([['√{n} = √(',WH],['{d2*d2}',GOLD],[' · ',WH],['{r2}',CY],[') = ',WH],['{d2}',GOLD],['√{r2}',CY]],540,985,62,{{opacity:0}}),
 TS([['√{n} = √(',WH],['{d3*d3}',GOLD],[' · ',WH],['{r3}',CY],[') = ',WH],['{d3}',GOLD],['√{r3}',CY]],540,985,62,{{opacity:0}}),
 TS([['√{n} = √(',WH],['{d4*d4}',GOLD],[' · ',WH],['{r4}',CY],[') = ',WH],['{d4}',GOLD],['√{r4}',CY]],540,985,62,{{opacity:0}})];
const KART=[], KTXT=[['√{n}'],['{d2}√{r2}'],['{d3}√{r3}'],['{d4}√{r4}']];
KTXT.forEach(([tx],i)=>{{const cx=180+i*240, g=el('g',{{opacity:.0}});
 const bx=el('rect',{{x:cx-108,y:1052,width:216,height:96,rx:24,fill:'rgba(255,255,255,.08)',stroke:'#9fd4ff','stroke-width':3}},g);
 const tt=T(tx,cx,1118,52,WH,{{}},g); KART.push({{g,bx,tt,cx}})}});
const tamEt=T('TAM AV ✓',900,1032,34,GOLD,{{opacity:0,filter:'url(#glow)'}});
const kural=el('g',{{opacity:0}});
el('rect',{{x:110,y:560,width:860,height:330,rx:36,fill:'rgba(246,201,69,.10)',stroke:GOLD,'stroke-width':6}},kural);
T('KURAL',540,630,44,GOLD,{{'letter-spacing':6}},kural);
kural.appendChild(TS([['En büyük katsayı: ',WH],['{k}',GOLD]],540,705,54,{{}}));
kural.appendChild(TS([['{k}\\'{ek_in(k)} bölenleri: ',WH],['{" · ".join(map(str, D))}',CY]],540,780,{54 if len(str(k))<2 else 46},{{}}));
kural.appendChild(TS([['→ ',WH],['{len(D)} farklı yazılış!',GOLD]],540,860,62,{{filter:'url(#glow)'}}));
function tumAv(t){{
 soru.setAttribute('opacity',ramp(t,.9,1.5)*(1-ramp(t,2.9,3.3)));
 G0.setAttribute('opacity',ramp(t,3.3,3.9)*(1-ramp(t,6.1,6.5)));
 C0.forEach((c,i)=>{{const a=ramp(t,3.3+i*.012,3.7+i*.012); c.setAttribute('opacity',a)}});
 animEx(X1,t,{{g:6.4,tint:7.2,lab:7.7,fly:999,vis0:6.3,vis1:9.0}});
 animEx(X2,t,{{g:9.3,tint:10.1,lab:10.6,fly:999,vis0:9.2,vis1:12.5}});
 animEx(X3,t,{{g:12.8,tint:13.7,lab:14.3,fly:999,vis0:12.7,vis1:16.5}});
 const W=[[4.3,6.3],[7.6,9.1],[10.5,12.6],[14.2,16.6]];
 FM.forEach((f,i)=>{{const a=ramp(t,W[i][0],W[i][0]+.5)*(1-ramp(t,W[i][1]-.2,W[i][1]+.2)); setT(f,a,.8+.2*back(ramp(t,W[i][0],W[i][0]+.5)),540,985)}});
 const on=[5.3,8.4,11.5,15.1], off=1-ramp(t,20.5,21.0);
 KART.forEach((K,i)=>{{const a=ramp(t,on[i],on[i]+.5), pul=t>16.9&&t<20.5?1+.08*Math.max(0,Math.sin(Math.PI*clamp((t-17.6-i*.55)/.5))):1;
  K.g.setAttribute('opacity',(t>3.3?(.35+.65*a):0)*off);
  K.g.setAttribute('transform',`translate(${{K.cx}},1100) scale(${{(.85+.15*back(a))*pul}}) translate(${{-K.cx}},-1100)`);
  K.bx.setAttribute('stroke',a>.5?(i==3?GOLD:CY):'#9fd4ff'); K.bx.setAttribute('fill',a>.5?(i==3?'rgba(246,201,69,.22)':'rgba(110,231,255,.16)'):'rgba(255,255,255,.08)');
  K.tt.setAttribute('fill',a>.5?(i==3?GOLD:WH):'#6d86a8');}});
 setT(tamEt,ramp(t,15.4,15.9)*off,.8+.2*back(ramp(t,15.4,15.9)),900,1032);
 const kq=ramp(t,16.9,17.5)*(1-ramp(t,20.4,20.8)); setT(kural,kq,.85+.15*back(ramp(t,16.9,17.5)),540,725);
}}
// ---------- sıra sende + final"""
    s = s.replace("// ---------- sıra sende + final", kod, 1)
    s = s.replace(" extra(t);\n};", " tumAv(t);\n extra(t);\n};", 1)
    s = s.replace(f"T('√{ss_n} = ?',540,820,200", f"T('√{ss_n} = a√b ?',540,820,140", 1)
    s = re.sub(r"const ipu=TS\(.*\n", f"const ipu=TS([['İpucu: önce tam avı bul, katsayının bölenlerini say',WH]],540,1070,40,{{opacity:0}});\n", s)
    SUB = [[0, 3.0, f'Tüm av: √{n} kaç yolla yazılır?'],
           [3.2, 6.3, f'1 ile: hiç blok yok → √{n}'],
           [6.5, 9.1, f'{d2} ile: {d2*d2}\'{ek_lik(d2*d2)} {r2} blok → {d2}√{r2}'],
           [9.3, 12.6, f'{d3} ile: {d3*d3}\'{ek_lik(d3*d3)} {r3} blok → {d3}√{r3}'],
           [12.8, 16.6, f'{d4} ile: {d4*d4}\'{ek_lik(d4*d4)} {r4} blok → {d4}√{r4} TAM AV'],
           [16.8, 20.6, f'{k}\'{ek_in(k)} bölenleri: {", ".join(map(str, D))} → {len(D)} yol!'],
           [20.8, 25.3, f'Sıra sende: √{ss_n} kaç yolla yazılır?'],
           [25.5, 28.6, 'Yarın yine buluşalım!']]
    s = re.sub(r"const SUB=\[.*\n", "const SUB=" + K.js(SUB) + ";\n", s)
    open(p, 'w').write(s)
    sy = K.soz
    metin = [f"Merhaba, ben Matlemur! Bugün tüm av: kök {sy(n)} kaç yolla yazılır?",
             f"Bir ile başla: hiç blok yok, kök {sy(n)}!",
             f"{K.cap(sy(d2))} ile: {K.lik(sy(d2*d2))} {sy(r2)} blok. {K.cap(sy(d2))} kök {sy(r2)}!",
             f"{K.cap(sy(d3))} ile: {K.lik(sy(d3*d3))} {sy(r3)} blok. {K.cap(sy(d3))} kök {sy(r3)}!",
             f"{K.cap(sy(d4))} ile: {K.lik(sy(d4*d4))} {sy(r4)} blok. {K.cap(sy(d4))} kök {sy(r4)}, tam av!",
             f"{K.cap(sy(k))}{ek_in(k)} bölenleri: {', '.join(sy(x) for x in D)}. Tam {sy(len(D))} yol!",
             f"Sıra sende! Kök {sy(ss_n)} kaç yolla yazılır? Cevabı yorumlara yaz!",
             "Yarın yine buluşalım!"]
    open(d + '/ses/metin.txt', 'w').write('\n'.join(metin) + '\n')
    j = json.load(open(d + '/ses.json')); j['muzik_dosya'] = 'kutuphane/muzik/' + K.MUZ[(seri_no + 6) % len(K.MUZ)]
    json.dump(j, open(d + '/ses.json', 'w'), ensure_ascii=False)
    yaz = ' = '.join([f'√{n}'] + [f'{a}√{b}' for a, b in F[1:]])
    post = json.load(open(d + '/post.json'))
    post['baslik'] = f"Mathlemur Tüm Av {seri_no}: √{n} kaç yolla yazılır?"
    post['caption'] = (f"Tüm av {seri_no} 🦝 √{n} kaç farklı a√b şeklinde yazılır?\n{yaz}\n"
                       f"Kural: en büyük katsayı {k} → {k}'{ek_in(k)} bölenleri {', '.join(map(str, D))} → {len(D)} yazılış\n\n"
                       f"Sıra sende: √{ss_n} kaç farklı şekilde yazılır? Cevabını yoruma yaz, bir sonraki bölümde birlikte kontrol edelim!\n\n"
                       "Kaydet, LGS'de lazım olur 📌\n\nHer gün matematik için takip et 👆")
    json.dump(post, open(d + '/post.json', 'w'), ensure_ascii=False, indent=1)
    return yeni, metin

if __name__ == '__main__':
    # Kullanım: python3 yayin/tumav_uret.py 2:108:96 3:128:150 ...   (seri_no:n:sıra_sende_n)
    # tum-av-01 yayınlandığı için varsayılan çalıştırma onu EZMEZ; açıkça 1:... verilmedikçe dokunulmaz.
    for a in sys.argv[1:]:
        no, n, ss = map(int, a.split(':'))
        slug, metin = tumav(no, n, ss, None)
        print(slug); print('\n'.join(metin)); print()
