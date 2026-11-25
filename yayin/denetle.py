#!/usr/bin/env python3
"""Depo bütünlük denetimi: her içerik klasörünün dosyaları, videosu, zamanlaması tam mı?
Kullanım: python3 yayin/denetle.py   → eksikleri listeler (çıkış kodu 0 = eksik yok)"""
import os, json, glob, sys, datetime
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEREK = ['sahne.html', 'ses.json', 'post.json', 'ses/metin.txt']
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
eksik, sayac = [], {}
for d in sorted(glob.glob(f'{R}/icerik/*/')):
    s = os.path.basename(d.rstrip('/'))
    try: p = json.load(open(d + 'post.json'))
    except Exception as e: eksik.append((s, f'post.json okunamadı: {e}')); continue
    du = p.get('durum'); sayac[du] = sayac.get(du, 0) + 1
    for g in GEREK:
        if not os.path.exists(d + g): eksik.append((s, f'dosya yok: {g} (durum {du})'))
    vid = os.path.exists(f'{R}/yayin/video/{s}.mp4')
    if du in ('onay-bekliyor', 'onaylandi', 'yayinlaniyor') and not vid: eksik.append((s, f'durum {du} ama video yok'))
    if du == 'onaylandi':
        z = p.get('yayin_zamani')
        if not z: eksik.append((s, 'onaylandi ama yayin_zamani YOK (hemen yayınlanır!)'))
        else:
            t = datetime.datetime.fromisoformat(z)
            if t < now: eksik.append((s, f'onaylandi ama zamanı geçmiş: {z}'))
    if du == 'taslak' and vid: pass
for v in sorted(glob.glob(f'{R}/yayin/video/*.mp4')):
    s = os.path.basename(v)[:-4]
    if not os.path.isdir(f'{R}/icerik/{s}'): eksik.append((s, 'video var, icerik klasörü yok'))
print('Durum sayıları:', sayac)
for s, m in eksik: print('EKSİK', s, '-', m)
print('TEMİZ' if not eksik else f'{len(eksik)} eksik/uyarı')
sys.exit(1 if eksik else 0)
