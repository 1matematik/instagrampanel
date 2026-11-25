#!/usr/bin/env python3
"""EKOK bulundu, peki sonra? serisi (8 video, zincirli). Senaryo: claude/ekok-tuzaklari-serisi.md (Fable incelemesi, 25 Kas).
Kullanım: python3 yayin/ekok_uret.py [ekok-01 ...]  → icerik/ekok-NN/{sahne.html, ses.json, ses/metin.txt, post.json}
Çerçeve: ebob_uret/mufredat_uret (Mathlemur, orman). Diyagramlar cfg['dia'] öğeleriyle (k=SVG etiketi, t=[beat,sn] belirme)."""
import os, sys, json, re, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import ebob_uret as E
import kok_uret as K
import mufredat_uret as MU

R, soz = K.R, K.soz
GOLD, CY, KIRMIZI, YESIL, TURUNCU, PEMBE = E.GOLD, E.CY, E.KIRMIZI, E.YESIL, E.TURUNCU, E.PEMBE
ETIKET = ['ekok', 'lgsmatematik', 'matematik', 'tuzak', 'keşfet']

def sp(s):
    """altyazı metnini (rakamlı) okunuşa çevirir: 12'ye → on ikiye, 8 → sekiz"""
    s = re.sub(r"(\d+)['’]([a-zçğıöşü]+)", lambda m: soz(int(m.group(1))) + m.group(2), s)
    return re.sub(r"\d+", lambda m: soz(int(m.group(0))), s)

# ---- diyagram öğeleri
def ln(x1, y1, x2, y2, col, w=4, dash=None, t=None, h=None):
    a = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'stroke': col, 'stroke-width': w, 'stroke-linecap': 'round'}
    if dash: a['stroke-dasharray'] = dash
    return dict(k='line', a=a, t=t, h=h)
def ci(cx, cy, r, fill, t, stroke='#fff', sw=2, h=None):
    return dict(k='circle', a={'cx': round(cx, 1), 'cy': cy, 'r': r, 'fill': fill, 'stroke': stroke, 'stroke-width': sw}, t=t, h=h)
def rc(x, y, w, hh, fill, t, stroke='#06210f', sw=2, rx=6, dash=None, h=None):
    a = {'x': round(x, 1), 'y': round(y, 1), 'width': round(w, 1), 'height': round(hh, 1), 'rx': rx, 'fill': fill, 'stroke': stroke, 'stroke-width': sw}
    if dash: a['stroke-dasharray'] = dash
    return dict(k='rect', a=a, t=t, h=h)
def tx(txt, x, y, size, fill, t, anchor=None, h=None):
    ex = {'text-anchor': anchor} if anchor else {}
    return dict(k='text', a={'txt': txt, 'x': round(x, 1), 'y': y, 'size': size, 'fill': fill, 'extra': ex}, t=t, h=h)

def dia1():
    X = lambda t: 90 + t * 4.5; L = []
    L += [ln(90, 720, 990, 720, '#cfe8d4', 4, t=[1, .3]), tx('A: 12 saniyede bir', 990, 612, 32, YESIL, [1, .4], 'end'), tx('B: 18 saniyede bir', 990, 838, 32, TURUNCU, [1, .5], 'end')]
    for i, t in enumerate(range(0, 201, 12)): L.append(ci(X(t), 650, 8, YESIL, [1, .7 + .06 * i]))
    for i, t in enumerate(range(0, 201, 18)): L.append(ci(X(t), 780, 8, TURUNCU, [1, .9 + .07 * i]))
    def mark(t, at, lab=None):
        L.append(ln(X(t), 650, X(t), 780, GOLD, 3, '6 8', at)); L.append(ci(X(t), 720, 15, GOLD, at, '#fff', 3)); L.append(tx(str(t), X(t), 758, 26, '#fff', at))
        if lab: L.append(tx(lab, X(t), 692, 28, GOLD, at))
    mark(36, [2, .3], 'EKOK = 36')
    for i, t in enumerate([72, 108, 144, 180]): mark(t, [4, .5 + .55 * i])
    mark(0, [4, 3.0]); L.append(tx('+1', 90, 692, 34, KIRMIZI, [4, 3.0], 'start'))
    L.append(tx('5 sonraki + 1 başlangıç = 6', 540, 895, 34, GOLD, [4, 3.6]))
    return L

