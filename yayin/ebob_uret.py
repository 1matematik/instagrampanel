#!/usr/bin/env python3
"""EBOB hesaplandı, peki sonra? +1 mi, -1 mi? serisi (7 video, zincirli: geçen cevap + yeni soru). 25 Kas kararı.
Fikir: kullanıcının gösterdiği başka hesap karuseli (yalnızca konu/tuzak tipleri); sayılar, tasarım, anlatım bizim (Mathlemur, orman).
Kullanım: python3 yayin/ebob_uret.py [ebob-01 ...]   → icerik/ebob-NN/{sahne.html, ses.json, ses/metin.txt, post.json}"""
import os, sys, json, math, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import kok_uret as K
import mufredat_uret as MU

R = K.R
soz = K.soz
GOLD, CY, KIRMIZI, YESIL, TURUNCU, PEMBE = '#f6c945', '#6ee7ff', '#ff6b6b', '#7be08a', '#ffb347', '#ff8fa3'
ETIKET = ['ebob', 'lgsmatematik', 'matematik', 'tuzak', 'keşfet']

def along(V, step, closed=False, ends=True):
    """V köşe listesi boyunca eşit adımla nokta; kapalıysa başlangıç tekrarlanmaz."""
    P = V + ([V[0]] if closed else [])
    seg = [math.dist(P[i], P[i+1]) for i in range(len(P)-1)]; tot = sum(seg); out = []
    n = int(round(tot / step)); lo, hi = (0, n - (1 if closed else 0)) if ends else (1, n - 1)
    for k in range(lo, hi + 1):
        d = k * step; i = 0
        while i < len(seg) - 1 and d > sum(seg[:i+1]) + 1e-6: i += 1
        c = d - sum(seg[:i]); t = c / seg[i]
        out.append([round(P[i][0] + (P[i+1][0]-P[i][0])*t, 1), round(P[i][1] + (P[i+1][1]-P[i][1])*t, 1)])
    return out

def geo_loop():
    x0, y0, W, H = 277, 545, 525, 300
    V = [[x0, y0+H], [x0, y0], [x0+W, y0], [x0+W, y0+H]]
    return dict(lines=[dict(pts=V, closed=True)], pts=along(V, 75, True), kind='tree', ends=[[x0, y0+H]], endx=False,
                labels=[[x0+W/2, y0-34, '84 m', 40, '#fff'], [x0+W+60, y0+H/2, '48 m', 40, '#fff'], [x0-10, y0+H+44, 'BAŞLANGIÇ', 28, GOLD]])

def geo_grid():
    x0, y0 = 290, 545; pts = [[x0+100*c, y0+100*r] for r in range(4) for c in range(6)]
    L = [dict(pts=[[x0, y0+100*r], [x0+500, y0+100*r]]) for r in range(4)] + [dict(pts=[[x0+100*c, y0], [x0+100*c, y0+300]]) for c in range(6)]
    return dict(lines=L, pts=pts, kind='tree', ends=[[x0, y0], [x0+500, y0], [x0, y0+300], [x0+500, y0+300]], endx=False,
                labels=[[x0+250, y0-34, '90 m', 40, '#fff'], [x0+560, y0+150, '54 m', 40, '#fff']])

def geo_L():
    cx, cy = 360, 545; A = [cx+360, cy]; B = [cx, cy+300]
    pts = [[cx, cy]] + along([[cx, cy], A], 60, False, True)[1:] + along([[cx, cy], B], 60, False, True)[1:]
    return dict(lines=[dict(pts=[A, [cx, cy], B])], pts=pts, kind='tree', ends=[[cx, cy]], endx=False,
                labels=[[cx+180, cy-36, '72 m', 40, '#fff'], [cx-70, cy+150, '60 m', 40, '#fff'], [cx-10, cy-52, 'ORTAK KÖŞE', 26, GOLD]])

def geo_two():
    a = [[246, 610], [834, 610]]; b = [[162, 780], [918, 780]]
    return dict(lines=[dict(pts=a), dict(pts=b)], pts=along(a, 84) + along(b, 84), kind='tree', ends=a + b, endx=False,
                labels=[[540, 566, '84 m', 40, '#fff'], [540, 736, '108 m', 40, '#fff']])

def geo_cut():
    a = [[180, 610], [900, 610]]; b = [[90, 780], [990, 780]]
    return dict(lines=[dict(pts=a, wood=True), dict(pts=b, wood=True)], pts=along(a, 180, False, False) + along(b, 180, False, False), kind='cut',
                ends=a + b, endx=True, labels=[[540, 556, '120 cm', 40, '#fff'], [540, 726, '150 cm', 40, '#fff']])

