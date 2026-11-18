#!/usr/bin/env python3
"""ses.json içinde "muzik_dosya" varsa ses/music.wav'ı bu mp3 ile değiştirir (süreye kırpar, fade in/out).
Kullanım: python3 ses/muzik_dosya.py <icerik-klasoru>"""
import sys, os, json, subprocess, wave
d = sys.argv[1]; cfg = json.load(open(os.path.join(d, 'ses.json')))
f = cfg.get('muzik_dosya')
if not f: sys.exit(0)
if not os.path.exists(f): print('müzik dosyası yok, sentetik müzik kalıyor:', f); sys.exit(0)
out = os.path.join(d, 'ses', 'music.wav')
w = wave.open(out); dur = w.getnframes() / w.getframerate(); w.close()
ss = cfg.get('muzik_baslangic', 0)
tmp = out + '.new.wav'
subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(ss), '-i', f, '-t', f'{dur:.2f}',
  '-af', f'loudnorm=I=-18:TP=-2,afade=t=in:d=0.5,afade=t=out:st={max(0, dur-1.5):.2f}:d=1.5',
  '-ar', '44100', '-ac', '1', tmp])
os.replace(tmp, out); print('müzik dosyası kullanıldı:', f, 'başlangıç', ss)