def dia2():
    X = lambda t: 90 + t * 10; L = []
    L += [ln(90, 720, 990, 720, '#cfe8d4', 4, t=[1, .3]), tx('A: 08:00, 12 dk', 990, 612, 32, YESIL, [1, .4], 'end'), tx('B: 08:09, 15 dk', 990, 862, 32, TURUNCU, [1, .5], 'end')]
    for i, t in enumerate(range(0, 91, 12)): L.append(ci(X(t), 650, 9, YESIL, [1, .7 + .1 * i]))
    for i, t in enumerate(range(9, 91, 15)): L.append(ci(X(t), 790, 9, TURUNCU, [1, 1.0 + .12 * i]))
    L += [ln(X(24), 650, X(24), 790, GOLD, 3, '6 8', [4, 1.2]), ci(X(24), 720, 16, GOLD, [4, 1.2], '#fff', 3), tx('08:24', X(24), 690, 30, GOLD, [4, 1.2])]
    L += [ln(X(84), 650, X(84), 790, GOLD, 3, '6 8', [5, 1.4]), ci(X(84), 720, 16, GOLD, [5, 1.4], '#fff', 3), tx('09:24', X(84), 690, 30, GOLD, [5, 1.4]), tx('+60 dk', X(54), 690, 30, CY, [5, 1.0])]
    return L

def dia3():
    X = lambda cm: 90 + cm * 1.8; L = [rc(90, 770, 720, 16, '#8b5a2b', [1, .2], '#e0b070', 3, 4), tx('RAF: 4 m = 400 cm', 90, 826, 32, '#fff', [1, .3], 'start')]
    for i in range(20):
        t = [1, .6 + .2 * i] if i < 15 else [4, 1.4 + .15 * (i - 15)]
        L.append(rc(90 + 43.2 * i, 620, 40.2, 56, YESIL if i < 15 else KIRMIZI, t))
    for j in range(12):
        t = [1, .8 + .3 * j] if j < 9 else [4, 1.6 + .2 * (j - 9)]
        L.append(rc(90 + 72 * j, 700, 69, 56, TURUNCU if j < 9 else KIRMIZI, t))
    for k, cm in enumerate([120, 240, 360]):
        L += [ln(X(cm), 590, X(cm), 770, GOLD, 3, '6 8', [4, .4 + .5 * k]), tx(str(cm), X(cm), 582, 30, GOLD, [4, .4 + .5 * k])]
    L += [ln(X(480), 590, X(480), 770, KIRMIZI, 4, '6 8', [4, 2.2]), tx('480 taşar', 1040, 582, 30, KIRMIZI, [4, 2.2], 'end')]
    L.append(tx('en uzun: 360 cm', 540, 880, 38, GOLD, [4, 3.4]))
    return L

def dia4():
    L = []; hA, hB, base = 18 * 1.35, 24 * 1.35, 860
    L += [ln(120, base, 960, base, '#cfe8d4', 4, t=[1, .2]), ln(120, base - 270, 960, base - 270, KIRMIZI, 4, '10 8', [1, .3]), tx('2 m = 200 cm', 775, base - 258, 24, KIRMIZI, [1, .3], 'start')]
    for i in range(12):
        t = [1, .8 + .25 * i] if i < 8 else [4, 2.4 + .25 * (i - 8)]
        L.append(rc(330, base - (i + 1) * hA, 140, hA - 1.5, YESIL if i % 2 == 0 else '#5fc872', t))
    for i in range(9):
        t = [1, .8 + .33 * i] if i < 6 else [4, 2.4 + .3 * (i - 6)]
        L.append(rc(610, base - (i + 1) * hB, 140, hB - 1.5, TURUNCU if i % 2 == 0 else '#e69a30', t))
    L += [ln(250, base - 72 * 1.35, 850, base - 72 * 1.35, GOLD, 3, '6 8', [2, .5]), tx('72', 215, base - 72 * 1.35 + 10, 28, GOLD, [2, .5]),
          ln(250, base - 144 * 1.35, 850, base - 144 * 1.35, '#ff9d9d', 3, '6 8', [4, .3]), tx('144: yetmez', 215, base - 144 * 1.35 + 10, 24, '#ff9d9d', [4, .3], 'end'),
          ln(250, base - 216 * 1.35, 850, base - 216 * 1.35, GOLD, 4, '6 8', [4, 4.8]), tx('216', 215, base - 216 * 1.35 + 10, 30, GOLD, [4, 4.8]),
          tx('12 blok', 400, 898, 30, '#fff', [4, 5.6]), tx('9 blok', 680, 898, 30, '#fff', [4, 5.6])]
    return L

