#!/usr/bin/env python3
"""Mathlemur Kök Avcısı bölüm üretici. v3 şablonunu parametreler.
Kullanım: python3 kok.py  (BOLUMLER listesindekileri icerik/kok-avcisi-bNN/ altına yazar)"""
import json, os, re, sys, math
R='/home/claude/instagrampanel'; TPL=open(f'{R}/icerik/kok-avcisi-v3/sahne.html').read()
TPLJ=json.load(open(f'{R}/icerik/kok-avcisi-v3/ses.json'))
B=['','bir','iki','üç','dört','beş','altı','yedi','sekiz','dokuz']; O=['','on','yirmi','otuz','kırk','elli','altmış','yetmiş','seksen','doksan']
def soz(n):
    if n==0: return 'sıfır'
    p=[]
    if n>=1000: p.append(('' if n//1000==1 else soz(n//1000)+' ')+'bin'); n%=1000
    if n>=100: p.append(('' if n//100==1 else B[n//100]+' ')+'yüz'); n%=100
    if n>=10: p.append(O[n//10]); n%=10
    if n: p.append(B[n])
    return ' '.join(p)
def lik(w):
    v=[c for c in w if c in 'aeıioöuü'][-1]; return w+{'a':'lık','ı':'lık','e':'lik','i':'lik','o':'luk','u':'luk','ö':'lük','ü':'lük'}[v]
def cap(s): return ('İ' if s[0]=='i' else s[0].upper())+s[1:]
def ayir(n):
    k=max(k for k in range(1,int(math.isqrt(n))+1) if n%(k*k)==0); return k, n//(k*k)
MUZ=sorted(f for f in os.listdir(f'{R}/kutuphane/muzik') if f.endswith('.mp3'))
def js(o): return json.dumps(o,ensure_ascii=False)

GEN=r'''const CS0=70;
function makeEx(k,r,label){
 const CS=Math.min(110,Math.floor(880/(r*k)),Math.floor(400/k)), bw=k*CS, W=r*bw, H=k*CS, X0=(1080-W)/2, Y0=500+(420-H)/2;
 const root=el('g',{opacity:0}), blocks=[]; const cells=[];
 for(let b=0;b<r;b++){const g=el('g',{},root), col=b%2?CY:GOLD, x0=X0+b*bw;
  for(let i=0;i<k;i++)for(let j=0;j<k;j++){const cx=x0+j*CS+CS/2,cy=Y0+i*CS+CS/2;
   cells.push({rc:el('rect',{x:x0+j*CS+2,y:Y0+i*CS+2,width:CS-4,height:CS-4,rx:Math.max(3,CS/7),fill:CELL,stroke:'#6fa8ff','stroke-width':2,opacity:0},g),cx,cy,b,col,d:(b*k+j+i)*Math.min(.06,1.2/(r*k+k))})}
  const per=4*bw, out=el('rect',{x:x0,y:Y0,width:bw,height:H,rx:12,fill:'none',stroke:col,'stroke-width':Math.max(5,CS/8),'stroke-dasharray':per,'stroke-dashoffset':per},g);
  const fs=Math.min(130,bw*.42), lb=T(label,x0+bw/2,Y0+H/2+fs*.36,fs,INK,{opacity:0},g);
  blocks.push({g,col,out,per,lb,fs,c:[x0+bw/2,Y0+H/2]})}
 const bl=el('g',{opacity:0},root);
 blocks.forEach(b=>{el('line',{x1:b.c[0]-bw/2+6,y1:Y0+H+38,x2:b.c[0]+bw/2-6,y2:Y0+H+38,stroke:b.col,'stroke-width':6,'stroke-linecap':'round'},bl);T(String(k),b.c[0],Y0+H+92,Math.min(56,bw*.5),b.col,{},bl)});
 const cnt=T('',540,478,40,CY,{opacity:0},root);
 return {root,blocks,cells,bl,cnt,r};
}
function animEx(E,t,o){
 E.root.setAttribute('opacity',ramp(t,o.vis0,o.vis0+.4)*(1-ramp(t,o.vis1,o.vis1+.5)));
 const td=1.6/E.r;
 E.cells.forEach(c=>{const k=ramp(t,o.g+c.d,o.g+.45+c.d),s=back(k);c.rc.setAttribute('opacity',k);
  c.rc.setAttribute('transform',`translate(${c.cx},${c.cy}) scale(${.2+.8*s}) translate(${-c.cx},${-c.cy})`);
  const tk=ramp(t,o.tint+c.b*td,o.tint+(c.b+1)*td);
  c.rc.setAttribute('fill',mix(CELL,c.col,tk*.9));c.rc.setAttribute('stroke',mix('#6fa8ff',c.col==GOLD?'#fff1b0':'#d8f8ff',tk))});
 E.blocks.forEach((b,i)=>{b.out.setAttribute('stroke-dashoffset',b.per*(1-eo(ramp(t,o.tint+i*td,o.tint+(i+1)*td))));
  const a=o.lab+i*.8/E.r; setT(b.lb,ramp(t,a,a+.6),.8+.2*back(ramp(t,a,a+.6)),b.c[0],b.c[1]+b.fs*.36)});
 setT(E.cnt,ramp(t,o.g+.8,o.g+1.4)*(1-ramp(t,o.tint,o.tint+.4)),1,540,478);
 E.bl.setAttribute('opacity',ramp(t,o.lab+.6,o.lab+1.2)*(1-ramp(t,o.fly-.3,o.fly)));
 const tx=540,ty=1215;
 E.blocks.forEach((b,i)=>{const a=o.fly+i*1.0/E.r,p=eio(ramp(t,a,a+.7));
  b.g.setAttribute('transform',`translate(${b.c[0]+(tx-b.c[0])*p},${b.c[1]+(ty-b.c[1])*p}) scale(${1-.93*p}) translate(${-b.c[0]},${-b.c[1]})`);b.g.setAttribute('opacity',1-ramp(p,.88,1))});
}
'''
def bolum(no,ex1,ex2,ss,prev):
    (n1,n2)=ex1,ex2; k1,r1=ayir(n1); k2,r2=ayir(n2); ks,rs=ayir(ss)
    s=TPL
    a=s.index('const CS=70;'); b=s.index('// ---------- formüller')
    s=s[:a]+GEN+f"const E1=makeEx({k1},{r1},'{k1*k1}'), E2=makeEx({k2},{r2},'{k2*k2}');\nE1.cnt.textContent='{n1} kare'; E2.cnt.textContent='{n2} kare';\n"+s[b:]
    # makeEx eski tanımı başlıktan sonra kaldı mı? başlık satırları a..b arasındaydı -> geri ekle
    s=s.replace(GEN,"// ---------- başlık\nconst tag=T('MATHLEMUR',540,300,56,GOLD,{'letter-spacing':8});\nconst tit=T('KÖK AVCISI',540,420,124,WH,{filter:'url(#glow)'});\n"+GEN,1)
    s=re.sub(r"const F1=fset\(.*\n",f"const F1=fset(0,[['√{n1} = √(',WH],['{k1*k1}',GOLD],[' · ',WH],['{r1}',CY],[')',WH]],[['√{n1} = ',WH],['{k1}',GOLD],['√{r1}',CY]],'√{n1}');\n",s)
    s=re.sub(r"const F2=fset\(.*\n",f"const F2=fset(0,[['√{n2} = √(',WH],['{k2*k2}',GOLD],[' · ',WH],['{r2}',CY],[')',WH]],[['√{n2} = ',WH],['{k2}',GOLD],['√{r2}',CY]],'√{n2}');\n",s)
    s=s.replace("T('√98 = ?'",f"T('√{ss} = ?'").replace("[['İpucu: 98 = ',WH],['49',GOLD],[' · ',WH],['2',CY]]",f"[['İpucu: {ss} = ',WH],['{ks*ks}',GOLD],[' · ',WH],['{rs}',CY]]")
    s=s.replace("const six=T('6',",f"const six=T('{k1}',").replace("five=T('5',",f"five=T('{k2}',")
    s=re.sub(r"'BÖLÜM 1( / 16)?'",f"'BÖLÜM {no}'",s,count=1)
    if prev:
        pk,pr=ayir(prev)
        s=s.replace("// ---------- altyazı + CTA",f"const dun=TS([['Geçen cevap: ',CY],['√{prev} = ',WH],['{pk}',GOLD],['√{pr}',CY]],540,620,56,{{opacity:0}});\n// ---------- altyazı + CTA")
        s=s.replace("window.seek=t=>{\n","window.seek=t=>{\n setT(dun,ramp(t,.8,1.4)*(1-ramp(t,3.0,3.4)),1,540,620);\n",1)
    l1=f'Geçen bölümün cevabı: √{prev} = {ayir(prev)[0]}√{ayir(prev)[1]}' if prev else 'Merhaba, ben Matlemur!'
    SUB=[[0,3.0,l1],[3.2,6.3,f'İlk av: √{n1} → {n1} kare çiz'],[6.5,9.1,f'En büyük tam kare bloğu yakala: {k1*k1}'],[9.3,12.6,f'Tam kareyi yakala, dışarı at: {k1}!'],[12.8,16.6,f'İkinci av: √{n2} → {k2*k2} · {r2}'],[16.8,20.6,f'Kenarı {k2} → √{n2} = {k2}√{r2}'],[20.8,25.3,f'Sıra sende: √{ss} = ?'],[25.5,28.6,'Yarın yine buluşalım!']]
    s=re.sub(r"const SUB=\[.*\n","const SUB="+js(SUB)+";\n",s)
    assert 'makeEx(12,6' not in s and "'√72'" not in s and "'√98 = ?'" not in s, 'eski değer kaldı'
    m1=(f"Merhaba, ben Matlemur! Geçen bölümün cevabı: kök {soz(prev)}, {soz(ayir(prev)[0])} kök {soz(ayir(prev)[1])}!" if prev else "Merhaba, ben Matlemur! Bugün birlikte kök avlıyoruz!")
    metin=[m1,
     f"İlk av: kök {soz(n1)}. {cap(soz(n1))} kare çiz!",
     f"En büyük tam kare bloğu yakala: {soz(k1*k1)}!",
     f"Tam kareyi yakala, dışarı at: {soz(k1)}! {cap(soz(r1))} blok var, {soz(r1)} içeride kalır!",
     f"İkinci av: kök {soz(n2)}! {cap(soz(n2))} kare, {lik(soz(k2*k2))} {soz(r2)} blok!",
     f"Kenarı {soz(k2)}! Yani kök {soz(n2)}, eşittir, {soz(k2)} kök {soz(r2)}!",
     f"Sıra sende! Kök {soz(ss)} kaç eder? Cevabı yorumlara yaz!",
     "Yarın yine buluşalım!"]
    slug=f'kok-avcisi-b{no:02d}'; d=f'{R}/icerik/{slug}'; os.makedirs(d+'/ses',exist_ok=True)
    import importlib.util as _u; _sp=_u.spec_from_file_location('v4',os.path.join(R,'yayin','v4_yama.py')); _m=_u.module_from_spec(_sp); _sp.loader.exec_module(_m); s=_m.yama(s)  # tasarım v4
    open(d+'/sahne.html','w').write(s); open(d+'/ses/metin.txt','w').write('\n'.join(metin)+'\n')
    j=dict(TPLJ); j['muzik_dosya']='kutuphane/muzik/'+MUZ[no%len(MUZ)]; j['muzik_baslangic']=6
    json.dump(j,open(d+'/ses.json','w'),ensure_ascii=False)
    post={"baslik":f"Mathlemur Kök Avcısı - Bölüm {no}: √{n1} ve √{n2}","tur":"özgün","sure":44,"fps":30,
     "caption":f"Kök avı, Bölüm {no} 🦝\n√{n1} = {k1}√{r1}\n√{n2} = {k2}√{r2}\n\nSıra sende: √{ss} kaç eder? Cevabını yoruma yaz, bir sonraki bölümde birlikte kontrol edelim!\n\nKaydet, LGS'de lazım olur 📌\n\nHer gün matematik için takip et 👆",
     "hashtagler":["keşfet", "yapayzeka", "teknoloji", "izleöğren", "mathlemur"],"kaynak":"Özgün Mathlemur karakteri ve kurgu","durum":"taslak","ana_izgara":False,"kayit":[]}
    json.dump(post,open(d+'/post.json','w'),ensure_ascii=False,indent=1)
    return slug
BOLUMLER=[(2,12,18,8,98),(3,20,27,45,8),(4,75,63,28,45),(5,200,300,500,28),(6,128,162,242,500)]
if __name__=='__main__':
    for no,a,b,ss,prev in BOLUMLER: print(bolum(no,a,b,ss,prev), open(f'{R}/icerik/kok-avcisi-b{no:02d}/ses/metin.txt').read())
