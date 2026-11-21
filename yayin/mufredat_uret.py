#!/usr/bin/env python3
"""Mathlemur "MAARİF RADARI" serisi üretici (2028 LGS / yeni 8. sınıf Maarif matematik müfredatı).
9 video: 1 duyuru, 1 ders saati dağılımı, 7 tema (madde madde öğrenme çıktıları).
Kullanım: python3 yayin/mufredat_uret.py            -> hepsi
          python3 yayin/mufredat_uret.py lgs28-03-tema1 ...
Çıktı: icerik/<slug>/{sahne.html, ses.json, ses/metin.txt, post.json}
Not: yayin_zamani YOK; seriyi kullanıcı başlatacak, durum 'taslak' kalır. Bilgiler kullanıcının gönderdiği görsellerden (birebir)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import kok_uret as K

R = K.R
GOLD, CY = '#f6c945', '#6ee7ff'
RENK = {1: '#f6c945', 2: '#6ee7ff', 3: '#b794ff', 4: '#5eead4', 5: '#ff8a8a', 6: '#7cb4ff', 7: '#ff9ed8', 0: '#8fa3c7'}
ETIKET = ['lgs2028', 'maarifmodel', 'matematik', 'lgsmatematik', 'keşfet']

TEMALAR = [
 (1, 'Sayılar ve Nicelikler', 38, [
  ('MAT.8.1.1', 'Farklı bağlamlardaki üslü ifadelere, özelliklerine ve üslü ifadelerle yapılan işlemlere ilişkin çıkarım yapabilme', 'Üslü ifadeler, özellikleri ve işlemler üzerine çıkarım yapabilme.'),
  ('MAT.8.1.2', 'Karşılaştığı problem durumlarında kareköklü ifadeler ile ilgili muhakeme yapabilme', 'Problemlerde kareköklü ifadelerle muhakeme yapabilme.'),
  ('MAT.8.1.3', 'Sayıların rasyonel ya da irrasyonelliğini değerlendirebilme', 'Sayıların rasyonel ya da irrasyonel olduğunu değerlendirebilme.'),
  ('MAT.8.1.4', 'Gerçek sayıları ve aralıklarını sayı doğrusunda yorumlayabilme', 'Gerçek sayıları ve aralıkları sayı doğrusunda yorumlayabilme.')]),
 (2, 'Cebirsel Düşünme ve Değişimler', 42, [
  ('MAT.8.2.1', 'Gerçek yaşam durumları üzerinden dik koordinat sistemini çözümleyebilme', 'Gerçek yaşam durumlarından dik koordinat sistemini çözümleyebilme.'),
  ('MAT.8.2.2', 'Gerçek yaşam durumlarındaki doğrusal ilişkileri doğrusal fonksiyonlarla temsil edebilme', 'Doğrusal ilişkileri doğrusal fonksiyonlarla temsil edebilme.'),
  ('MAT.8.2.3', 'Dik koordinat sisteminde iki doğrusal fonksiyonun birbirine göre durumuna ilişkin çıkarım yapabilme', 'İki doğrusal fonksiyonun birbirine göre durumunu yorumlayabilme.'),
  ('MAT.8.2.4', 'Doğrusal fonksiyonlara ilişkin problemlerin çözümlerini algoritma ifade yöntemlerini kullanarak yapılandırabilme', 'Doğrusal fonksiyon problemlerini algoritma yöntemleriyle yapılandırabilme.')]),
 (3, 'Geometrik Şekiller', 39, [
  ('MAT.8.3.1', 'Matematiksel araç ve teknoloji yardımıyla üçgenin kenarları ve açıları arasındaki ilişkiyi yorumlayabilme', 'Teknoloji yardımıyla üçgenin kenar ve açı ilişkisini yorumlayabilme.'),
  ('MAT.8.3.2', 'Üçgenin kenar uzunlukları arasındaki ilişkiye yönelik çıkarım yapabilme', 'Üçgenin kenar uzunlukları arasındaki ilişkiye yönelik çıkarım yapabilme.'),
  ('MAT.8.3.3', 'Bir üçgene eş üçgen oluşturmak için yeterli olan elemanlara dair çıkarım yapabilme', 'Eş üçgen oluşturmak için yeterli elemanlara dair çıkarım yapabilme.'),
  ('MAT.8.3.4', 'Bir üçgene benzer üçgen oluşturmak için yeterli olan elemanlara dair çıkarım yapabilme', 'Benzer üçgen oluşturmak için yeterli elemanlara dair çıkarım yapabilme.'),
  ('MAT.8.3.5', 'Kenar uzunlukları a² + b² = c² eşitliğini sağlayan üçgenleri oluşturarak dik üçgen olduklarını yorumlayabilme', 'Kenarları a kare artı b kare eşittir c kare olan üçgenlerin dik üçgen olduğunu yorumlayabilme.'),
  ('MAT.8.3.6', 'Üçgende açı-kenar ilişkisi, üçgen eşitsizliği ve Pisagor bağıntısını içeren problemleri çözebilme', 'Açı kenar ilişkisi, üçgen eşitsizliği ve Pisagor problemlerini çözebilme.')]),
 (4, 'Geometrik Nicelikler', 15, [
  ('MAT.8.4.1', 'Dik prizmalar, dikdörtgen dik piramit, dik dairesel silindir ve koninin yüzey açınımlarını çözümleyebilme', 'Dik prizma, piramit, silindir ve koninin yüzey açınımlarını çözümleyebilme.'),
  ('MAT.8.4.2', 'Dik dairesel silindirin yüzey açınımına ilişkin deneyimlerini yüzey alanına yansıtabilme', 'Silindirin yüzey açınımı deneyimini yüzey alanına yansıtabilme.'),
  ('MAT.8.4.3', 'Dairenin alan bağıntısından hareketle silindirin hacim bağıntısına yönelik analojik akıl yürütebilme', 'Daire alanından hareketle silindirin hacmine yönelik analojik akıl yürütebilme.')]),
 (5, 'Dönüşüm', 9, [
  ('MAT.8.5.1', 'Matematiksel araç ve teknoloji yardımıyla öteleme dönüşümünü çözümleyebilme', 'Teknoloji yardımıyla öteleme dönüşümünü çözümleyebilme.'),
  ('MAT.8.5.2', 'Noktaların apsis ve ordinatlarının öteleme ve eksen yansımasındaki değişimine ilişkin çıkarım yapabilme', 'Noktaların apsis ve ordinatlarının öteleme ve yansımadaki değişimini yorumlayabilme.'),
  ('MAT.8.5.3', 'Öteleme ve yansıma dönüşümlerini içeren problemleri çözebilme', 'Öteleme ve yansıma problemlerini çözebilme.')]),
 (6, 'İstatistiksel Araştırma Süreci', 20, [
  ('MAT.8.6.1', 'Kategorik veya nicel (kesikli-sürekli) veri ile çalışabilme ve veriye dayalı karar verebilme', 'Kategorik ya da nicel veriyle çalışıp veriye dayalı karar verebilme.'),
  ('MAT.8.6.2', 'Başkaları tarafından oluşturulan veriye dayalı istatistiksel sonuç veya yorumları tartışabilme', 'Başkalarının oluşturduğu veriye dayalı sonuçları tartışabilme.')]),
 (7, 'Veriden Olasılığa', 9, [
  ('MAT.8.7.1', 'Bir olayın olasılığına ilişkin öznel, deneysel ve teorik yaklaşımlardan uygun olanı seçerek karar verebilme', 'Öznel, deneysel ve teorik yaklaşımlardan uygun olanı seçerek olasılıkta karar verebilme.')]),
]
OKUL_TEMELLI = 8
TOPLAM_SAAT = sum(t[2] for t in TEMALAR) + OKUL_TEMELLI           # 180
TOPLAM_CIKTI = sum(len(t[3]) for t in TEMALAR)                     # 23
assert TOPLAM_SAAT == 180 and TOPLAM_CIKTI == 23 and len(TEMALAR) == 7

ORD_KUCUK = ['', 'birinci', 'ikinci', 'üçüncü', 'dördüncü', 'beşinci', 'altıncı', 'yedinci']
ORD_BUYUK = ['', 'Birinci', 'İkinci', 'Üçüncü', 'Dördüncü', 'Beşinci', 'Altıncı', 'Yedinci']
soz = K.soz

def sure_tahmin(metin):          # sahne zamanı için kaba tahmin; senkron.py gerçek sürelere ölçekler
    return max(2.2, 0.40 * len(metin.split()) + 0.6)

def beats(cumleler, ilk=0.0):
    b, t = [], ilk
    for c in cumleler:
        b.append(round(t, 2)); t += sure_tahmin(c)
    return b, round(t + 1.4, 2)

# ---------------------------------------------------------------- video tanımları
def v_duyuru():
    ses = ["Merhaba, ben Matlemur! Önemli bir duyuru var!",
           f"MEB, yeni müfredata uyumlu soru modelinin El Ge Se'de iki bin yirmi sekizden itibaren kullanılacağını açıkladı.",
           f"Yeni müfredat {soz(7)} temadan oluşuyor.",
           f"{soz(23).capitalize()} öğrenme çıktısı var.",
           f"Toplam {soz(180)} ders saati!",
           "Önümüzdeki videolarda temaları tek tek anlatıyorum!",
           "Kaydet ve takip et, kaçırma!"]
    alt = ["Merhaba, ben Matlemur! Önemli bir duyuru var!",
           "MEB: yeni müfredata uyumlu soru modeli LGS'de 2028'den itibaren kullanılacak",
           "Yeni müfredat 7 temadan oluşuyor", "23 öğrenme çıktısı var", "Toplam 180 ders saati!",
           "Önümüzdeki videolarda temaları tek tek anlatıyorum!", "Kaydet ve takip et, kaçırma!"]
    b, end = beats(ses)
    cfg = dict(kind='duyuru', accent=GOLD, label='2028 • MAARİF MODELİ', beats=b, end=end, cta=round(b[-1] + .6, 2), subs=alt,
               renkler=[RENK[i] for i in range(1, 8)])
    cap = ("Önemli duyuru 🔔 MEB, yeni müfredata uyumlu soru modelinin LGS'de 2028'den itibaren kullanılacağını açıkladı.\n\n"
           f"Yeni 8. sınıf Maarif matematik müfredatı: {len(TEMALAR)} tema • {TOPLAM_CIKTI} öğrenme çıktısı • {TOPLAM_SAAT} ders saati\n\n"
           "Önümüzdeki videolarda temaları tek tek, madde madde anlatıyorum. Takipte kal!\n\n"
           "Kaydet, LGS 2028 için lazım olur 📌\n\nHer gün matematik için takip et 👆")
    return 'lgs28-01-duyuru', 'Maarif Radarı 1: LGS 2028 soru modeli duyurusu', cfg, ses, cap

def v_saatler():
    rows = [[t[1], t[2], RENK[t[0]], t[0]] for t in TEMALAR] + [['Okul Temelli Planlama', OKUL_TEMELLI, RENK[0], 0]]
    ses = ["Ders saatleri nasıl dağılıyor? Yüz seksen saatin paylarına bak!",
           f"En çok saat, Cebirsel Düşünme ve Değişimler temasında: {soz(42)} saat!",
           f"Sayılar ve Nicelikler {soz(38)}, Geometrik Şekiller {soz(39)} saat.",
           f"Geometrik Nicelikler {soz(15)} saat.",
           f"İstatistiksel Araştırma Süreci {soz(20)} saat.",
           "Dönüşüm ile Veriden Olasılığa dokuzar saat.",
           f"Okul temelli planlama da {soz(8)} saat.",
           f"Toplam {soz(180)} ders saati, {soz(23)} çıktı!",
           "Temaları tek tek anlatacağım! Kaydet ve takip et!"]
    alt = ["Ders saatleri nasıl dağılıyor?", "En çok saat: Cebirsel Düşünme ve Değişimler • 42 saat", "Sayılar ve Nicelikler 38, Geometrik Şekiller 39 saat",
           "Geometrik Nicelikler 15 saat", "İstatistiksel Araştırma Süreci 20 saat", "Dönüşüm ve Veriden Olasılığa 9'ar saat",
           "Okul temelli planlama 8 saat", "Toplam 180 ders saati, 23 çıktı!", "Temaları tek tek anlatacağım! Kaydet ve takip et!"]
    b, end = beats(ses)
    cfg = dict(kind='dagilim', accent=GOLD, label='2028 • MAARİF MODELİ', beats=b, end=end, cta=round(b[-1] + .6, 2), subs=alt, rows=rows,
               hl=[None, [1], [0, 2], [3], [5], [4, 6], [7], None, None])
    sat = "\n".join(f"{t[0]}. {t[1]}: {t[2]} saat" for t in TEMALAR) + f"\nOkul Temelli Planlama: {OKUL_TEMELLI} saat"
    cap = (f"Yeni 8. sınıf Maarif matematik: ders saatleri nasıl dağılıyor? ⏱️\n\n{sat}\n\nToplam: {TOPLAM_SAAT} ders saati • {TOPLAM_CIKTI} öğrenme çıktısı\n\n"
           "Sıradaki videolarda temaları tek tek anlatıyorum.\n\nKaydet, LGS 2028 için lazım olur 📌\n\nHer gün matematik için takip et 👆")
    return 'lgs28-02-saatler', 'Maarif Radarı 2: 8. sınıf matematik ders saati dağılımı', cfg, ses, cap

def v_tema(i):
    no, ad, saat, items = TEMALAR[i]; n = len(items)
    sonraki = TEMALAR[i + 1] if i + 1 < len(TEMALAR) else None
    cikti = 'Tek çıktı' if n == 1 else f'{soz(n).capitalize()} çıktı'
    ses = [f"Maarif modeli, {ORD_KUCUK[no]} tema: {ad}! {cikti}, {soz(saat)} saat."]
    alt = [f"Maarif modeli • {no}. tema: {ad} • {n} çıktı, {saat} saat"]
    for j, (kod, tam, kisa) in enumerate(items):
        ses.append(f"{ORD_BUYUK[j + 1]} çıktı: {kisa}" if n > 1 else f"Çıktı: {kisa}")
        alt.append(ses[-1].replace('a kare artı b kare eşittir c kare', 'a² + b² = c²'))
    if sonraki:
        ses.append(f"Sıradaki tema: {sonraki[1]}! Kaydet ve takip et!"); alt.append(ses[-1])
    else:
        ses.append("Serinin sonu! Kaydet ve takip et, El Ge Se iki bin yirmi sekize hazırlan!"); alt.append("Serinin sonu! Kaydet ve takip et, LGS 2028'e hazırlan!")
    b, end = beats(ses)
    cfg = dict(kind='tema', accent=RENK[no], label='2028 • MAARİF MODELİ', beats=b, end=end, cta=round(b[-1] + .6, 2), subs=alt,
               no=no, name=ad, n=n, hours=saat, items=[[k, t] for k, t, _ in items],
               next=({'no': sonraki[0], 'name': sonraki[1], 'accent': RENK[sonraki[0]]} if sonraki else None))
    liste = "\n".join(f"{k} {t}" for k, t, _ in items)
    cap = (f"2028 LGS • Maarif modeli matematik: {no}. Tema — {ad}\n{n} öğrenme çıktısı • {saat} ders saati\n\n{liste}\n\n"
           + (f"Sıradaki tema: {sonraki[1]}\n\n" if sonraki else "Serinin sonu! Hazırlık başlasın 💪\n\n")
           + "Kaydet, LGS 2028 için lazım olur 📌\n\nHer gün matematik için takip et 👆")
    return f'lgs28-{no + 2:02d}-tema{no}', f'Maarif Radarı {no + 2}: {no}. Tema {ad}', cfg, ses, cap

# ---------------------------------------------------------------- sahne
JS = r"""
const CFG=/*CFG*/;
const ACC=CFG.accent, B=CFG.beats, END=CFG.end, N=B.length, CTA=CFG.cta;
const bi=t=>{let k=0;for(let i=0;i<N;i++)if(t>=B[i])k=i;return k};
const vis=(t,a,b,fi=.4,fo=.4)=>ramp(t,a,a+fi)*(1-ramp(t,b-fo,b));
function wrap(txt,max){const w=txt.split(' '),L=[];let c='';w.forEach(x=>{if(c&&(c+' '+x).length>max){L.push(c);c=x}else c=c?c+' '+x:x});if(c)L.push(c);return L}
function TF(txt,x,y,size,fill,maxW,extra={},parent=main){const t=T(txt,x,y,size,fill,extra,parent);const w=t.getComputedTextLength();if(w>maxW)t.setAttribute('font-size',size*maxW/w);return t}
function chip(x,y,w,h,txt,sz,col,parent){const g=el('g',{},parent);el('rect',{x:x-w/2,y:y-h/2,width:w,height:h,rx:h/2,fill:'rgba(255,255,255,.09)',stroke:col,'stroke-width':3},g);T(txt,x,y+sz*.35,sz,WH,{},g);return g}
const label=T(CFG.label,540,168,34,CY,{'letter-spacing':6});
const tag=T('MATHLEMUR',540,300,56,GOLD,{'letter-spacing':8});
const tit=T('2028 RADARI',540,420,112,WH,{filter:'url(#glow)'});
let big,mini,cards=[],dots=[],outro,A1,A2,A4,ring1,STG=[],ROWS=[],tot;
if(CFG.kind==='tema'){
 big=el('g',{opacity:0}); el('circle',{cx:540,cy:640,r:122,fill:ACC,stroke:'#fff','stroke-width':7},big); T(String(CFG.no),540,696,170,INK,{},big);
 const NL=wrap(CFG.name,20); NL.forEach((l,i)=>T(l,540,860+i*76,66,WH,{filter:'url(#glow)'},big));
 const cy=NL.length>1?1046:972; chip(330,cy,310,76,CFG.n+' ÇIKTI',40,ACC,big); chip(750,cy,310,76,CFG.hours+' SAAT',40,GOLD,big);
 mini=el('g',{opacity:0}); el('circle',{cx:105,cy:540,r:34,fill:ACC,stroke:'#fff','stroke-width':4},mini); T(String(CFG.no),105,556,44,INK,{},mini);
 const mt=el('text',{x:165,y:554,'font-size':42,fill:WH,'text-anchor':'start'},mini); mt.textContent=CFG.name; {const w=mt.getComputedTextLength(); if(w>800)mt.setAttribute('font-size',42*800/w)}
 CFG.items.forEach((it,i)=>{const g=el('g',{opacity:0}); let FS=46, L=wrap(it[1],27); for(const z of [60,54,48,44]){const l=wrap(it[1],Math.floor(800/(z*.63))); FS=z; L=l; if(l.length*z*1.3<=335)break}
  const LH=Math.round(FS*1.3), H=150+L.length*LH+16;
  el('rect',{x:70,y:620,width:940,height:H,rx:40,fill:'rgba(255,255,255,.07)',stroke:ACC,'stroke-width':4},g);
  el('rect',{x:90,y:628,width:900,height:34,rx:17,fill:'#fff',opacity:.06},g);
  const cw=it[0].length*21+44; el('rect',{x:110,y:650,width:cw,height:58,rx:29,fill:ACC},g); T(it[0],110+cw/2,689,32,INK,{},g);
  if(CFG.n>1)T('ÇIKTI '+(i+1)+'/'+CFG.n,970,689,30,CY,{'text-anchor':'end'},g);
  L.forEach((l,j)=>T(l,120,770+FS*.9+j*LH,FS,WH,{'text-anchor':'start'},g)); cards.push(g)});
 for(let i=0;i<CFG.n;i++)dots.push(el('circle',{cx:540+(i-(CFG.n-1)/2)*46,cy:1136,r:11,fill:'rgba(255,255,255,.25)',opacity:0}));
 outro=el('g',{opacity:0});
 if(CFG.next){T('SIRADAKİ TEMA',540,600,84,GOLD,{filter:'url(#glow)'},outro); el('circle',{cx:540,cy:772,r:88,fill:CFG.next.accent,stroke:'#fff','stroke-width':6},outro); T(String(CFG.next.no),540,822,120,INK,{},outro); TF(CFG.next.name,540,950,58,WH,900,{filter:'url(#glow)'},outro)}
 else{T('SERİNİN SONU',540,640,88,GOLD,{filter:'url(#glow)'},outro); T('LGS 2028 YOLUNDA',540,780,66,WH,{},outro); T('HAZIRLIK BAŞLASIN!',540,890,66,CY,{},outro)}
}
if(CFG.kind==='duyuru'){
 A1=el('g',{opacity:0}); ring1=el('circle',{cx:540,cy:690,r:120,fill:'rgba(246,201,69,.14)',stroke:GOLD,'stroke-width':12},A1); T('!',540,765,230,GOLD,{filter:'url(#glow)'},A1);
 T('ÖNEMLİ DUYURU',540,930,84,WH,{filter:'url(#glow)'},A1); T('MEB AÇIKLADI',540,1010,46,CY,{'letter-spacing':6},A1);
 A2=el('g',{opacity:0}); T('Yeni müfredata uyumlu',540,590,58,WH,{},A2); T('SORU MODELİ',540,700,108,GOLD,{filter:'url(#glow)'},A2); T("LGS'DE KULLANILACAK",540,785,52,CY,{'letter-spacing':2},A2);
 T('2028',540,1000,250,WH,{filter:'url(#glow)'},A2); T('İTİBAREN',540,1075,50,GOLD,{'letter-spacing':10},A2);
 [[7,'TEMA'],[23,'ÖĞRENME ÇIKTISI'],[180,'DERS SAATİ']].forEach(([v,l],i)=>{const g=el('g',{opacity:0}), col=[GOLD,CY,'#b794ff'][i];
  el('circle',{cx:540,cy:760,r:260,fill:'none',stroke:'rgba(255,255,255,.12)','stroke-width':14},g);
  const c=el('circle',{cx:540,cy:760,r:260,fill:'none',stroke:col,'stroke-width':14,'stroke-linecap':'round','stroke-dasharray':1634,'stroke-dashoffset':1634,transform:'rotate(-90 540 760)'},g);
  const num=T('0',540,834,210,WH,{filter:'url(#glow)'},g); T(l,540,1085,62,col,{filter:'url(#glow)'},g); STG.push({g,c,num,v})});
 A4=el('g',{opacity:0}); T('SIRADAKİ VİDEOLARDA',540,640,44,CY,{'letter-spacing':6},A4); TF('TEMA TEMA ANLATIYORUM',540,745,70,GOLD,920,{filter:'url(#glow)'},A4);
 CFG.renkler.forEach((c,i)=>{const x=540+(i-3)*135; el('circle',{cx:x,cy:900,r:48,fill:c,stroke:'#fff','stroke-width':4},A4); T(String(i+1),x,918,52,INK,{},A4)});
}
if(CFG.kind==='dagilim'){
 CFG.rows.forEach(([nm,h,col,no],i)=>{const g=el('g',{opacity:0}), y=585+i*62;
  el('circle',{cx:64,cy:y-8,r:23,fill:col},g); T(no?String(no):'•',64,y+2,28,INK,{},g);
  const lt=el('text',{x:104,y:y,'font-size':30,fill:WH,'text-anchor':'start'},g); lt.textContent=nm; {const w=lt.getComputedTextLength(); if(w>455)lt.setAttribute('font-size',30*455/w)}
  const bw=h/42*330, bar=el('rect',{x:575,y:y-32,width:0,height:42,rx:21,fill:col},g);
  const vt=T(h+' saat',587+bw,y+2,30,GOLD,{'text-anchor':'start',opacity:0},g); ROWS.push({g,bar,vt,bw})});
 tot=el('g',{opacity:0}); TF('TOPLAM  180 SAAT  •  23 ÇIKTI',540,1120,50,GOLD,960,{filter:'url(#glow)'},tot);
}
/*MASCOT*/
/*BADGE*/
const SUB=[]; CFG.subs.forEach((s,i)=>{const a=B[i], b=(i+1<N?B[i+1]-.08:END-.3), ch=[]; let c='';
 s.split(' ').forEach(w=>{if(c&&(c+' '+w).length>27){ch.push(c);c=w}else c=c?c+' '+w:w}); if(c)ch.push(c);
 const tot=ch.reduce((m,x)=>m+x.length,0); let t0=a; ch.forEach(x=>{const d=(b-a)*x.length/tot; SUB.push([t0,t0+d,x]); t0+=d})});