def dia5():
    L = [tx('18 cm’lik kutular', 150, 640, 30, YESIL, [1, .3], 'start'), tx('15 cm’lik kutular', 150, 760, 30, TURUNCU, [1, .4], 'start')]
    for i in range(5): L.append(rc(150 + 144 * i, 655, 141, 64, YESIL, [1, .6 + .15 * i]))
    for i in range(6): L.append(rc(150 + 120 * i, 775, 117, 64, TURUNCU, [1, .8 + .15 * i]))
    for y in (655, 775):
        L += [rc(870, y, 24, 64, '#6b1e24', [3, .3 + (y - 655) / 600], KIRMIZI, 3), tx('3', 882, y - 8, 28, KIRMIZI, [3, .3 + (y - 655) / 600])]
    L += [tx('raf = 90 + 3 = 93 cm', 540, 885, 38, GOLD, [5, .6])]
    return L

def dia6():
    L = [tx('15 cm’lik kutular', 190, 640, 30, YESIL, [1, .3], 'start'), tx('12 cm’lik kutular', 190, 760, 30, TURUNCU, [1, .4], 'start')]
    for i in range(3): L.append(rc(190 + 210 * i, 655, 207, 64, YESIL, [1, .6 + .2 * i]))
    for i in range(4): L.append(rc(190 + 168 * i, 775, 165, 64, TURUNCU, [1, .8 + .2 * i]))
    L += [ln(890, 630, 890, 860, '#fff', 4, '8 8', [1, .3]), tx('raf 50 cm', 890, 618, 28, '#fff', [1, .3])]
    L += [rc(820, 655, 70, 64, '#6b1e24', [3, .3], KIRMIZI, 3), tx('5', 855, 647, 28, KIRMIZI, [3, .3]), rc(862, 775, 28, 64, '#6b1e24', [3, .6], KIRMIZI, 3), tx('2', 876, 767, 28, KIRMIZI, [3, .6])]
    L += [rc(890, 655, 140, 64, 'rgba(246,201,69,.15)', [4, .8], GOLD, 3, 6, '8 6'), tx('+10', 960, 647, 30, GOLD, [4, .8]),
          rc(890, 775, 140, 64, 'rgba(246,201,69,.15)', [4, 1.4], GOLD, 3, 6, '8 6'), tx('+10', 960, 767, 30, GOLD, [4, 1.4])]
    L.append(tx('raf = 60 − 10 = 50 cm', 540, 885, 38, GOLD, [5, .6]))
    return L

def dia7():
    L = [rc(408, 565, 264, 264, 'rgba(255,255,255,.05)', [1, .3], '#cfe8d4', 3, 4, '8 6'), tx('24 cm', 540, 548, 30, '#fff', [2, .3]), tx('24 cm', 335, 705, 30, '#fff', [2, .3])]
    L.append(rc(408, 565, 88, 66, YESIL, [1, .5], '#06210f', 3)); L.append(tx('6 × 8', 395, 600, 28, GOLD, [1, .5], 'end'))
    n = 0
    for r in range(4):
        for c in range(3):
            if r == 0 and c == 0: continue
            L.append(rc(408 + 88 * c, 565 + 66 * r, 88, 66, YESIL if (r + c) % 2 == 0 else '#5fc872', [2, .6 + .25 * n], '#06210f', 3)); n += 1
    L += [tx('4 + 3 = 7 ✗', 165, 700, 32, KIRMIZI, [4, .4]), tx('4 × 3 = 12 ✓', 905, 700, 32, GOLD, [4, 2.4])]
    return L

def dia8():
    L = []
    L += [rc(40, 548, 480, 125, '#0f3a2a', [3, .3], YESIL, 4, 24), tx('BÖLÜYORSAN: EBOB', 280, 600, 38, YESIL, [3, .3]), tx('parçala · eşit böl · en büyük', 280, 648, 23, '#fff', [3, .3]),
          rc(560, 548, 480, 125, '#3a3010', [3, 2.4], GOLD, 4, 24), tx('BULUŞTURUYORSAN: EKOK', 800, 600, 29, GOLD, [3, 2.4]), tx('yan yana diz · buluş · en küçük', 800, 648, 23, '#fff', [3, 2.4])]
    for i, s in enumerate(['1  Başlangıç sayılıyor mu?', '2  Şart var mı?', '3  Boy mu soruldu, adet mi?', '4  Kalan mı var, eksik mi?']):
        y = 690 + i * 56
        L += [rc(60, y, 960, 46, 'rgba(10,50,25,.85)', [4, .3 + 1.15 * i], CY, 3, 16), tx(s, 90, y + 33, 32, '#fff', [4, .3 + 1.15 * i], 'start')]
    return L