def geo_route():
    A, B, C = [70, 720], [352, 720], [1010, 720]
    return dict(lines=[dict(pts=[A, C])], pts=along([A, C], 94, False, False), kind='pin', ends=[A, C], endx=True,
                labels=[[70, 790, 'A', 46, GOLD], [352, 790, 'B', 46, GOLD], [1010 - 5, 790, 'C', 46, GOLD], [211, 660, '180 km', 36, '#fff'], [681, 660, '420 km', 36, '#fff']])

EP = [
 dict(slug='ebob-01', tur='ÇEVREYE AĞAÇ', geo=geo_loop, counter='ağaç', badge='+1 YOK', bcol=KIRMIZI,
  ses=["Ben Matlemur! EBOB hesaplandı, peki sonra? Bir fazlası mı, bir eksiği mi? Bu serinin tuzağı bu!",
       f"{soz(84)} metreye {soz(48)} metre bir bahçenin çevresine eşit aralıkla ağaç dikiyoruz. Köşelere de ağaç gelecek.",
       f"EBOB {soz(84)}, {soz(48)}, {soz(12)}. Aralık {soz(12)} metre!",
       "Peki sonra? Bir fazlası mı, bir eksiği mi?",
       f"Çevre {soz(264)}. Bölü {soz(12)}, {soz(22)} aralık. Başladığın yere dönüyorsun, ilk ve son ağaç aynı. Artı bir yok! {soz(22)} ağaç.",
       "Kural: çevreye dikiyorsan ve başladığın yere dönüyorsan, artı bir yok!",
       f"Sıra sende! {soz(90)} metreye {soz(54)} metre tarlayı en büyük karelere ayırıp köşelere ağaç dikiyoruz. Kaç ağaç?"],
  prob=['84 m × 48 m bahçenin çevresine', 'eşit aralıkla ağaç, köşelere de!'], ebob=['EBOB(84, 48) = 12', 'aralık = 12 m'],
  calc=['çevre = 2 × (84 + 48) = 264', '264 ÷ 12 = 22 aralık', 'başa dönüyor → 22 ağaç'], rule=['ÇEVRE + BAŞA DÖNÜŞ', 'ilk ağaç = son ağaç'],
  nextq=['90 m × 54 m tarla,', 'en büyük karelere ayrılıyor,', 'köşelere ağaç dikiliyor.', 'KAÇ AĞAÇ?'], prev=None, ans='22 ağaç'),
 dict(slug='ebob-02', tur='KARELERE AYIR', geo=geo_grid, counter='ağaç', badge='2 YANA +1', bcol=YESIL,
  ses=["Ben Matlemur! Geçen cevap, yirmi iki ağaç. Artı bir yoktu!",
       f"{soz(90)} metreye {soz(54)} metre tarla, en büyük karelere ayrılıyor. Her karenin köşesine ağaç dikiliyor.",
       f"EBOB {soz(90)}, {soz(54)}, {soz(18)}. Kare kenarı {soz(18)} metre!",
       "Peki sonra? Bir fazlası mı, bir eksiği mi?",
       f"{soz(90)} bölü {soz(18)}, {soz(5)} kare. {soz(54)} bölü {soz(18)}, {soz(3)} kare. Her satırın başında ve sonunda ağaç var: {soz(5)} artı bir çarpı {soz(3)} artı bir, {soz(24)} ağaç!",
       "Kural: karelere ayırıp köşelere dikiyorsan, iki yana da artı bir!",
       f"Sıra sende! Köşesi ortak, {soz(72)} ve {soz(60)} metrelik iki yola eşit aralıkla ağaç dikiyoruz. Kaç ağaç?"],
  prob=['90 m × 54 m tarla, en büyük', 'karelere ayrılıyor, köşelere ağaç!'], ebob=['EBOB(90, 54) = 18', 'kare kenarı = 18 m'],
  calc=['90 ÷ 18 = 5 kare, 54 ÷ 18 = 3 kare', '(5 + 1) × (3 + 1)', '6 × 4 = 24 ağaç'], rule=['KARELERE AYIR + KÖŞELERE DİK', 'iki yana da +1'],
  nextq=['Köşesi ortak iki yol:', '72 m ve 60 m,', 'eşit aralıkla ağaç.', 'KAÇ AĞAÇ?'], prev='22 ağaç', ans='24 ağaç'),
 dict(slug='ebob-03', tur='ORTAK KÖŞE', geo=geo_L, counter='ağaç', badge='BİR KEZ +1', bcol=CY,
  ses=["Ben Matlemur! Geçen cevap, yirmi dört ağaç. İki yana da artı bir!",
       f"Köşesi ortak iki yol var: {soz(72)} metre ve {soz(60)} metre. Ortak köşeye de ağaç dikilecek.",
       f"EBOB {soz(72)}, {soz(60)}, {soz(12)}. Aralık {soz(12)} metre!",
       "Peki sonra? Bir fazlası mı, bir eksiği mi?",
       f"{soz(72)} bölü {soz(12)}, {soz(6)} aralık. {soz(60)} bölü {soz(12)}, {soz(5)} aralık. {soz(6)} artı {soz(5)}, artı ortak köşe için bir, {soz(12)} ağaç!",
       "Kural: ortak köşe tek, o yüzden sadece bir kez artı bir!",
       f"Sıra sende! Bağımsız iki yol, {soz(84)} metre ve {soz(108)} metre. Başlarına ve sonlarına ağaç dikiyoruz. Kaç ağaç?"],
  prob=['köşesi ortak iki yol: 72 m, 60 m', 'ortak köşeye de ağaç!'], ebob=['EBOB(72, 60) = 12', 'aralık = 12 m'],
  calc=['72 ÷ 12 = 6, 60 ÷ 12 = 5 aralık', '6 + 5 + 1 (ortak köşe)', '= 12 ağaç'], rule=['ORTAK KÖŞE TEK', 'sadece 1 kez +1'],
  nextq=['Bağımsız iki yol:', '84 m ve 108 m,', 'başa ve sona ağaç.', 'KAÇ AĞAÇ?'], prev='24 ağaç', ans='12 ağaç'),
 dict(slug='ebob-04', tur='BAĞIMSIZ YOLLAR', geo=geo_two, counter='ağaç', badge='HER YOLA +1', bcol=TURUNCU,
  ses=["Ben Matlemur! Geçen cevap, on iki ağaç. Ortak köşeye bir kez artı bir!",
       f"İki bağımsız yol var: {soz(84)} metre ve {soz(108)} metre. İkisinin de başına ve sonuna ağaç dikilecek.",
       f"EBOB {soz(84)}, {soz(108)}, {soz(12)}. Aralık {soz(12)} metre!",
       "Peki sonra? Bir fazlası mı, bir eksiği mi?",
       f"{soz(84)} bölü {soz(12)}, {soz(7)} aralık, {soz(7)} artı bir, {soz(8)} ağaç. {soz(108)} bölü {soz(12)}, {soz(9)} aralık, {soz(9)} artı bir, {soz(10)} ağaç. Toplam {soz(18)}!",
       "Kural: yollar bağımsızsa, her yola ayrı artı bir!",
       f"Sıra sende! {soz(120)} santimetre ve {soz(150)} santimetrelik iki tel, en uzun eşit parçalara kesiliyor. En az kaç kesim?"],
  prob=['iki bağımsız yol: 84 m, 108 m', 'başlarına ve sonlarına ağaç!'], ebob=['EBOB(84, 108) = 12', 'aralık = 12 m'],
  calc=['84 ÷ 12 = 7 → 7 + 1 = 8 ağaç', '108 ÷ 12 = 9 → 9 + 1 = 10 ağaç', '8 + 10 = 18 ağaç'], rule=['YOLLAR BAĞIMSIZ', 'her yola ayrı +1'],
  nextq=['120 cm ve 150 cm tel,', 'eşit en uzun parçalara', 'kesiliyor.', 'EN AZ KAÇ KESİM?'], prev='12 ağaç', ans='18 ağaç'),
 dict(slug='ebob-05', tur='KESME İŞLEMİ', geo=geo_cut, counter='kesim', badge='−1', bcol=PEMBE,
  ses=["Ben Matlemur! Geçen cevap, on sekiz ağaç. Her yola ayrı artı bir!",
       f"{soz(120)} santimetre ve {soz(150)} santimetrelik iki tel, en uzun eşit parçalara kesilecek. Kaç kesim gerekir?",
       f"EBOB {soz(120)}, {soz(150)}, {soz(30)}. Parça uzunluğu {soz(30)} santimetre!",
       "Peki sonra? Bir fazlası mı, bir eksiği mi?",
       f"{soz(120)} bölü {soz(30)}, {soz(4)} parça, {soz(3)} kesim. {soz(150)} bölü {soz(30)}, {soz(5)} parça, {soz(4)} kesim. {soz(3)} artı {soz(4)}, {soz(7)} kesim!",
       "Kural: kesimde eksi bir! Kesim sayısı, parça sayısından bir eksik!",
       f"Sıra sende! A şehrinden B'ye {soz(180)} kilometre, B'den C'ye {soz(420)} kilometre. Eşit aralıkla mola veriliyor, B'de de mola var. En az kaç mola?"],
  prob=['120 cm ve 150 cm tel,', 'en uzun eşit parçalara kesiliyor'], ebob=['EBOB(120, 150) = 30', 'parça = 30 cm'],
  calc=['120 ÷ 30 = 4 parça → 3 kesim', '150 ÷ 30 = 5 parça → 4 kesim', '3 + 4 = 7 kesim'], rule=['KESİM = PARÇA − 1', 'her telde −1'],
  nextq=['A → B: 180 km, B → C: 420 km', 'eşit aralıkla mola,', 'B’de de mola var.', 'EN AZ KAÇ MOLA?'], prev='18 ağaç', ans='7 kesim'),
 dict(slug='ebob-06', tur='MOLA / SON DURAK', geo=geo_route, counter='mola', badge='−1', bcol=PEMBE,
  ses=["Ben Matlemur! Geçen cevap, yedi kesim. Kesimde eksi bir!",
       f"A'dan B'ye {soz(180)} kilometre, B'den C'ye {soz(420)} kilometre. Eşit mesafelerde mola veriliyor, B'de de mola var.",
       f"EBOB {soz(180)}, {soz(420)}, {soz(60)}. Mola aralığı {soz(60)} kilometre!",
       "Peki sonra? Bir fazlası mı, bir eksiği mi?",
       f"Toplam {soz(600)} kilometre, bölü {soz(60)}, {soz(10)} aralık. Yolun başında ve varışta mola verilmez. {soz(10)} eksi bir, {soz(9)} mola!",
       "Kural: başlangıçta ve son durakta mola yok, eksi bir!",
       "Sıra sende! Bir sonraki videoda bütün tuzakları tek tabloda topluyoruz. Kaydet ve takip et!"],
  prob=['A → B: 180 km, B → C: 420 km', 'eşit aralıkla mola, B’de de mola'], ebob=['EBOB(180, 420) = 60', 'mola aralığı = 60 km'],
  calc=['toplam yol = 600 km', '600 ÷ 60 = 10 aralık', 'başta ve sonda mola yok → 9 mola'], rule=['BAŞTA VE SONDA MOLA YOK', 'aralık − 1'],
  nextq=['Bir sonraki videoda', 'bütün tuzaklar', 'TEK TABLODA!', ''], prev='7 kesim', ans='9 mola'),
 dict(slug='ebob-07', tur='REHBER', geo=None, counter='', badge='', bcol=GOLD,
  ses=["Ben Matlemur! Geçen cevap, dokuz mola. Şimdi bütün tuzakları tek tabloda toplayalım!",
       "Çevreye dikiyorsan ve başladığın yere dönüyorsan: artı bir yok.",
       "Karelere ayırıp köşelere dikiyorsan: iki yana da artı bir. Ortak köşeli iki yolda: sadece bir kez artı bir.",
       "Bağımsız iki yolda: her yola ayrı artı bir.",
       "Kesme ve mola sorularında: eksi bir!",
       "Püf nokta: kaç ayrı başlangıç ve bitiş noktası var, ona bak! Ezberleme, mantığını kur!",
       f"Sıra sende! {soz(100)} metrelik düz bir yola {soz(10)} metre aralıkla, başına ve sonuna da ağaç dikiliyor. Kaç ağaç? Yoruma yaz!"],
  prob=[], ebob=[], calc=[], rule=['KAÇ AYRI BAŞLANGIÇ–BİTİŞ?', 'ona bak!'], nextq=['100 m düz yol,', '10 m aralık,', 'başa ve sona da ağaç.', 'KAÇ AĞAÇ?'], prev='9 mola', ans='11 ağaç'),
]
REHBER = [['Çevre, başa dönüş', '+1 YOK', KIRMIZI], ['Karelere ayır, köşelere dik', '2 YANA +1', YESIL], ['Ortak köşeli iki yol', 'BİR KEZ +1', CY],
          ['Bağımsız iki yol', 'HER YOLA +1', TURUNCU], ['Kesme işlemi', '−1', PEMBE], ['Mola, son durak', '−1', PEMBE]]

