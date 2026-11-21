#!/usr/bin/env python3
"""Kodla müzik + efekt üretir. Kullanım: python3 muzik.py <icerik-klasoru>
Klasörde ses.json olmalı: {"sure":20,"bpm":124,"sfx":[{"t":0.3,"tip":"pop"},...]}  Çıktı: ses/music.wav, ses/sfx.wav"""
import json, sys, os, wave
import numpy as np
from scipy import signal
SR = 44100
rng = np.random.default_rng(7)
d = sys.argv[1]; cfg = json.load(open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(d, 'ses.json')))
D, BPM = cfg['sure'], cfg.get('bpm', 124); N = int(D*SR); beat = 60/BPM; bar = 4*beat
def mix_in(buf, snd, t, g=1.0):
    i = int(t*SR)
    if i >= len(buf): return
    e = min(len(buf), i+len(snd)); buf[i:e] += snd[:e-i]*g
def lp(x, fc, o=2): return signal.lfilter(*signal.butter(o, fc/(SR/2), 'low'), x)
def hp(x, fc, o=2): return signal.lfilter(*signal.butter(o, fc/(SR/2), 'high'), x)
def bp(x, f1, f2, o=2): return signal.lfilter(*signal.butter(o, [f1/(SR/2), f2/(SR/2)], 'band'), x)
def midi(m): return 440*2**((m-69)/12)
def kick():
    t = np.arange(int(.32*SR))/SR; f = 48+120*np.exp(-t*28)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*8.5)
def clap():
    t = np.arange(int(.22*SR))/SR; n = bp(rng.standard_normal(len(t)), 900, 4500)
    env = np.exp(-t*22)+0.8*np.exp(-((t-.012)%.012)*0) * 0
    for k in (0.0, .011, .022): env += np.where(t >= k, np.exp(-(t-k)*70), 0)*0.7
    return n*env*0.5
def hat(op=False):
    t = np.arange(int((.18 if op else .05)*SR))/SR
    return hp(rng.standard_normal(len(t)), 7000)*np.exp(-t*(18 if op else 70))*0.5
def saw(f, n, ph=0): return 2*((f*np.arange(n)/SR+ph) % 1)-1
def bassnote(f, dur):
    n = int(dur*SR); t = np.arange(n)/SR
    x = lp(saw(f, n)+0.6*np.sin(2*np.pi*f*t), 420)
    return x*np.minimum(1, t/.004)*np.exp(-t*5)
def stab(freqs, dur=.22):
    n = int(dur*SR); t = np.arange(n)/SR
    x = sum(saw(f, n, i*.13)+saw(f*1.004, n) for i, f in enumerate(freqs))/len(freqs)/2
    return lp(x, 2600)*np.exp(-t*14)*np.minimum(1, t/.003)
def ks(f, dur, bright=.5):
    """Karplus-Strong: lir/lavta benzeri telli çalgı"""
    n = int(dur*SR); p = max(2, int(SR/f)); buf = rng.uniform(-1, 1, p); out = np.empty(n)
    buf = lp(buf, 6000, 1) if bright < .5 else buf
    for i in range(n):
        j = i % p; out[i] = buf[j]; buf[j] = .5*(buf[j]+buf[(j+1) % p])*.9985
    return out*np.exp(-np.arange(n)/SR*2.2)
# ---------- müzik ----------
M = np.zeros(N)
prog = [(33, [57, 60, 64]), (29, [53, 57, 60]), (36, [60, 64, 67]), (31, [55, 59, 62])]  # Am F C G (bas, akor)
K, C, H, HO = kick(), clap(), hat(), hat(True)
nb = int(D/beat)+1
for b in range(nb):
    t = b*beat; bi = int(t/bar); ch = prog[bi % 4]
    mix_in(M, K, t, 1.0 if t < D-.6 else .0)
    if bi >= 1 and b % 4 in (1, 3): mix_in(M, C, t, .8)
    mix_in(M, H, t+beat/2, .55); mix_in(M, H if b % 2 else HO, t+beat*.25, .25) if bi >= 2 else None
    if bi >= 1:
        for k in range(2):  # bas: sekizlikler
            mix_in(M, bassnote(midi(ch[0]) , beat*.48), t+k*beat/2, .55 if k == 0 else .4)
    if bi >= 2 and b % 4 in (0, 2): mix_in(M, stab([midi(m) for m in ch[1]]), t+beat/2, .22)
# lir melodisi (Karplus-Strong), sekizlik arpej + her 4 barda küçük motif
cache = {}
def pluck(m, dur=.55):
    if (m, dur) not in cache: cache[(m, dur)] = ks(midi(m), dur)
    return cache[(m, dur)]
