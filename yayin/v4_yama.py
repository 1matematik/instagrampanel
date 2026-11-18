#!/usr/bin/env python3
"""Tasarım v4 yaması: canlı Mathlemur (gülüş, tavşan dişi, küçük dil, göz kırpma, yanak), sağa-sola zıplama, ekran kenarına tutunma,
parlayan MATHLEMUR başlığı, cam (glass) KAYDET/TAKİP ET butonu, altta www.sariakademi.com. Kullanım: v4_yama.py sahne.html..."""
import sys
def yama(s):
    if 'V4YAMA' in s: return s
    r=[
    # başlık: MATHLEMUR yukarı + aynı ışıltı
    ("const tag=T('MATHLEMUR',540,300,56,GOLD,{'letter-spacing':8});",
     "const tag=T('MATHLEMUR',540,268,62,GOLD,{'letter-spacing':12,filter:'url(#glow)'});"),
    ("setT(tag,p0,1,540,300);","setT(tag,p0,.85+.15*back(p0),540,250);"),
    ("const bol=mk('text',{x:540,y:200,","const bol=mk('text',{x:540,y:168,"),
    # alt yazı: web sitesi
    ("const nm=T('MATHLEMUR',540,1790,40,GOLD,{'letter-spacing':12,opacity:.95});",
     "const nm=TS([['www.',WH],['sariakademi',GOLD],['.com',WH]],540,1792,40,{'letter-spacing':3,opacity:.95});"),
    # cam buton
    ("const cta=el('g',{});el('rect',{x:130,y:1095,width:820,height:100,rx:50,fill:GOLD},cta); cta.appendChild(T('KAYDET • TAKİP ET',540,1160,44,INK,{}));",
     r"""const cta=el('g',{}); document.querySelector('defs').insertAdjacentHTML('beforeend','<linearGradient id=gl x1=0 y1=0 x2=0 y2=1><stop offset=0 stop-color="#fff" stop-opacity=.42 /><stop offset=.5 stop-color="#fff" stop-opacity=.14 /><stop offset=1 stop-color="#9fd4ff" stop-opacity=.22 /></linearGradient><clipPath id=glc><rect x=130 y=1088 width=820 height=114 rx=57 /></clipPath><filter id=gsh x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation=14 /></filter>');
el('rect',{x:150,y:1110,width:780,height:104,rx:52,fill:'#000',opacity:.45,filter:'url(#gsh)'},cta);
el('rect',{x:130,y:1088,width:820,height:114,rx:57,fill:'url(#gl)',stroke:'#ffffff','stroke-opacity':.75,'stroke-width':2.5},cta);
el('rect',{x:160,y:1094,width:760,height:40,rx:20,fill:'#fff',opacity:.18},cta);
const shG=el('g',{'clip-path':'url(#glc)'},cta), shine=el('rect',{x:0,y:1060,width:90,height:180,fill:'#fff',opacity:.5,transform:'skewX(-20)'},shG);
el('path',{d:'M206,1118 h30 v46 l-15,-11 l-15,11z',fill:GOLD},cta);
el('circle',{cx:860,cy:1145,r:22,fill:'none',stroke:GOLD,'stroke-width':5},cta); el('path',{d:'M860,1133 v24 M848,1145 h24',stroke:GOLD,'stroke-width':5,'stroke-linecap':'round'},cta);
TS([['KAYDET',WH],['  •  ',GOLD],['TAKİP ET',WH]],540,1162,48,{filter:'url(#glow)'}).remove(); cta.appendChild(TS([['KAYDET',WH],['  •  ',GOLD],['TAKİP ET',WH]],540,1162,48,{}));
const SPK=[[150,1080],[930,1094],[300,1215],[790,1210],[540,1072]].map(([x,y])=>el('path',{d:`M${x},${y-16} L${x+4},${y-4} L${x+16},${y} L${x+4},${y+4} L${x},${y+16} L${x-4},${y+4} L${x-16},${y} L${x-4},${y-4}Z`,fill:'#fff'},cta));"""),
    # yüz parçaları: yanak, açık ağız (diş+dil), dil çıkarma, kırpılan göz
    ("const smile=el('path',{d:'M-30,-66 Q0,-46 30,-66',fill:'none',stroke:'#22252b','stroke-width':5,'stroke-linecap':'round'},head);",
     r"""const smile=el('path',{d:'M-30,-66 Q0,-46 30,-66',fill:'none',stroke:'#22252b','stroke-width':5,'stroke-linecap':'round'},head);
const chL=el('ellipse',{cx:-84,cy:-84,rx:20,ry:13,fill:'#ff8fa8',opacity:.5},head), chR=el('ellipse',{cx:84,cy:-84,rx:20,ry:13,fill:'#ff8fa8',opacity:.5},head);
const mo=el('g',{},head); el('path',{d:'M-30,0 Q0,7 30,0 Q25,34 0,36 Q-25,34 -30,0Z',fill:'#e9788f'},mo); el('path',{d:'M-22,10 Q0,14 22,10 Q18,30 0,31 Q-18,30 -22,10Z',fill:'#d4566f'},mo);
el('ellipse',{cx:0,cy:27,rx:11,ry:6,fill:'#e8324c'},mo);
const teeth=el('g',{transform:'translate(0,-61) scale(.5) translate(0,61)'},head); el('path',{d:'M-11,-61 h10 v12 q0,5 -5,5 q-5,0 -5,-5z',fill:'#fff',stroke:'#d8dbe2','stroke-width':1.5},teeth); el('path',{d:'M1,-61 h10 v12 q0,5 -5,5 q-5,0 -5,-5z',fill:'#fff',stroke:'#d8dbe2','stroke-width':1.5},teeth);
const tng=el('g',{},head); el('path',{d:'M2,-52 Q0,-36 9,-35 Q18,-36 16,-52Z',fill:'#ef3b55'},tng); el('line',{x1:9,y1:-50,x2:9,y2:-40,stroke:'#c42640','stroke-width':1.5},tng);
const wink=el('path',{d:'M18,-128 Q46,-112 74,-128',fill:'none',stroke:'#14171c','stroke-width':7,'stroke-linecap':'round'},head);"""),
    ]
    for a,b in r:
        assert a in s, a[:60]
        s=s.replace(a,b)
    # hareket: extra() içindeki eski zıplamayı değiştir
    old_start=s.index(" // lemur: sevinç zıplaması + kuyruk"); old_end=s.index("}\nwindow.seek=t=>{")
    s=s[:old_start]+r""" // V4YAMA lemur canlılık
 const app2=eo(ramp(t,.1,.9)), bob2=7*Math.sin(t*3.1);
 const HOP=[[3.0,0,70],[6.4,70,-70],[9.3,-70,0],[13.0,0,70],[16.6,70,0],[20.8,0,-70],[25.3,-70,0]];
 let dx=0,hj=0; for(const [a,f,g] of HOP){ if(t>=a+.45) dx=g; else if(t>=a){const k=(t-a)/.45; dx=f+(g-f)*eio(k); hj=Math.sin(Math.PI*k)*45;} }
 const jmp=[12.0,26.9].reduce((m,k)=>{const d=t-k;return d>0&&d<.7?Math.max(m,Math.sin(Math.PI*d/.7)*80):m},0);
 // belgesel tadında: sağ ve sol ekran kenarına tutunma
 const cl=(a,b)=>eio(ramp(t,a,a+.5))*(1-eio(ramp(t,b-.5,b)));
 const cR=cl(19.4,20.7), cL=cl(25.3,26.75), cc=Math.max(cR,cL), side=cR>cL?1:-1;
 const lmx=540+dx+(side*420-dx)*cc, lmy=1440+bob2+260*(1-app2)-hj-jmp-cc*(230+12*Math.sin(t*4)), crt=-side*14*cc;
 M.setAttribute('transform',`translate(${lmx},${lmy}) rotate(${crt} 0 0) scale(.95)`);
 if(cc>0.01){ if(side>0){armR.setAttribute('transform',`rotate(${-110*cc} 95 -20)`);armL.setAttribute('transform',`rotate(${-150*cc} -95 -20)`);}
  else{armL.setAttribute('transform',`rotate(${110*cc} -95 -20)`);armR.setAttribute('transform',`rotate(${150*cc} 95 -20)`);}
  head.setAttribute('transform',`rotate(${-side*10*cc} 0 -60)`);}
 const tw=14*Math.sin(t*2.4)+6*Math.sin(t*5.3); tailB.setAttribute('transform',`rotate(${tw} 70 120)`); tailW.setAttribute('transform',`rotate(${tw} 70 120)`);
 // yüz: konuşurken diş+dil görünen açık ağız, arada göz kırpma ve dil çıkarma
 const tk=(t>0.5&&t<28)?(.5+.5*Math.sin(t*11)):0, wk=[[2.2,2.9],[12.3,13.0],[27.4,28.2]].some(([a,b])=>t>=a&&t<b);
 mouth.setAttribute('opacity',0); smile.setAttribute('opacity',(tk<.25||wk)?1:0);
 mo.setAttribute('opacity',(tk>=.25&&!wk)?1:0); mo.setAttribute('transform',`translate(0,-66) scale(1,${.35+.65*tk})`);
 tng.setAttribute('opacity',wk?1:0); tng.setAttribute('transform',`translate(0,${wk?0:-12})`);
 wink.setAttribute('opacity',wk?1:0); if(wk){eR.setAttribute('ry',2);[iR,pR,hR].forEach(e=>e.setAttribute('opacity',0));}
 const big=Math.max(...[6.5,20.8].map(k=>t>k&&t<k+1.2?Math.sin(Math.PI*(t-k)/1.2):0)); [iL,iR].forEach(e=>e.setAttribute('r',19+5*big)); [pL,pR].forEach(e=>e.setAttribute('r',10+4*big));
 [chL,chR].forEach(e=>e.setAttribute('opacity',.45+.25*Math.max(big,wk?1:0)));
 // cam buton: salto ile giriş, parıltı, yıldızlar
 const cq=ramp(t,26.8,27.6), fl=Math.cos(Math.PI*(1-eio(cq))), pl=1+.025*Math.sin((t-26.8)*7)*cq;
 cta.setAttribute('opacity',cq>0?1:0); cta.setAttribute('transform',`translate(540,1145) scale(${pl},${fl*pl}) translate(-540,-1145)`);
 shine.setAttribute('x',-200+(((t-27.2)*700)%1500+1500)%1500);
 SPK.forEach((e,i)=>{const p=.5+.5*Math.sin(t*5+i*1.7); e.setAttribute('opacity',cq*p); const [x,y]=[[150,1080],[930,1094],[300,1215],[790,1210],[540,1072]][i]; e.setAttribute('transform',`translate(${x},${y}) scale(${.4+.6*p}) rotate(${t*60}) translate(${-x},${-y})`)});
"""+s[old_end:]
    return s
if __name__=='__main__':
    for p in sys.argv[1:]:
        y=yama(open(p).read()); open(p,'w').write(y); print('yamandı',p)