def tanim(e, no):
    alt = [s for s in e['ses']]
    # altyazı: sayıları rakamla yaz (kısaltılmış el yapımı)
    A = {
     1: ["Ben Matlemur! EBOB hesaplandı, peki sonra? 1 fazlası mı, 1 eksiği mi? Bu serinin tuzağı bu!", "84 m × 48 m bahçenin çevresine eşit aralıkla ağaç dikiyoruz. Köşelere de ağaç gelecek.", "EBOB(84, 48) = 12. Aralık 12 metre!", "Peki sonra? 1 fazlası mı, 1 eksiği mi?", "Çevre 264. ÷ 12 = 22 aralık. Başladığın yere dönüyorsun, ilk ve son ağaç aynı. +1 yok! 22 ağaç.", "Kural: çevreye dikiyorsan ve başladığın yere dönüyorsan, +1 yok!", "Sıra sende! 90 m × 54 m tarlayı en büyük karelere ayırıp köşelere ağaç dikiyoruz. Kaç ağaç?"],
     2: ["Ben Matlemur! Geçen cevap, 22 ağaç. +1 yoktu!", "90 m × 54 m tarla en büyük karelere ayrılıyor. Her karenin köşesine ağaç dikiliyor.", "EBOB(90, 54) = 18. Kare kenarı 18 m!", "Peki sonra? 1 fazlası mı, 1 eksiği mi?", "90 ÷ 18 = 5 kare, 54 ÷ 18 = 3 kare. Her satırın başında ve sonunda ağaç var: (5+1) × (3+1) = 24 ağaç!", "Kural: karelere ayırıp köşelere dikiyorsan, iki yana da +1!", "Sıra sende! Köşesi ortak, 72 m ve 60 m'lik iki yola eşit aralıkla ağaç dikiyoruz. Kaç ağaç?"],
     3: ["Ben Matlemur! Geçen cevap, 24 ağaç. İki yana da +1!", "Köşesi ortak iki yol var: 72 m ve 60 m. Ortak köşeye de ağaç dikilecek.", "EBOB(72, 60) = 12. Aralık 12 m!", "Peki sonra? 1 fazlası mı, 1 eksiği mi?", "72 ÷ 12 = 6 aralık. 60 ÷ 12 = 5 aralık. 6 + 5 + ortak köşe için 1 = 12 ağaç!", "Kural: ortak köşe tek, o yüzden sadece bir kez +1!", "Sıra sende! Bağımsız iki yol, 84 m ve 108 m. Başlarına ve sonlarına ağaç dikiyoruz. Kaç ağaç?"],
     4: ["Ben Matlemur! Geçen cevap, 12 ağaç. Ortak köşeye bir kez +1!", "İki bağımsız yol var: 84 m ve 108 m. İkisinin de başına ve sonuna ağaç dikilecek.", "EBOB(84, 108) = 12. Aralık 12 m!", "Peki sonra? 1 fazlası mı, 1 eksiği mi?", "84 ÷ 12 = 7 aralık, 7 + 1 = 8 ağaç. 108 ÷ 12 = 9 aralık, 9 + 1 = 10 ağaç. Toplam 18!", "Kural: yollar bağımsızsa, her yola ayrı +1!", "Sıra sende! 120 cm ve 150 cm'lik iki tel, en uzun eşit parçalara kesiliyor. En az kaç kesim?"],
     5: ["Ben Matlemur! Geçen cevap, 18 ağaç. Her yola ayrı +1!", "120 cm ve 150 cm'lik iki tel, en uzun eşit parçalara kesilecek. Kaç kesim gerekir?", "EBOB(120, 150) = 30. Parça uzunluğu 30 cm!", "Peki sonra? 1 fazlası mı, 1 eksiği mi?", "120 ÷ 30 = 4 parça, 3 kesim. 150 ÷ 30 = 5 parça, 4 kesim. 3 + 4 = 7 kesim!", "Kural: kesimde −1! Kesim sayısı, parça sayısından bir eksik!", "Sıra sende! A'dan B'ye 180 km, B'den C'ye 420 km. Eşit aralıkla mola veriliyor, B'de de mola var. En az kaç mola?"],
     6: ["Ben Matlemur! Geçen cevap, 7 kesim. Kesimde −1!", "A'dan B'ye 180 km, B'den C'ye 420 km. Eşit mesafelerde mola veriliyor, B'de de mola var.", "EBOB(180, 420) = 60. Mola aralığı 60 km!", "Peki sonra? 1 fazlası mı, 1 eksiği mi?", "Toplam 600 km, ÷ 60 = 10 aralık. Yolun başında ve varışta mola verilmez. 10 − 1 = 9 mola!", "Kural: başlangıçta ve son durakta mola yok, −1!", "Sıra sende! Bir sonraki videoda bütün tuzakları tek tabloda topluyoruz. Kaydet ve takip et!"],
     7: ["Ben Matlemur! Geçen cevap, 9 mola. Şimdi bütün tuzakları tek tabloda toplayalım!", "Çevreye dikiyorsan ve başladığın yere dönüyorsan: +1 yok.", "Karelere ayırıp köşelere dikiyorsan: iki yana da +1. Ortak köşeli iki yolda: sadece bir kez +1.", "Bağımsız iki yolda: her yola ayrı +1.", "Kesme ve mola sorularında: −1!", "Püf nokta: kaç ayrı başlangıç ve bitiş noktası var, ona bak! Ezberleme, mantığını kur!", "Sıra sende! 100 m'lik düz bir yola 10 m aralıkla, başına ve sonuna da ağaç dikiliyor. Kaç ağaç? Yoruma yaz!"],
    }[no]
    b, end = MU.beats(e['ses'])
    g = e['geo']() if e['geo'] else None
    cfg = dict(kind='ebob' if g else 'rehber', accent=GOLD, title='EBOB HESAPLANDI, PEKİ SONRA?', label=f'BÖLÜM {no} • {e["tur"]}', beats=b, end=end, cta=round(b[-1] + .6, 2), subs=A,
               geo=g, counter=e['counter'], badge=e['badge'], bcol=e['bcol'], prob=e['prob'], ebob=e['ebob'], calc=e['calc'], rule=e['rule'], nextq=e['nextq'], prev=e['prev'], ans=e['ans'],
               rehber=REHBER, bursts=[[b[5] + .3, 540, 800, e['bcol']]], rings=[[b[5] + .3, e['bcol'], 800]])
    nxt = 'Cevap sonraki videoda!' if no < 7 else 'Cevabı yoruma yaz!'
    cap = (f"EBOB HESAPLANDI, PEKİ SONRA? +1 mi, −1 mi? 🧮 (Bölüm {no}: {e['tur'].title()})\n\n" + ' · '.join(e['calc']) + f"\n\nKural: {' — '.join(e['rule'])}\n\n"
           + ('SIRA SENDE: ' + ' '.join(x for x in e['nextq'] if x) + f' {nxt}\n\n') + "Kaydet, LGS matematik için lazım olur 📌\n\nHer gün matematik için takip et 👆")
    return e['slug'], f'EBOB +1/−1 tuzağı {no}: {e["tur"].title()}', cfg, e['ses'], cap