pat = [0, 1, 2, 1, 2, 1, 2, 1]; motif = {3: [76, 74, 72, 69], 7: [79, 76, 74, 72]}
for b in range(nb):
    t = b*beat; bi = int(t/bar); ch = prog[bi % 4][1]
    for e in range(2):
        s = (b % 4)*2+e; m = ch[pat[s]]+12
        mix_in(M, pluck(m), t+e*beat/2, .30 if bi < 1 else .42)
    if bi % 4 == 3 and b % 4 == 3: pass
mel = [(4, 76), (4.5, 79), (5, 81), (5.5, 79)]  # kısa Yunan-modlu hook
hook = [81, 80, 77, 76, 77, 80, 81, 84]  # Hicaz/Frig kokulu
for k, m in enumerate(hook):
    mix_in(M, pluck(m, .6), 4*bar+k*beat/2, .5)
for k, m in enumerate(hook[::-1]):
    mix_in(M, pluck(m, .6), 7*bar+k*beat/2, .5)
M = np.tanh(M*1.1)
fade = np.ones(N); fl = int(1.0*SR); fade[-fl:] = np.linspace(1, 0, fl)**1.5; M *= fade
M = M/np.max(np.abs(M))*.8
# ---------- efektler ----------
X = np.zeros(N)
def whoosh(dur=.7, up=True):
    n = int(dur*SR); x = rng.standard_normal(n); out = np.zeros(n); ch = 1024; zi = None
    for i in range(0, n, ch):
        k = i/n; fc = (300+5200*np.sin(np.pi*(k if up else 1-k)*.5+0.01)**2) if True else 1000
        b, a = signal.butter(2, [max(150, fc*.5)/(SR/2), min(.45, fc*1.4/(SR/2))], 'band')
        if zi is None: zi = signal.lfilter_zi(b, a)*0
        y, zi = signal.lfilter(b, a, x[i:i+ch], zi=zi); out[i:i+ch] = y
    env = np.sin(np.pi*np.linspace(0, 1, n))**1.5
    return out*env*1.6
def pop():
    t = np.arange(int(.14*SR))/SR; f = 380+700*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*24)*.9
def ding():
    t = np.arange(int(1.6*SR))/SR; x = sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*dk) for f, a, dk in [(1318.5, 1, 3), (1975.5, .5, 4), (2637, .35, 6), (3951, .12, 8)])
    return x*.55
def sparkle():
    out = np.zeros(int(1.4*SR))
    for k, m in enumerate([88, 91, 93, 95]):
        t = np.arange(int(.7*SR))/SR; s = np.sin(2*np.pi*midi(m)*t)*np.exp(-t*7)*.35; i = int(k*.07*SR); out[i:i+len(s)] += s
    return out
def tick():
    t = np.arange(int(.05*SR))/SR; return np.sin(2*np.pi*1800*t)*np.exp(-t*90)*.5
def zipla(dur=.30, glide=300):
    """Sevimli hareket sesi: yumuşak, yukarı kayan 'bıdık' (22 Kas kararı: rüzgâr/whoosh sesi rahatsız ediyordu)."""
    t = np.arange(int(dur*SR))/SR; f = 300+glide*(1-np.exp(-t*16)); ph = 2*np.pi*np.cumsum(f)/SR
    x = np.sin(ph)+.28*np.sin(2*ph)+.1*np.sin(3*ph); env = (1-np.exp(-t*260))*np.exp(-t*(12 if dur < .4 else 9))
    return lp(x*env, 3200)*.85
TATLI = {'whoosh_kisa': 'zipla', 'swish': 'zipla', 'whoosh': 'zipla_buyuk'}   # eski rüzgâr efektleri yerine sevimli ses (yeni üretimler)
fx = {'pop': pop, 'ding': ding, 'sparkle': sparkle, 'tick': tick,
      'zipla': zipla, 'zipla_buyuk': lambda: zipla(.45, 480), 'whoosh': lambda: whoosh(.7), 'whoosh_kisa': lambda: whoosh(.45), 'swish': lambda: whoosh(.9, up=True)}
for e in cfg['sfx']: mix_in(X, fx[TATLI.get(e['tip'], e['tip']) if not os.environ.get('ESKI_SES') else e['tip']](), e['t'], e.get('g', .6))
X = np.tanh(X)*1.0; X = X/max(1e-9, np.max(np.abs(X)))*.7 if np.max(np.abs(X)) > 0 else X
def save(path, mono):
    st = np.stack([mono, mono], 1); pcm = (np.clip(st, -1, 1)*32767).astype('<i2')
    with wave.open(path, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
os.makedirs(os.path.join(d, 'ses'), exist_ok=True)
save(os.path.join(d, 'ses', 'music.wav'), M); save(os.path.join(d, 'ses', 'sfx.wav'), X)
print('ok', D, 'sn', BPM, 'bpm')