/*SUBCTA*/
/*BG*/
/*CF*/
const HOPX=[0,70,-70], XS=B.map((_,i)=>i===N-1?0:HOPX[i%3]);
const HOP=B.slice(1).map((a,i)=>[a,XS[i],XS[i+1]]);
const WK=[[.9,1.6],[CTA+.2,CTA+1.0]];
function content(t){
 if(CFG.kind==='tema'){
  const n=CFG.n;
  setT(big,vis(t,.3,B[1]+.1,.6,.5),.85+.15*back(ramp(t,.3,.9)),540,760);
  setT(mini,vis(t,B[1],B[n+1]+.1,.5,.3),1,540,545);
  cards.forEach((g,i)=>{const a=ramp(t,B[i+1],B[i+1]+.6), e=ramp(t,B[i+2]-.4,B[i+2]), dx=(1-eo(a))*900-eio(e)*900;
   g.setAttribute('transform','translate('+dx+',0)'); g.setAttribute('opacity',(a>0&&e<1)?1:0)});
  const act=bi(t)-1, dop=ramp(t,B[1],B[1]+.4)*(1-ramp(t,B[n+1]-.2,B[n+1]));
  dots.forEach((d,i)=>{d.setAttribute('opacity',dop); d.setAttribute('fill',i<=act?ACC:'rgba(255,255,255,.25)'); d.setAttribute('r',i===act?15:11)});
  setT(outro,ramp(t,B[n+1],B[n+1]+.5),.8+.2*back(ramp(t,B[n+1],B[n+1]+.5)),540,760);
 }
 if(CFG.kind==='duyuru'){
  ring1.setAttribute('r',120+10*Math.sin(t*6));
  setT(A1,vis(t,.3,B[1],.5,.4),.7+.3*back(ramp(t,.3,.9)),540,800);
  setT(A2,vis(t,B[1],B[2],.5,.4),.85+.15*back(ramp(t,B[1],B[1]+.6)),540,800);
  STG.forEach((s,i)=>{const b=B[2+i], e=B[3+i]||END+5, p=eo(ramp(t,b+.1,b+1.1));
   setT(s.g,vis(t,b,e,.4,.3),.8+.2*back(ramp(t,b,b+.6)),540,800); s.num.textContent=Math.round(s.v*p); s.c.setAttribute('stroke-dashoffset',1634*(1-p))});
  setT(A4,ramp(t,B[5],B[5]+.5),.85+.15*back(ramp(t,B[5],B[5]+.6)),540,800);
 }
 if(CFG.kind==='dagilim'){
  const k=bi(t), hl=CFG.hl[k];
  ROWS.forEach((r,i)=>{const a=ramp(t,B[0]+.4+i*.22,B[0]+.9+i*.22), g2=eo(ramp(t,B[0]+.7+i*.22,B[0]+1.5+i*.22));
   const dim=(hl&&!hl.includes(i))?.3:1, on=hl&&hl.includes(i);
   r.g.setAttribute('opacity',a*dim); r.bar.setAttribute('width',Math.max(0,r.bw*g2)); r.bar.setAttribute('filter',on?'url(#glow)':'');
   r.vt.setAttribute('opacity',ramp(g2,.85,1)); r.vt.setAttribute('x',587+r.bw*g2)});
  setT(tot,vis(t,B[7],B[8],.4,.3),.85+.15*back(ramp(t,B[7],B[7]+.5)),540,1105);
 }
}
function mascot(t){
 const app=eo(ramp(t,.1,.9)), bob=7*Math.sin(t*3.1);
 let dx=0,hj=0; for(const [a,f,g] of HOP){ if(t>=a+.45) dx=g; else if(t>=a){const k=(t-a)/.45; dx=f+(g-f)*eio(k); hj=Math.sin(Math.PI*k)*45;} }
 const jd=t-(CTA+.1), jmp=(jd>0&&jd<.7)?Math.sin(Math.PI*jd/.7)*80:0;
 M.setAttribute('transform',`translate(${540+dx},${1440+bob+260*(1-app)-hj-jmp}) scale(.95)`); M.setAttribute('opacity',app);
 const tw=14*Math.sin(t*2.4)+6*Math.sin(t*5.3); tailB.setAttribute('transform',`rotate(${tw} 70 120)`); tailW.setAttribute('transform',`rotate(${tw} 70 120)`);
 const point=eio(ramp(t,B[1],B[1]+.5))*(1-eio(ramp(t,CTA-.3,CTA))), wave=eio(ramp(t,CTA,CTA+.4))*Math.sin((t-CTA)*9), ctaOn=t>=CTA;
 armL.setAttribute('transform',`rotate(${6*Math.sin(t*3)} -95 -20)`);
 armR.setAttribute('transform',`rotate(${-6*Math.sin(t*3+1)+point*(-120+6)+(ctaOn?-1:0)*(60+wave*28)} 95 -20)`);
 head.setAttribute('transform',`rotate(${3*Math.sin(t*1.7)} 0 -60)`);
 const tk=(t>0.5&&t<END-.6)?(.5+.5*Math.sin(t*11)):0, wk=WK.some(([a,b])=>t>=a&&t<b);
 mouth.setAttribute('opacity',0); smile.setAttribute('opacity',(tk<.25||wk)?1:0);
 mo.setAttribute('opacity',(tk>=.25&&!wk)?1:0); mo.setAttribute('transform',`translate(0,-66) scale(1,${.35+.65*tk})`);
 tng.setAttribute('opacity',wk?1:0); tng.setAttribute('transform',`translate(0,${wk?0:-12})`);
 wink.setAttribute('opacity',wk?1:0);
 const bph=t%3.4, blink=Math.max(0,1-Math.abs((bph-3.3)/.09)), big=Math.max(...B.slice(1,3).map(k=>t>k&&t<k+1.2?Math.sin(Math.PI*(t-k)/1.2):0));
 [eL,eR].forEach(e=>e.setAttribute('ry',wk?(e===eR?2:30):30*(1-.9*blink)));
 [iL,iR,pL,pR,hL,hR].forEach(e=>e.setAttribute('opacity',(wk&&(e===iR||e===pR||e===hR))?0:1-blink));
 [iL,iR].forEach(e=>e.setAttribute('r',19+5*big)); [pL,pR].forEach(e=>e.setAttribute('r',10+4*big));
 [chL,chR].forEach(e=>e.setAttribute('opacity',.45+.25*Math.max(big,wk?1:0)));
 const lookY=(t>B[1]&&t<CTA)?-7:2, lookX=Math.sin(t*.9)*3;
 [[iL,-46],[pL,-46]].forEach(([e,x])=>{e.setAttribute('cx',x+lookX);e.setAttribute('cy',-132+lookY)}); [[iR,46],[pR,46]].forEach(([e,x])=>{e.setAttribute('cx',x+lookX);e.setAttribute('cy',-132+lookY)});
 hL.setAttribute('cx',-40+lookX);hL.setAttribute('cy',-139+lookY);hR.setAttribute('cx',52+lookX);hR.setAttribute('cy',-139+lookY);
}
function subs(t){
 const sub=SUB.find(s=>t>=s[0]&&t<s[1]);
 if(sub){const k=SUB.indexOf(sub); if(k!==_subKey){_subKey=k;subT.textContent='';_words=sub[2].split(' ').map(w=>{const sp=document.createElementNS(NS,'tspan');sp.textContent=w+' ';subT.appendChild(sp);return sp})}
  const pr=(t-sub[0])/(sub[1]-sub[0]), cur=Math.min(_words.length-1,Math.floor(pr*1.15*_words.length)); _words.forEach((sp,i)=>sp.setAttribute('fill',i===cur?GOLD:WH));}
 else{_subKey=-1;subT.textContent='';}
 subT.setAttribute('opacity',sub?Math.min(ramp(t,sub[0],sub[0]+.2),1-ramp(t,sub[1]-.15,sub[1])):0);
}
function extra(t){
 P.forEach(o=>{const y=((o.y-o.v*t)%2000+2000)%2000-40, x=o.x+Math.sin(t*.7+o.w)*30; o.e.setAttribute('x',x);o.e.setAttribute('y',y);o.e.setAttribute('opacity',o.o)});
 swp.setAttribute('x',-500+((t*260)%1900));
 pb.setAttribute('width',960*clamp(t/END));
 const punch=B.reduce((m,k)=>Math.max(m,t>k?Math.exp(-(t-k)*7)*.03:0),0);
 const z=1+.04*(t/END)+punch, cx=540+Math.sin(t*.5)*14, cy=960+Math.cos(t*.4)*10;
 mainG.setAttribute('transform',`translate(${cx},${cy}) scale(${z}) translate(-540,-960)`);
 CF.forEach(c=>{const dt=t-c.t0; if(dt<0||dt>1.3){c.e.setAttribute('opacity',0);return}
  c.e.setAttribute('cx',c.x+c.vx*dt);c.e.setAttribute('cy',c.y+c.vy*dt+700*dt*dt);c.e.setAttribute('opacity',1-ramp(dt,.7,1.3))});
 const rr=RINGS.find(r=>t>=r[0]&&t<r[0]+.7);
 if(rr){const d=(t-rr[0])/.7;ring.setAttribute('cx',540);ring.setAttribute('cy',rr[2]);ring.setAttribute('r',40+520*eo(d));ring.setAttribute('stroke',rr[1]);ring.setAttribute('opacity',1-d)}else ring.setAttribute('opacity',0);
 wsh.setAttribute('x',300+(((t*330)%1700+1700)%1700)-300);
 WSP.forEach((e,i)=>{const q=.5+.5*Math.sin(t*4+i*1.9), [x,y]=[[210,1742],[872,1818],[700,1734],[380,1826]][i]; e.setAttribute('opacity',q); e.setAttribute('transform',`translate(${x},${y}) scale(${.35+.65*q}) rotate(${t*50}) translate(${-x},${-y})`)});
 const cq=ramp(t,CTA,CTA+.8), fl=Math.cos(Math.PI*(1-eio(cq))), pl=1+.025*Math.sin((t-CTA)*7)*cq;
 cta.setAttribute('opacity',cq>0?1:0); cta.setAttribute('transform',`translate(540,1145) scale(${pl},${fl*pl}) translate(-540,-1145)`);
 shine.setAttribute('x',-200+(((t-CTA)*700)%1500+1500)%1500);
 SPK.forEach((e,i)=>{const p=.5+.5*Math.sin(t*5+i*1.7); e.setAttribute('opacity',cq*p); const [x,y]=[[150,1080],[930,1094],[300,1215],[790,1210],[540,1072]][i]; e.setAttribute('transform',`translate(${x},${y}) scale(${.4+.6*p}) rotate(${t*60}) translate(${-x},${-y})`)});
}
window.seek=t=>{
 const p0=ramp(t,.2,.8); setT(tag,p0,.85+.15*back(p0),540,250); setT(tit,p0,.7+.3*back(p0),540,400);
 label.setAttribute('opacity',ramp(t,.1,.6));
 content(t); mascot(t); subs(t); extra(t);
};
seek(0);
</script>
"""

def sahne_html(cfg):
    base = open(f'{R}/icerik/tum-av-01/sahne.html', encoding='utf-8').read()
    cut = lambda a, b: base[base.index(a):base.index(b)]
    head = base[:base.index('// ---------- başlık')]
    masc = cut('// ---------- MATLEMUR', 'const six=')
    badge = cut('// ---------- altyazı + CTA', 'const SUB=')
    subcta = cut('const subT=', "const svg=document.getElementById('s')")
    bg = cut("const svg=document.getElementById('s')", 'const bol=mk(')
    cf = base[base.index('const CF=[];'):]; cf = cf[:cf.index('const ring=mk(')]; cf = cf[:cf.index('const BURSTS')] + '''const BURSTS=BURST_LIST;
BURSTS.forEach(([t0,x,y,c],bi)=>{for(let i=0;i<16;i++){const a=rnd()*6.28,v=250+rnd()*420;CF.push({e:mk('circle',{r:5+rnd()*8,fill:i%2?c:'#ffffff'},topG),t0,x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v-200,});}});
'''
    ring = "const ring=mk('circle',{fill:'none','stroke-width':8},topG);\n"
    c = cfg['cta']; b = cfg['beats']
    bursts = [[c + .1, 540, 1180, GOLD], [c + .5, 540, 1150, '#fff1b0'], [c + .9, 540, 1120, CY]]
    rings = [[c + .1, GOLD, 1180]]
    if cfg['kind'] == 'duyuru':
        for i in range(3): bursts.append([b[2 + i] + 1.0, 540, 800, ['#f6c945', CY, '#b794ff'][i]]); rings.append([b[2 + i] + 1.0, [GOLD, CY, '#b794ff'][i], 800])
        bursts.append([b[1] + .3, 540, 1000, GOLD])
    if cfg['kind'] == 'dagilim': bursts.append([b[7] + .3, 540, 1110, GOLD]); rings.append([b[7] + .3, GOLD, 1110])
    if cfg['kind'] == 'tema': bursts.append([b[1] + .3, 540, 850, cfg['accent']])
    cf = cf.replace('BURST_LIST', json.dumps(bursts)) + ring + f"const RINGS={json.dumps(rings)};\n"
    js = JS.replace('/*CFG*/', json.dumps(cfg, ensure_ascii=False)).replace('/*MASCOT*/', masc).replace('/*BADGE*/', badge) \
           .replace('/*SUBCTA*/', subcta).replace('/*BG*/', bg).replace('/*CF*/', cf)
    return head + js

def yaz(slug, baslik, cfg, ses, cap):
    d = f'{R}/icerik/{slug}'; os.makedirs(d + '/ses', exist_ok=True)
    open(d + '/sahne.html', 'w', encoding='utf-8').write(sahne_html(cfg))
    open(d + '/ses/metin.txt', 'w', encoding='utf-8').write('\n'.join(ses) + '\n')
    b = cfg['beats']; n = len(b); sfx = [{'t': 0.3, 'tip': 'pop'}]
    for i, t in enumerate(b):
        if i: sfx.append({'t': round(t + .05, 2), 'tip': 'whoosh_kisa', 'g': .5})
        if cfg['kind'] == 'tema' and 0 < i < n - 1: sfx.append({'t': round(t + .5, 2), 'tip': 'ding', 'g': .5})
    sfx.append({'t': round(cfg['cta'] + .2, 2), 'tip': 'sparkle', 'g': .6}); sfx.append({'t': round(cfg['cta'] + .6, 2), 'tip': 'pop', 'g': .7})
    uzun = [m for m in K.MUZ if float(__import__('subprocess').check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{R}/kutuphane/muzik/{m}']).decode()) >= 80]
    no = int(slug.split('-')[1])
    ses_json = {'sure': cfg['end'], 'bpm': 128, 'sfx': sfx, 'sahne_basi': b, 'sahne_sonu': cfg['end'],
                'muzik_dosya': 'kutuphane/muzik/' + uzun[(no + 2) % len(uzun)], 'muzik_baslangic': 6}
    json.dump(ses_json, open(d + '/ses.json', 'w', encoding='utf-8'), ensure_ascii=False)
    pj = f'{d}/post.json'
    old = json.load(open(pj)) if os.path.exists(pj) else {}
    post = {'baslik': baslik, 'tur': 'özgün', 'sure': 60, 'fps': 30, 'caption': cap, 'hashtagler': ETIKET,
            'kaynak': 'MEB açıklaması ve yeni 8. sınıf Maarif matematik programı bilgileri; özgün Mathlemur tasarımı',
            'durum': old.get('durum', 'taslak') if old.get('durum') in ('taslak', 'onay-bekliyor') else 'taslak', 'ana_izgara': False,
            'kayit': old.get('kayit', []) + ['seri taslağı üretildi (yayın tarihini kullanıcı belirleyecek)']}
    json.dump(post, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); open(pj, 'a').write('\n')
    return slug

def hepsi():
    return [v_duyuru(), v_saatler()] + [v_tema(i) for i in range(7)]

if __name__ == '__main__':
    secim = set(sys.argv[1:])
    for v in hepsi():
        if secim and v[0] not in secim: continue
        print(yaz(*v), f'beats={len(v[2]["beats"])} end={v[2]["end"]}')