ON = MU.JS[:MU.JS.index("let big,mini")]
ON = ON.replace("const tit=T('2028 RADARI',540,420,112,WH,{filter:'url(#glow)'});",
                "const tit=T(CFG.title,540,420,100,WH,{filter:'url(#glow)'}); {const w=tit.getComputedTextLength(); if(w>980)tit.setAttribute('font-size',100*980/w)}")
ARA = MU.JS[MU.JS.index("/*MASCOT*/"):MU.JS.index("function content(t){")]
SON = MU.JS[MU.JS.index("function mascot(t){"):]
ORTA = r"""
const YESIL='#7be08a', TURUNCU='#ffb347', KIRMIZI='#ff6b6b', PEMBE='#ff8fa3';
const G=CFG.geo, KIND=CFG.kind, BC=CFG.bcol;
const dG=el('g',{opacity:0}); const PT=[], ENDS=[];
function mkText(lines,x,y0,dy,size,fill,extra){const g=el('g',{opacity:0}); const arr=[]; lines.forEach((s,i)=>{arr.push(TF(s,x,y0+i*dy,size,Array.isArray(fill)?fill[i]:fill,960,extra||{},g))}); return {g,arr}}
if(G){
 G.lines.forEach(L=>{ if(L.wood){ const [a,b]=L.pts; el('rect',{x:a[0],y:a[1]-24,width:b[0]-a[0],height:48,rx:14,fill:'#8b5a2b',stroke:'#e0b070','stroke-width':4},dG)}
   else {const d=L.pts.map((p,i)=>(i?'L':'M')+p[0]+','+p[1]).join(' ')+(L.closed?' Z':''); el('path',{d,fill:'none',stroke:'#cfe8d4','stroke-width':5,'stroke-dasharray':'2 12','stroke-linecap':'round'},dG)}});
 G.labels.forEach(([x,y,s,z,c])=>T(s,x,y,z,c,{},dG));
 G.pts.forEach(([x,y])=>{const g=el('g',{opacity:0},dG);
   if(G.kind==='tree'){el('rect',{x:x-3,y:y,width:6,height:12,fill:'#8b5a2b'},g); el('circle',{cx:x,cy:y-3,r:15,fill:'#3fbf5a',stroke:'#fff','stroke-width':3},g)}
   else if(G.kind==='cut'){el('line',{x1:x,y1:y-40,x2:x,y2:y+40,stroke:KIRMIZI,'stroke-width':8,'stroke-linecap':'round'},g); T('✂',x,y-48,34,'#fff',{},g)}
   else {el('line',{x1:x,y1:y+14,x2:x,y2:y,stroke:'#fff','stroke-width':4},g); el('circle',{cx:x,cy:y-8,r:14,fill:GOLD,stroke:'#fff','stroke-width':3},g)}
   PT.push({g,x,y})});
 G.ends.forEach(([x,y])=>{const g=el('g',{opacity:0},dG);
   if(G.endx){el('path',{d:`M${x-16},${y-16} L${x+16},${y+16} M${x+16},${y-16} L${x-16},${y+16}`,stroke:KIRMIZI,'stroke-width':9,'stroke-linecap':'round'},g)}
   else el('circle',{cx:x,cy:y-3,r:26,fill:'none',stroke:BC,'stroke-width':7},g);
   ENDS.push({g,x,y})});
}
const cnt=T('',830,880,46,WH,{opacity:0,filter:'url(#glow)'});
const prevG=el('g',{opacity:0}); T('GEÇEN CEVAP',540,975,40,CY,{'letter-spacing':8},prevG); T(CFG.prev||'',540,1075,110,GOLD,{filter:'url(#glow)'},prevG);
const hookT=T('EBOB HESAPLANDI.',540,985,64,WH,{opacity:0,filter:'url(#glow)'}); const hookQ=el('g',{opacity:0}); T('+1 mi?',300,1085,100,YESIL,{filter:'url(#glow)'},hookQ); T('−1 mi?',780,1085,100,PEMBE,{filter:'url(#glow)'},hookQ);
const PB=mkText(CFG.prob,540,975,70,46,WH,{}), EB=mkText(CFG.ebob,540,1000,80,62,[GOLD,CY],{filter:'url(#glow)'});
const CL=mkText(CFG.calc,540,960,66,46,[WH,WH,GOLD],{}); const calcEl=CL.arr;
const rG=el('g',{opacity:0}); el('rect',{x:50,y:920,width:980,height:230,rx:40,fill:'rgba(10,50,25,.85)',stroke:BC,'stroke-width':7},rG);
T(CFG.badge||'',540,1005,86,BC,{filter:'url(#glow)','font-weight':900},rG); T((CFG.rule||[])[0]||'',540,1075,46,WH,{},rG); T((CFG.rule||[])[1]||'',540,1125,44,CY,{},rG);
const nG=el('g',{opacity:0}); el('rect',{x:60,y:560,width:960,height:510,rx:46,fill:'rgba(10,50,25,.85)',stroke:GOLD,'stroke-width':6},nG);
T('SIRA SENDE',540,635,44,GOLD,{'letter-spacing':10},nG); CFG.nextq.forEach((s,i)=>{if(s)TF(s,540,715+i*76,i===3?72:54,i===3?CY:WH,900,i===3?{filter:'url(#glow)'}:{},nG)});
// rehber
const RH=[]; if(KIND==='rehber'){CFG.rehber.forEach(([a,b,c],i)=>{const g=el('g',{opacity:0}); const y=590+i*84; el('rect',{x:50,y:y-48,width:980,height:70,rx:22,fill:'rgba(10,50,25,.8)',stroke:c,'stroke-width':4},g); TF(a,70,y,40,WH,520,{'text-anchor':'start'},g); T(b,830,y,40,c,{'font-weight':900},g); RH.push(g)})}
"""
CONTENT = r"""
function content(t){
 const fin=ramp(t,B[6]-.05,B[6]+.4), fo=1-fin;
 if(KIND==='rehber'){
  const T0=[B[1]-.1,B[2]-.1,B[2]+.9,B[3],B[4],B[4]+.8];
  RH.forEach((g,i)=>{const a=ramp(t,T0[i],T0[i]+.4)*fo; setT(g,a,.9+.1*back(ramp(t,T0[i],T0[i]+.5)),540,590+i*84)});
  setT(prevG,ramp(t,.3,.7)*(1-ramp(t,B[1]-.3,B[1]+.1)),1,540,1030);
  const ru=ramp(t,B[5]+.1,B[5]+.6)*fo; setT(rG,ru,.9+.1*back(ramp(t,B[5]+.1,B[5]+.6)),540,1035);
  setT(nG,fin,.9+.1*back(fin),540,815); return}
 // diyagram
 const dv=ramp(t,B[1]+.2,B[1]+.7)*fo; dG.setAttribute('opacity',dv);
 const t0=B[4]+.2, t1=B[5]-.5, n=PT.length; let shown=0;
 PT.forEach((p,i)=>{const a=ramp(t,t0+(t1-t0)*i/n,t0+(t1-t0)*i/n+.25); p.g.setAttribute('opacity',a); if(a>.9)shown++; p.g.setAttribute('transform',`translate(${p.x},${p.y}) scale(${.4+.6*back(a)}) translate(${-p.x},${-p.y})`)});
 const ev=ramp(t,B[3],B[3]+.4)*(1-.0)*(t<B[5]?1:.6); ENDS.forEach((e,i)=>{e.g.setAttribute('opacity',ev*(.65+.35*Math.sin(t*6+i))); });
 cnt.textContent=(CFG.counter?CFG.counter+': ':'')+shown; cnt.setAttribute('opacity',ramp(t,t0,t0+.3)*fo*(1-ramp(t,B[5]+.2,B[5]+.6)));
 // metin bölgesi
 const pv=ramp(t,B[0]+.2,B[0]+.6)*(1-ramp(t,B[1]-.2,B[1]+.1)); setT(prevG,CFG.prev?pv:0,.9+.1*back(ramp(t,B[0]+.2,B[0]+.7)),540,1030);
 const hv0=ramp(t,.4,.9)*(1-ramp(t,B[1]-.2,B[1]+.1)); hookT.setAttribute('opacity',CFG.prev?0:hv0); 
 const pb=ramp(t,B[1]+.1,B[1]+.5)*(1-ramp(t,B[2]-.1,B[2]+.2)); setT(PB.g,pb,1,540,1000);
 const eb=ramp(t,B[2]+.1,B[2]+.5)*(1-ramp(t,B[3]-.1,B[3]+.2)); setT(EB.g,eb,.9+.1*back(ramp(t,B[2]+.1,B[2]+.6)),540,1030);
 const hq=ramp(t,B[3]+.1,B[3]+.5)*(1-ramp(t,B[4]-.1,B[4]+.2)); hookQ.setAttribute('opacity',hq); setT(hookQ,hq,.85+.15*back(ramp(t,B[3]+.1,B[3]+.6)),540,1060);
 const cv=ramp(t,B[4]+.1,B[4]+.4)*(1-ramp(t,B[5]-.05,B[5]+.25)); CL.g.setAttribute('opacity',cv);
 calcEl.forEach((e,i)=>{const s=B[4]+.2+i*(B[5]-B[4]-.6)/3; e.setAttribute('opacity',ramp(t,s,s+.3))});
 const ru=ramp(t,B[5]+.1,B[5]+.6)*fo; setT(rG,ru,.9+.1*back(ramp(t,B[5]+.1,B[5]+.6)),540,1035);
 setT(nG,fin,.9+.1*back(fin),540,815);
}
"""
JS_E = ON + ORTA + ARA + CONTENT + SON