# ---- bölümler: (ses = sp(alt) varsayılan; manuel okunuş için (alt, ses))
EP = [
 dict(slug='ekok-01', tur='BAŞLANGIÇ +1', dia=dia1, prev='11 ağaç', hook='Başlangıç dahil mi?', badge='+1', bcol=GOLD,
  s=["Ben Matlemur! Geçen serinin cevabı: 11 ağaç. Yeni seri: EKOK bulundu, peki sonra?",
     "Ormanda iki ateş böceği var: biri 12 saniyede bir, diğeri 18 saniyede bir yanıyor. Şimdi birlikte yandılar.",
     "EKOK 36, yani 36 saniyede bir birlikte yanıyorlar.",
     "Peki sonra? İlk 200 saniyede, şimdiki dahil kaç kez birlikte yanarlar?",
     "200 bölü 36, 5; bunlar sonraki buluşmalar. Şimdiki anı da ekle: 6!",
     "Kural: Süre bölü EKOK sonrakileri verir; başlangıç sayılıyorsa artı 1.",
     "Sıra sende! 8 ve 12 saniyede bir çalan iki zil birlikte çaldı. İlk 100 saniyede, ilk çalış dahil kaç kez birlikte çalar?"],
  prob=['ateş böcekleri: 12 sn ve 18 sn', 'ilk 200 sn, şimdiki dahil?'], ekok=['EKOK(12, 18) = 36', '36 sn’de bir birlikte'],
  calc=['200 ÷ 36 = 5 (kalan 20)', 'sonraki buluşma: 5', 'başlangıç dahil: 5 + 1 = 6'], rule=['SÜRE ÷ EKOK = SONRAKİLER', 'başlangıç sayılıyorsa +1'],
  nextq=['8 ve 12 sn’de çalan zil,', 'ilk 100 sn, ilk çalış dahil,', 'kaç kez birlikte çalar?', 'KAÇ KEZ?']),
 dict(slug='ekok-02', tur='BİRİ GEÇ BAŞLARSA', dia=dia2, prev='5 kez', hook='Dokuz mu?', badge='SAY, SONRA EKOK', bcol=CY,
  s=["Ben Matlemur! Geçen cevap: 5 kez.",
     ("A otobüsü 08:00'den başlayıp 12 dakikada bir, B otobüsü 08:09'dan başlayıp 15 dakikada bir kalkıyor.", "A otobüsü sekizde başlayıp 12 dakikada bir, B otobüsü sekiz sıfır dokuzda başlayıp 15 dakikada bir kalkıyor."),
     "EKOK 60 dakika.",
     ("Peki sonra? İlk birlikte kalkış 09:00 mı?", "Peki sonra? İlk birlikte kalkış dokuz mu?"),
     ("Hayır! Önce say: A 08:00, 08:12, 08:24. B 08:09, 08:24. İlk buluşma 08:24!", "Hayır! Önce say: A sekiz, sekiz on iki, sekiz yirmi dört. B sekiz sıfır dokuz, sekiz yirmi dört. İlk buluşma sekiz yirmi dört!"),
     ("Kural: Biri geç başlıyorsa ilk buluşmayı sayarak bul, sonra EKOK ekle: 09:24, 10:24.", "Kural: Biri geç başlıyorsa ilk buluşmayı sayarak bul, sonra EKOK ekle: dokuz yirmi dört, on yirmi dört."),
     ("Sıra sende! B otobüsü 08:10'da başlasaydı, ilk ne zaman birlikte kalkarlardı?", "Sıra sende! B otobüsü sekiz onda başlasaydı, ilk ne zaman birlikte kalkarlardı?")],
  prob=['A: 08:00, her 12 dk', 'B: 08:09, her 15 dk'], ekok=['EKOK(12, 15) = 60', 'ilk buluşma 09:00 mı?'],
  calc=['A: 08:00  08:12  08:24', 'B: 08:09  08:24', 'ilk buluşma 08:24, sonra +60 dk'], rule=['İLKİNİ SAYARAK BUL', 'sonra EKOK ekle'],
  nextq=['B otobüsü 08:10’da', 'başlasaydı, ilk ne zaman', 'birlikte kalkarlardı?', 'İLK BULUŞMA?']),
 dict(slug='ekok-03', tur='ŞARTLI RAF', dia=dia3, prev='Hiç', hook='Hep EKOK mu?', badge='EKOK’UN KATI', bcol=CY,
  s=["Ben Matlemur! Geçen cevap: hiçbir zaman, çünkü fark EBOB'un katı değil.",
     "24 santimlik ve 40 santimlik kutular, iki ayrı sıra hâlinde uç uca diziliyor. Sıralar eşit uzunlukta olacak.",
     "EKOK 120 santim.",
     "Peki sonra? Raf 4 metre; en uzun sıra kaç santim?",
     "Önce birim: 4 metre, 400 santim. 120 katları: 120, 240, 360, 480. Cevap 360 santim!",
     "Kural: EKOK en kısa ortak boydur. Şart varsa EKOK katlarında gez.",
     "Sıra sende! Aynı kutularla, 5 metreden uzun en kısa eşit sıra kaç santim?"],
  prob=['24 cm ve 40 cm’lik kutular', 'iki sıra eşit uzunlukta'], ekok=['EKOK(24, 40) = 120', 'ortak boy: 120 cm'],
  calc=['4 m = 400 cm', '120, 240, 360, 480…', '400’ü geçmeyen en büyük: 360 cm'], rule=['ŞART VARSA EKOK’UN KATLARI', 'önce birimi eşitle'],
  nextq=['Aynı kutularla 5 m’den', 'uzun en kısa eşit sıra', 'kaç santim?', 'KAÇ CM?']),
 dict(slug='ekok-04', tur='BOY MU, ADET Mİ', dia=dia4, prev='600 cm', hook='Boy mu, adet mi?', badge='ÖNCE ŞART', bcol=CY,
  s=["Ben Matlemur! Geçen cevap: 600 santim.",
     "18 santimlik ve 24 santimlik bloklarla eşit boyda iki kule yapılıyor. Her kule en az 2 metre olacak.",
     "EKOK 72 santim.",
     "Peki sonra? Kaç blok gerekir?",
     "72 katları: 72, 144, 216. 200 santimi geçen ilk boy 216. 216 bölü 18, 12; 216 bölü 24, 9. Toplam 21 blok!",
     "Kural: Önce şartı sağlayan katı bul, sonra adede geç.",
     "Sıra sende! İki kulenin boyları toplamı 6 metreyi geçmeyecekse, bir kule en çok kaç santim olur?"],
  prob=['18 cm ve 24 cm’lik bloklar', 'iki kule eşit boy, en az 2 m'], ekok=['EKOK(18, 24) = 72', 'en az 200 cm → katlara bak'],
  calc=['72, 144, 216 → boy 216 cm', '216 ÷ 18 = 12 blok', '216 ÷ 24 = 9 blok → 21'], rule=['ÖNCE ŞARTI SAĞLAYAN KAT', 'sonra adede geç'],
  nextq=['İki kulenin boyları toplamı', '6 m’yi geçmesin,', 'bir kule en çok?', 'KAÇ CM?']),
 dict(slug='ekok-05', tur='BOŞLUK AYNI', dia=dia5, prev='288 cm', hook='Raf 90 mı?', badge='KALAN: +', bcol=TURUNCU,
  s=["Ben Matlemur! Geçen cevap: 288 santim.",
     "Bir rafa 18 santimlik kutular dizilince 3 santim boşluk kalıyor. 15 santimlik kutular dizilince de yine 3 santim.",
     "EKOK 90 santim.",
     "Peki sonra? Raf 90 santim mi?",
     "Hayır! Boşluğu at: raf eksi 3, 90'ın katı olmalı. Raf: 93, 183, 273!",
     "Kural: Kalanlar aynıysa EKOK katına kalanı ekle.",
     "Sıra sende! 12'ye ve 15'e bölününce 4 kalanını veren en büyük 3 basamaklı sayı kaç?"],
  prob=['18 cm’lik kutuyla 3 cm boşluk', '15 cm’lik kutuyla 3 cm boşluk'], ekok=['EKOK(18, 15) = 90', 'raf 90 mı?'],
  calc=['boşluğu at: raf − 3 = 90’ın katı', 'raf = 90k + 3', '93, 183, 273…'], rule=['KALANLAR AYNI → EKOK + KALAN', 'boşluğu at, katını al, geri ekle'],
  nextq=['12’ye ve 15’e bölününce', '4 kalan veren en büyük', '3 basamaklı sayı?', 'KAÇ?']),
 dict(slug='ekok-06', tur='EKSİK AYNI', dia=dia6, prev='964', hook='Hangisini ekleyeceğim?', badge='EKSİK: −', bcol=PEMBE,
  s=["Ben Matlemur! Geçen cevap: 964.",
     "Bu rafta 15 santimlik kutularla 5 santim, 12 santimlik kutularla 2 santim boşluk kalıyor.",
     "EKOK 60 santim.",
     "Peki sonra? Kalanlar farklı; hangisini ekleyeceğim?",
     "Hiçbirini! Eksiğe bak: 15 eksi 5, 10. 12 eksi 2, yine 10. Raf 10 santim uzun olsa ikisi de tam dolardı.",
     "Kural: Eksikler aynıysa EKOK katından eksiği çıkar: 50, 110, 170.",
     "Sıra sende! 12'ye bölününce 11, 15'e bölününce 14 kalanını veren en küçük 3 basamaklı sayı kaç?"],
  prob=['15 cm’lik kutuyla 5 cm boşluk', '12 cm’lik kutuyla 2 cm boşluk'], ekok=['EKOK(15, 12) = 60', 'kalanlar farklı!'],
  calc=['15 − 5 = 10 ve 12 − 2 = 10', 'raf + 10 = 60’ın katı', 'raf = 50, 110, 170…'], rule=['EKSİKLER AYNI → EKOK − EKSİK', 'katını al, eksiği çıkar'],
  nextq=['12’ye bölününce 11,', '15’e bölününce 14 kalan,', 'en küçük 3 basamaklı?', 'KAÇ?']),
 dict(slug='ekok-07', tur='KARE VE FAYANS', dia=dia7, prev='119', hook='4 + 3 = 7 mi?', badge='ÇARP!', bcol=YESIL,
  s=["Ben Matlemur! Geçen cevap: 119.",
     "Kenarları 6 ve 8 santim olan dikdörtgen fayanslarla en küçük kare yapılacak.",
     "EKOK 24; karenin kenarı 24 santim.",
     "Peki sonra? Kaç fayans: 4 artı 3, 7 mi?",
     "Hayır! Bir kenara 4, diğer kenara 3 fayans sığar. 4 çarpı 3, 12 fayans!",
     "Kural: Uç uca sırada adetleri topla, kare gibi alanda çarp.",
     "Sıra sende! 12 ve 18 dişli iki çarkta işaretli dişler yan yana. Yeniden yan yana gelmeleri için küçük çark en az kaç tur atar?"],
  prob=['6 × 8 cm’lik fayanslarla', 'en küçük kare yapılacak'], ekok=['EKOK(6, 8) = 24', 'kare kenarı 24 cm'],
  calc=['24 ÷ 6 = 4  ve  24 ÷ 8 = 3', '4 + 3 = 7 değil!', '4 × 3 = 12 fayans'], rule=['KARE / ALAN → ÇARP', 'uç uca sıra → topla'],
  nextq=['12 ve 18 dişli çark,', 'yeniden yan yana için', 'küçük çark en az kaç tur?', 'KAÇ TUR?']),
 dict(slug='ekok-08', tur='REHBER', dia=dia8, prev='3 tur', hook='Kontrol listesi?', badge='KONTROL', bcol=GOLD,
  s=["Ben Matlemur! Geçen cevap: küçük çark 3 tur, büyük çark 2 tur.",
     "Bugün rehber günü: EBOB mu, EKOK mu?",
     "Büyük bir şeyi eş parçalara bölüyorsan EBOB. Küçük şeyleri biriktirip buluşturuyorsan EKOK.",
     "Peki sonra? EKOK'u bulunca 4 soru sor.",
     "Başlangıç sayılıyor mu? Şart var mı? Boy mu adet mi? Kalan mı eksik mi?",
     "Kontrol: EBOB çarpı EKOK, iki sayının çarpımıdır. 12 ve 18 için 6 çarpı 36, 216.",
     "Sıra sende! 8 ile 15'in EBOB'u 1. Peki EKOK'u kaç?"],
  prob=[], ekok=[], calc=[], rule=['EBOB × EKOK = a × b', '6 × 36 = 12 × 18 = 216'],
  nextq=['8 ile 15’in EBOB’u 1.', 'EKOK’u kaç?', '', 'EKOK = ?']),
]

