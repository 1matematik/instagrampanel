#!/usr/bin/env python3
"""Cümle sürelerine göre sahne zamanını ayarlar. Kullanım: python3 senkron.py <icerik-klasoru>
Girdi : ses.json (sahne_basi, sahne_sonu, sfx) + ses/sesler.json + ses/cumle-N.wav
Çıktı : ses/zaman.json (gerçek->sahne zamanı), ses/ses_gercek.json (müzik/efekt için), ses/voice.wav"""
import sys, os, json, wave, numpy as np
d = sys.argv[1]; GAP = 0.25; TAIL = 1.0
cfg = json.load(open(os.path.join(d, 'ses.json'))); S = json.load(open(os.path.join(d, 'ses', 'sesler.json')))
beats = cfg['sahne_basi']; assert len(beats) == len(S), f"{len(beats)} sahne başlangıcı, {len(S)} ses cümlesi: sayılar eşit olmalı"
real = []; t = 0.35
for c in S: real.append(t); t += c['sure'] + GAP
end = t - GAP + TAIL
anch = [[r, b] for r, b in zip(real, beats)] + [[end, cfg['sahne_sonu']]]
anch[0][0] = 0.0  # ilk sahne en baştan başlar
def to_real(sc):
    for (r0, s0), (r1, s1) in zip(anch, anch[1:]):
        if s0 <= sc <= s1: return r0 + (sc - s0) / (s1 - s0) * (r1 - r0)
    return end
json.dump({"anchors": anch, "sure": end}, open(os.path.join(d, 'ses', 'zaman.json'), 'w'), indent=1)
json.dump({"sure": round(end, 3), "bpm": cfg.get('bpm', 124), "sfx": [dict(e, t=round(to_real(e['t']), 3)) for e in cfg['sfx']]},
          open(os.path.join(d, 'ses', 'ses_gercek.json'), 'w'), indent=1)
SR = 24000; buf = np.zeros(int(end*SR) + SR)
for c, r in zip(S, real):
    with wave.open(os.path.join(d, 'ses', f"cumle-{c['no']}.wav")) as w: x = np.frombuffer(w.readframes(w.getnframes()), '<i2')
    i = int(r*SR); buf[i:i+len(x)] += x
with wave.open(os.path.join(d, 'ses', 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.clip(buf, -32768, 32767).astype('<i2').tobytes())
print('toplam süre', round(end, 2), 'sn; sahne ölçekleri:', [round((r1-r0)/(s1-s0), 2) for (r0, s0), (r1, s1) in zip(anch, anch[1:])])