def sahne_html(cfg):
    MU.JS = JS_E
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
               'muzik_dosya': 'kutuphane/muzik/' + uzun[(no + 3) % len(uzun)], 'muzik_baslangic': 6}, open(d + '/ses.json', 'w', encoding='utf-8'), ensure_ascii=False)
    pj = f'{d}/post.json'; old = json.load(open(pj)) if os.path.exists(pj) else {}
    post = {'baslik': baslik, 'tur': 'özgün', 'sure': 60, 'fps': 30, 'caption': cap, 'hashtagler': ETIKET,
            'kaynak': 'EBOB +1/−1 tuzağı serisi (konu fikri: kullanıcının gösterdiği karusel; sayılar, tasarım ve anlatım özgün Mathlemur)',
            'durum': old['durum'] if old.get('durum') in ('taslak', 'onay-bekliyor') else 'taslak', 'ana_izgara': False,
            'kayit': old.get('kayit', []) + ['EBOB +1/−1 serisi taslağı üretildi (yayın zamanını kullanıcı belirleyecek)']}
    json.dump(post, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2); open(pj, 'a').write('\n')
    return slug

if __name__ == '__main__':
    secim = set(sys.argv[1:])
    for no, e in enumerate(EP, 1):
        if secim and e['slug'] not in secim: continue
        v = tanim(e, no); print(yaz(*v), 'end=', v[2]['end'])