ORTA = r"""
const YESIL='#7be08a', TURUNCU='#ffb347', KIRMIZI='#ff6b6b', PEMBE='#ff8fa3', BC=CFG.bcol;
const dG=el('g',{opacity:0}); const DE=[];
(CFG.dia||[]).forEach(e=>{const g=el('g',{opacity:0},dG); const a=e.a;
  if(e.k==='text')T(a.txt,a.x,a.y,a.size||40,a.fill||WH,a.extra||{},g); else el(e.k,a,g);
  DE.push({g,t:e.t,h:e.h||null})});
function mkText(lines,x,y0,dy,size,fill,extra){const g=el('g',{opacity:0}); const arr=[]; lines.forEach((s,i)=>{arr.push(TF(s,x,y0+i*dy,size,Array.isArray(fill)?fill[i]:fill,960,extra||{},g))}); return {g,arr}}
const prevG=el('g',{opacity:0}); T('GEÇEN CEVAP',540,975,40,CY,{'letter-spacing':8},prevG); T(CFG.prev||'',540,1075,110,GOLD,{filter:'url(#glow)'},prevG);
const hookQ=el('g',{opacity:0}); TF(CFG.hook,540,1085,80,BC,960,{filter:'url(#glow)'},hookQ);
const PB=mkText(CFG.prob,540,975,70,46,WH,{}), EB=mkText(CFG.ekok,540,1000,80,62,[GOLD,CY],{filter:'url(#glow)'});
const CL=mkText(CFG.calc,540,960,66,46,[WH,WH,GOLD],{}); const calcEl=CL.arr;
const rG=el('g',{opacity:0}); el('rect',{x:50,y:920,width:980,height:230,rx:40,fill:'rgba(10,50,25,.85)',stroke:BC,'stroke-width':7},rG);
TF(CFG.badge||'',540,1005,86,BC,900,{filter:'url(#glow)','font-weight':900},rG); TF((CFG.rule||[])[0]||'',540,1075,46,WH,940,{},rG); TF((CFG.rule||[])[1]||'',540,1125,44,CY,940,{},rG);
const nG=el('g',{opacity:0}); el('rect',{x:60,y:560,width:960,height:510,rx:46,fill:'rgba(10,50,25,.85)',stroke:GOLD,'stroke-width':6},nG);
T('SIRA SENDE',540,635,44,GOLD,{'letter-spacing':10},nG); CFG.nextq.forEach((s,i)=>{if(s)TF(s,540,715+i*76,i===3?72:54,i===3?CY:WH,900,i===3?{filter:'url(#glow)'}:{},nG)});
"""
CONTENT = r"""
function content(t){
 const fin=ramp(t,B[6]-.05,B[6]+.4), fo=1-fin;
 dG.setAttribute('opacity',ramp(t,B[1]-.1,B[1]+.3)*fo);
 DE.forEach(d=>{const s=B[d.t[0]]+d.t[1]; let a=ramp(t,s,s+.25); if(d.h){const e=B[d.h[0]]+d.h[1]; a*=1-ramp(t,e,e+.25)} d.g.setAttribute('opacity',a)});
 const pv=ramp(t,B[0]+.2,B[0]+.6)*(1-ramp(t,B[1]-.2,B[1]+.1)); setT(prevG,pv,.9+.1*back(ramp(t,B[0]+.2,B[0]+.7)),540,1030);
 const pb=ramp(t,B[1]+.1,B[1]+.5)*(1-ramp(t,B[2]-.1,B[2]+.2)); setT(PB.g,pb,1,540,1000);
 const eb=ramp(t,B[2]+.1,B[2]+.5)*(1-ramp(t,B[3]-.1,B[3]+.2)); setT(EB.g,eb,.9+.1*back(ramp(t,B[2]+.1,B[2]+.6)),540,1030);
 const hq=ramp(t,B[3]+.1,B[3]+.5)*(1-ramp(t,B[4]-.1,B[4]+.2)); setT(hookQ,hq,.85+.15*back(ramp(t,B[3]+.1,B[3]+.6)),540,1060);
 const cv=ramp(t,B[4]+.1,B[4]+.4)*(1-ramp(t,B[5]-.05,B[5]+.25)); CL.g.setAttribute('opacity',cv);
 calcEl.forEach((e,i)=>{const s=B[4]+.2+i*(B[5]-B[4]-.6)/3; e.setAttribute('opacity',ramp(t,s,s+.3))});
 const ru=ramp(t,B[5]+.1,B[5]+.6)*fo; setT(rG,ru,.9+.1*back(ramp(t,B[5]+.1,B[5]+.6)),540,1035);
 setT(nG,fin,.9+.1*back(fin),540,815);
}
"""
JS_K = E.ON + ORTA + E.ARA + CONTENT + E.SON

