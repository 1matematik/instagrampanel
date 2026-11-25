#!/usr/bin/env python3
"""ARALARINDA ASAL: peki sonra? serisi (7 video, zincirli). Senaryo: claude/asal-serisi.md (Fable tasarımı, 25 Kas).
Kullanım: python3 yayin/asal_uret.py [asal-01 ...]  → icerik/asal-NN/{sahne.html, ses.json, ses/metin.txt, post.json}
Çerçeve: ekok_uret (diyagram öğeleri, JS) + mufredat_uret."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import ekok_uret as X
import mufredat_uret as MU
from ekok_uret import ln, ci, rc, tx, sp, GOLD, CY, KIRMIZI, YESIL, TURUNCU, PEMBE

R = X.R
ETIKET = ['aralarındaasal', 'lgsmatematik', 'matematik', 'tuzak', 'keşfet']

def dia1():
    L = [ci(270, 600, 44, '#14502a', [1, .3], GOLD, 5), tx('8', 270, 616, 52, '#fff', [1, .3]), ci(810, 600, 44, '#14502a', [1, .5], GOLD, 5), tx('15', 810, 616, 52, '#fff', [1, .5])]
    for k, x in enumerate([180, 270, 360]):
        L += [ln(270, 640, x, 705, '#cfe8d4', 3, t=[1, 1.2 + .3 * k]), ci(x, 740, 30, YESIL, [1, 1.2 + .3 * k]), tx('2', x, 752, 36, '#06210f', [1, 1.2 + .3 * k])]
    for k, (x, v) in enumerate([(750, '3'), (870, '5')]):
        L += [ln(810, 640, x, 705, '#cfe8d4', 3, t=[1, 2.4 + .3 * k]), ci(x, 740, 30, TURUNCU, [1, 2.4 + .3 * k]), tx(v, x, 752, 36, '#06210f', [1, 2.4 + .3 * k])]
    L += [tx('ortak çarpan?', 540, 690, 30, '#fff', [3, .3]), tx('YOK!', 540, 745, 46, KIRMIZI, [4, .4]), tx('ortak bölen: yalnız 1', 540, 860, 36, GOLD, [4, 1.6])]
    return L

def dia2():
    L = []
    rows = [('34  –  35', '✓', YESIL, 'ardışık sayılar'), ('48  –  50', '✗', KIRMIZI, 'ikisi de çift: 2 ortak'), ('1  –  100', '✓', YESIL, '1 her sayıyla')]
    for i, (a, m, c, why) in enumerate(rows):
        y = 565 + i * 100
        L += [rc(60, y, 960, 84, 'rgba(10,50,25,.85)', [1, .6 + .8 * i], '#cfe8d4', 3, 22), tx(a, 100, y + 58, 50, '#fff', [1, .6 + .8 * i], 'start'),
              tx(m, 700, y + 60, 56, c, [4, .3 + 1.7 * i]), tx(why, 1000, y + 55, 28, c, [4, .3 + 1.7 * i], 'end')]
    return L

def dia3():
    L = [tx('36', 280, 640, 96, YESIL, [1, .5]), ln(190, 665, 370, 665, '#fff', 6, t=[1, .5]), tx('48', 280, 770, 96, TURUNCU, [1, .5]),
         tx('÷ 12', 540, 690, 52, GOLD, [4, .3]), tx('→', 540, 760, 70, GOLD, [4, .3]),
         tx('3', 800, 640, 96, YESIL, [4, 1.6]), ln(710, 665, 890, 665, '#fff', 6, t=[4, 1.6]), tx('4', 800, 770, 96, TURUNCU, [4, 1.6]),
         tx('a + b = 3 + 4 = 7', 540, 880, 40, GOLD, [4, 3.6])]
    return L

def dia4():
    L = []
    rows = [('1 × 36', '✓', YESIL, ''), ('2 × 18', '✗', KIRMIZI, 'EBOB 2'), ('3 × 12', '✗', KIRMIZI, 'EBOB 3'), ('4 × 9', '✓', YESIL, ''), ('6 × 6', '✗', KIRMIZI, 'EBOB 6')]
    for i, (a, m, c, why) in enumerate(rows):
        y = 590 + i * 54
        L += [tx(a, 330, y, 38, '#fff', [1, .4 + .35 * i], 'start'), tx(m, 640, y, 40, c, [4, .2 + .8 * i])]
        if why: L.append(tx(why, 780, y, 28, c, [4, .2 + .8 * i], 'start'))
    L.append(tx('en az toplam: 4 + 9 = 13', 540, 885, 38, GOLD, [4, 4.6]))
    return L

def dia5():
    L = []; surv = {1, 5, 7, 11, 13, 17, 19}
    for n in range(1, 20):
        x = 103 + (n - 1) * 46
        L += [rc(x, 650, 42, 56, 'rgba(255,255,255,.12)', [1, .3 + .12 * n], '#cfe8d4', 2, 8), tx(str(n), x + 21, 690, 24, '#fff', [1, .3 + .12 * n])]
    L.append(tx('2 ve 3’ün katları elenir', 540, 760, 34, '#fff', [4, .3]))
    k = 0
    for n in range(1, 20):
        if n not in surv:
            x = 103 + (n - 1) * 46; L.append(rc(x, 650, 42, 56, 'rgba(255,107,107,.55)', [4, .6 + .18 * k], KIRMIZI, 3, 8)); k += 1
    for j, n in enumerate(sorted(surv)):
        x = 103 + (n - 1) * 46; L.append(rc(x, 650, 42, 56, 'none', [4, 3.0 + .15 * j], GOLD, 5, 8))
    L.append(tx('7 sayı', 540, 850, 52, GOLD, [4, 4.4]))
    return L

def dia6():
    X_ = lambda t: 90 + t * 13.5; L = [ln(90, 720, 990, 720, '#cfe8d4', 4, t=[1, .3]), tx('A: 7 sn', 990, 612, 32, YESIL, [1, .4], 'end'), tx('B: 9 sn', 990, 838, 32, TURUNCU, [1, .5], 'end')]
    for i, t in enumerate(range(0, 64, 7)): L.append(ci(X_(t), 650, 9, YESIL, [1, .6 + .1 * i]))
    for i, t in enumerate(range(0, 64, 9)): L.append(ci(X_(t), 780, 9, TURUNCU, [1, .8 + .12 * i]))
    L += [ln(X_(63), 650, X_(63), 780, GOLD, 3, '6 8', [4, .6]), ci(X_(63), 720, 16, GOLD, [4, .6], '#fff', 3), tx('63', X_(63), 765, 28, '#fff', [4, .6]), tx('7 × 9 = 63', X_(63) - 40, 600, 32, GOLD, [4, .6], 'end'),
          tx('6 ve 8: 6 × 8 = 48 değil, EKOK 24!', 540, 885, 34, KIRMIZI, [5, 1.2])]
    return L

def dia7():
    L = [rc(90, 610, 336, 70, YESIL, [1, .4], '#06210f', 3, 8), tx('48', 258, 655, 40, '#06210f', [1, .4]), rc(90, 710, 420, 70, TURUNCU, [1, .8], '#06210f', 3, 8), tx('60', 300, 755, 40, '#06210f', [1, .8])]
    for k in range(1, 5): L.append(ln(90 + 84 * k, 600, 90 + 84 * k, 790, GOLD, 4, '6 6', [4, .3 + .3 * k]))
    L += [tx('4', 640, 655, 70, YESIL, [4, 2.2]), tx('5', 640, 755, 70, TURUNCU, [4, 2.2]), tx('ortak bölen yok ✓', 880, 705, 34, GOLD, [4, 3.0]),
          tx('6’ya bölsen: 8 ve 10 → ortak 2 kalır', 540, 870, 32, KIRMIZI, [4, 4.4])]
    return L

EP = [
 dict(slug='asal-01', tur='ASAL DEĞİL AMA', dia=dia1, prev='120', hook='Asal olmak şart mı?', badge='EBOB = 1', bcol=GOLD,
  s=["Ben Matlemur! Geçen cevap: 120, yani tam 8 çarpı 15.", "8 asal mı? Değil. 15 de asal değil.", "Ama ortak bölenleri yalnız 1; yani EBOB 1.",
     "Peki sonra? Aralarında asal olmak için asal olmak şart mı?", "Hayır! Tek tek asal olmaları gerekmez. Ortak bölenin yalnız 1 olması yeter.",
     "Kural: Aralarında asal demek, EBOB 1 demek.", "Sıra sende! Hangisi aralarında asal değil: 4 ile 9, 7 ile 21, 14 ile 15?"],
  prob=['8 ve 15 asal mı?', 'ikisi de asal değil!'], ekok=['EBOB(8, 15) = 1', 'ortak bölen: yalnız 1'], calc=['8 = 2 · 2 · 2', '15 = 3 · 5', 'ortak çarpan yok → aralarında asal'],
  rule=['ARALARINDA ASAL = EBOB 1', 'asal olmak şart değil'], nextq=['Hangisi aralarında asal', 'DEĞİL?  4-9 · 7-21 · 14-15', '', 'HANGİSİ?']),
 dict(slug='asal-02', tur='HESAPSIZ 3 TEST', dia=dia2, prev='7 ile 21', hook='Hesapsız nasıl?', badge='ARDIŞIK EVET', bcol=YESIL,
  s=["Ben Matlemur! Geçen cevap: 7 ile 21. 7 asal ama 21'i bölüyor.", "34 ile 35, 48 ile 50, 1 ile 100. Hangileri aralarında asal?", "EBOB hesaplamaya gerek yok.",
     "Peki sonra? Hesapsız nasıl anlarım?", "Ardışık iki sayı her zaman aralarında asaldır: 34 ile 35 tamam. İki çift sayı asla olmaz, çünkü 2 ortaktır. 1 ise her sayıyla aralarında asaldır.",
     "Kural: Ardışık evet, iki çift hayır, 1 her sayıyla evet.", "Sıra sende! Bir tek, bir çift sayı her zaman aralarında asal mıdır? 15 ile 18'i dene."],
  prob=['34-35 · 48-50 · 1-100', 'hangisi aralarında asal?'], ekok=['EBOB hesabı yok!', 'kural bilmek yeter'], calc=['ardışık sayılar → EVET', 'iki çift sayı → HAYIR', '1 ile her sayı → EVET'],
  rule=['ARDIŞIK EVET, İKİ ÇİFT HAYIR', '1 her sayıyla aralarında asal'], nextq=['Bir tek, bir çift sayı', 'her zaman aralarında asal mı?', '15 ile 18’i dene.', 'EVET Mİ?']),
 dict(slug='asal-03', tur='KESRİN SADE HÂLİ', dia=dia3, prev='Hayır', hook='36 + 48 = 84 mü?', badge='SADE KESİR', bcol=CY,
  s=["Ben Matlemur! Geçen cevap: hayır. 15 ile 18'in ortak böleni 3.", "a ile b aralarında asal ve a bölü b, 36 bölü 48'e eşit. a artı b soruluyor.", "36 ile 48'in EBOB'u 12.",
     "Peki sonra? a 36, b 48 mi; toplam 84 mü?", "Hayır! 36 ile 48 aralarında asal değil. İkisini de 12'ye böl: 3 bölü 4. Toplam 7.",
     "Kural: Aralarında asal demek, kesrin en sade hâli demek.", ("Sıra sende! a ile b aralarında asal ve a bölü b, 0,6 ise a artı b kaç?", "Sıra sende! a ile b aralarında asal ve a bölü b, sıfır virgül altı ise a artı b kaç?")],
  prob=['a/b = 36/48, a ve b', 'aralarında asal; a + b = ?'], ekok=['EBOB(36, 48) = 12', '36/48 = 3/4'], calc=['36 ÷ 12 = 3', '48 ÷ 12 = 4', 'a + b = 3 + 4 = 7'],
  rule=['ARALARINDA ASAL = SADE KESİR', 'a/b sadeleşmiş hâlidir'], nextq=['a/b = 0,6 ve a ile b', 'aralarında asal ise', 'a + b kaç?', 'KAÇ?']),
 dict(slug='asal-04', tur='ÇARPIM 36', dia=dia4, prev='8', hook='6 × 6 → 12 mi?', badge='ÇİFTLERİ ELE', bcol=TURUNCU,
  s=[("Ben Matlemur! Geçen cevap: 8; çünkü 0,6, en sade hâliyle 3 bölü 5.", "Ben Matlemur! Geçen cevap: 8; çünkü sıfır virgül altı, en sade hâliyle 3 bölü 5."),
     "a ile b aralarında asal ve çarpımları 36. a artı b en az kaç?", "Çarpımı 36 olan çiftleri yazalım.", "Peki sonra? 6 çarpı 6 deyip 12 mi diyeceğiz?",
     "Hayır! 6 ile 6 aralarında asal değil. 2 ile 18 ve 3 ile 12 de değil. Kalanlar: 1 ile 36, 4 ile 9. En az toplam 13.",
     "Kural: Çarpan çiftlerini yaz, ortak böleni olanları ele.", "Sıra sende! a ile b aralarında asal, çarpımları 60. a artı b en az kaç?"],
  prob=['a, b aralarında asal', 'a × b = 36, a + b en az?'], ekok=['çarpan çiftlerini yaz', 'ortak böleni olanı ele'], calc=['EBOB 1 olanlar: 1×36, 4×9', '1 + 36 = 37', '4 + 9 = 13 → en az'],
  rule=['ÇİFTLERİ YAZ, ORTAK BÖLENİ ELE', '1 ile 36 ve 4 ile 9 kalır'], nextq=['a, b aralarında asal,', 'a × b = 60,', 'a + b en az kaç?', 'KAÇ?']),
 dict(slug='asal-05', tur='12 İLE ARALARINDA ASAL', dia=dia5, prev='17', hook='Yalnız asalları mı?', badge='BÖLMEMEK ŞART', bcol=CY,
  s=["Ben Matlemur! Geçen cevap: 17; sayılar 5 ile 12.", "20'den küçük kaç sayma sayısı 12 ile aralarında asaldır?", "12'nin asal çarpanları 2 ve 3.",
     "Peki sonra? Sadece asal sayıları mı sayacağım?", "Hayır! 2'ye de 3'e de bölünmeyenleri say: 1, 5, 7, 11, 13, 17, 19. Cevap 7.",
     "Kural: 2 ve 3 asal ama sayılmaz. 1 asal değil ama sayılır.", "Sıra sende! 20 ile 30 arasında, 12 ile aralarında asal kaç sayı var?"],
  prob=['20’den küçük kaç sayı', '12 ile aralarında asal?'], ekok=['12 = 2 · 2 · 3', '2’ye ve 3’e bölünmesin'], calc=['1, 5, 7, 11, 13, 17, 19', '2 ve 3 sayılmaz', '1 sayılır → 7 sayı'],
  rule=['ASAL OLMAK DEĞİL, BÖLMEMEK', '2 ve 3’e bölünmeyenler'], nextq=['20 ile 30 arasında', '12 ile aralarında asal', 'kaç sayı var?', 'KAÇ SAYI?']),
 dict(slug='asal-06', tur='EBOB 1 İSE', dia=dia6, prev='3', hook='Tablo şart mı?', badge='EKOK = ÇARPIM', bcol=TURUNCU,
  s=["Ben Matlemur! Geçen cevap: 3; yani 23, 25 ve 29.", "İki ışık 7 ve 9 saniyede bir yanıyor. Şimdi birlikte yandılar.", "7 ile 9 aralarında asal.",
     "Peki sonra? EKOK için bölme tablosu şart mı?", "Hayır! Aralarında asalsa EKOK doğrudan çarpımdır: 7 çarpı 9, 63.",
     "Kural: EBOB 1 ise EKOK çarpıma eşittir. 6 ile 8'de olmaz: EBOB 2, EKOK 24, 48 değil.", "Sıra sende! a ile b aralarında asal ve EKOK'ları 45. a artı b en az kaç?"],
  prob=['7 sn ve 9 sn’de bir ışık', 'birlikte yandılar'], ekok=['EBOB(7, 9) = 1', 'aralarında asal!'], calc=['EKOK = 7 × 9', '= 63 sn', '6 ve 8: EBOB 2, EKOK 24'],
  rule=['EBOB 1 İSE EKOK = ÇARPIM', '6 × 8 = 48 olmaz!'], nextq=['a, b aralarında asal,', 'EKOK 45,', 'a + b en az kaç?', 'KAÇ?']),
 dict(slug='asal-07', tur='SAĞLAMA', dia=dia7, prev='14', hook='Doğru mu buldum?', badge='SAĞLAMA', bcol=YESIL,
  s=["Ben Matlemur! Geçen cevap: 14; sayılar 5 ile 9.", "48 ile 60 için EBOB'u 12 buldum.", "Doğru olabilir mi?", "Peki sonra? Doğru bulduğumu nasıl anlarım?",
     "İkisini de 12'ye böl: 4 ve 5. Aralarında asal, demek EBOB doğru. 6'ya bölseydim 8 ve 10 çıkardı; ortak 2 kaldı, EBOB eksik demek.",
     "Kural: Sayıları EBOB'a bölünce çıkan sayılar aralarında asaldır.", "Sıra sende! EBOB'u 6, toplamı 30 olan iki farklı sayı kaç değişik şekilde seçilir?"],
  prob=['48 ve 60 için', 'EBOB = 12 buldum'], ekok=['EBOB(48, 60) = 12', 'doğru mu?'], calc=['48 ÷ 12 = 4', '60 ÷ 12 = 5', '4 ve 5 aralarında asal ✓'],
  rule=['BÖLÜMLER ARALARINDA ASAL', 'değilse EBOB eksik'], nextq=['EBOB’u 6, toplamı 30', 'olan iki farklı sayı', 'kaç değişik şekilde?', 'KAÇ ŞEKİL?']),
]

def tanim(e, no):
    alt = [x[0] if isinstance(x, tuple) else x for x in e['s']]
    ses = [x[1] if isinstance(x, tuple) else sp(x) for x in e['s']]
    b, end = MU.beats(ses)
    cfg = dict(kind='ekok', accent=GOLD, title='ARALARINDA ASAL: PEKİ SONRA?', label=f'BÖLÜM {no} • {e["tur"]}', beats=b, end=end, cta=round(b[-1] + .6, 2), subs=alt,
               dia=e['dia'](), prev=e['prev'], hook=e['hook'], badge=e['badge'], bcol=e['bcol'], prob=e['prob'], ekok=e['ekok'], calc=e['calc'], rule=e['rule'], nextq=e['nextq'],
               bursts=[[b[5] + .3, 540, 800, e['bcol']]], rings=[[b[5] + .3, e['bcol'], 800]])
    nxt = 'Cevap sonraki videoda!' if no < 7 else 'Cevabı yoruma yaz!'
    cap = (f"ARALARINDA ASAL: PEKİ SONRA? 🔗 (Bölüm {no}: {e['tur'].title()})\n\n" + ' · '.join(x for x in e['calc'] if x) + f"\n\nKural: {' — '.join(e['rule'])}\n\n"
           + 'SIRA SENDE: ' + ' '.join(x for x in e['nextq'] if x) + f' {nxt}\n\nKaydet, LGS matematik için lazım olur 📌\n\nHer gün matematik için takip et 👆')
    return e['slug'], f'Aralarında asal {no}: {e["tur"].title()}', cfg, ses, cap

def yaz(slug, baslik, cfg, ses, cap):
    X.ETIKET = ETIKET
    X.yaz(slug, baslik, cfg, ses, cap)
    pj = f'{R}/icerik/{slug}/post.json'; p = json.load(open(pj))
    p['kaynak'] = 'Aralarında asal serisi (plan: Fable tasarımı + kullanıcı fikri; sayılar ve anlatım özgün Mathlemur)'
    p['kayit'] = [k for k in p['kayit'] if 'EKOK' not in k] + ['Aralarında asal serisi taslağı üretildi (Paket 2; yayın zamanı onaydan sonra)']
    json.dump(p, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); open(pj, 'a').write('\n')
    return slug

if __name__ == '__main__':
    secim = set(sys.argv[1:])
    for no, e in enumerate(EP, 1):
        if secim and e['slug'] not in secim: continue
        v = tanim(e, no); print(yaz(*v), 'end=', v[2]['end'])