def tanim(e, no):
    alt = [x[0] if isinstance(x, tuple) else x for x in e['s']]
    ses = [x[1] if isinstance(x, tuple) else sp(x) for x in e['s']]
    b, end = MU.beats(ses)
    cfg = dict(kind='ekok', accent=GOLD, title='EKOK BULUNDU, PEKİ SONRA?', label=f'BÖLÜM {no} • {e["tur"]}', beats=b, end=end, cta=round(b[-1] + .6, 2), subs=alt,
               dia=e['dia'](), prev=e['prev'], hook=e['hook'], badge=e['badge'], bcol=e['bcol'], prob=e['prob'], ekok=e['ekok'], calc=e['calc'], rule=e['rule'], nextq=e['nextq'],
               bursts=[[b[5] + .3, 540, 800, e['bcol']]], rings=[[b[5] + .3, e['bcol'], 800]])
    nxt = 'Cevap sonraki videoda!' if no < 8 else 'Cevabı yoruma yaz!'
    cap = (f"EKOK BULUNDU, PEKİ SONRA? 🔁 (Bölüm {no}: {e['tur'].title()})\n\n" + ' · '.join(x for x in e['calc'] if x) + f"\n\nKural: {' — '.join(e['rule'])}\n\n"
           + 'SIRA SENDE: ' + ' '.join(x for x in e['nextq'] if x) + f' {nxt}\n\nKaydet, LGS matematik için lazım olur 📌\n\nHer gün matematik için takip et 👆')
    return e['slug'], f'EKOK tuzağı {no}: {e["tur"].title()}', cfg, ses, cap

def sahne_html(cfg):
    MU.JS = JS_K
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
    sfx += [{'t': round(b[3] + .15, 2), 'tip': 'pop', 'g': .6}, {'t': round(b[4] + .2, 2), 'tip': 'tick', 'g': .5}, {'t': round(b[5] + .3, 2), 'tip': 'ding', 'g': .55},
            {'t': round(cfg['cta'] + .2, 2), 'tip': 'sparkle', 'g': .6}, {'t': round(cfg['cta'] + .6, 2), 'tip': 'pop', 'g': .6}]
    sfx.sort(key=lambda e: e['t'])
    uzun = [m for m in K.MUZ if float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{R}/kutuphane/muzik/{m}']).decode()) >= 80]
    no = int(slug.split('-')[1])
    json.dump({'sure': cfg['end'], 'bpm': 128, 'sfx': sfx, 'sahne_basi': b, 'sahne_sonu': cfg['end'],
               'muzik_dosya': 'kutuphane/muzik/' + uzun[(no + 5) % len(uzun)], 'muzik_baslangic': 6}, open(d + '/ses.json', 'w', encoding='utf-8'), ensure_ascii=False)
    pj = f'{d}/post.json'; old = json.load(open(pj)) if os.path.exists(pj) else {}
    post = {'baslik': baslik, 'tur': 'özgün', 'sure': 60, 'fps': 30, 'caption': cap, 'hashtagler': ETIKET,
            'kaynak': 'EKOK tuzakları serisi (konu planı kullanıcı + Fable incelemesi; sayılar ve anlatım özgün Mathlemur)',
            'durum': old['durum'] if old.get('durum') in ('taslak', 'onay-bekliyor') else 'taslak', 'ana_izgara': False,
            'kayit': old.get('kayit', []) + ['EKOK serisi taslağı üretildi (Paket 1; yayın zamanı onaydan sonra)']}
    json.dump(post, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); open(pj, 'a').write('\n')
    return slug

if __name__ == '__main__':
    secim = set(sys.argv[1:])
    for no, e in enumerate(EP, 1):
        if secim and e['slug'] not in secim: continue
        v = tanim(e, no); print(yaz(*v), 'end=', v[2]['end'], 'beats=', v[2]['beats'])
