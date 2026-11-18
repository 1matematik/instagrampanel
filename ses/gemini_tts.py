#!/usr/bin/env python3
"""Gemini TTS ile her cümleyi ayrı WAV yapar.
Kullanım: GEMINI_API_KEY=... python3 gemini_tts.py <metin.txt> <cikti-klasoru> [ses-adi] [stil]
Her boş olmayan satır bir cümledir. Çıktı: cumle-1.wav ... ve sesler.json (süreler)."""
import sys, os, json, time, base64, wave, urllib.request, urllib.error
txt, out = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else 'Charon'
style = sys.argv[4] if len(sys.argv) > 4 else 'Speak in clear, correct Turkish like a calm, confident, warm male math teacher: articulate every word fully with proper Turkish pronunciation and stress, steady medium pace, short natural pauses between phrases, encouraging tone, gently emphasize the key words and numbers, never rush or swallow word endings'
key = os.environ['GEMINI_API_KEY']
MODELS = [m for m in [os.environ.get('GEMINI_TTS_MODEL'), 'gemini-2.5-flash-preview-tts', 'gemini-2.5-pro-preview-tts'] if m]
os.makedirs(out, exist_ok=True)
lines = [l.strip() for l in open(txt, encoding='utf-8') if l.strip()]
def call(model, text):
    body = {"contents": [{"parts": [{"text": f"{style}: {text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=120) as r: j = json.load(r)
    part = j['candidates'][0]['content']['parts'][0]['inlineData']
    return base64.b64decode(part['data'])  # ham PCM, 16 bit, 24 kHz, mono
def istek(text):
    err = None
    for model in MODELS:
        for attempt in range(6):
            try: return call(model, text), model
            except urllib.error.HTTPError as e:
                err = f"{model} HTTP {e.code}"; time.sleep(35 if e.code in (429, 500, 503) else 1)
                if e.code in (400, 404): break
            except Exception as e: err = f"{model} {e}"; time.sleep(5)
    sys.exit(f"ses üretilemedi: {err}")
def bol(pcm, n):
    """Tek parça sesi en uzun n-1 sessizlikten böler."""
    import numpy as np
    x = np.frombuffer(pcm, '<i2').astype(float); fr = 480  # 20 ms
    rms = np.array([np.sqrt(np.mean(x[i:i+fr]**2)) for i in range(0, len(x)-fr, fr)])
    th = max(250, np.percentile(rms, 95) * 0.06); q = rms < th
    runs = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if i > 0 and j < len(q): runs.append((j - i, i, j))
            i = j
        else: i += 1
    if len(runs) < n - 1: return None
    cuts = sorted(sorted(runs, reverse=True)[:n-1], key=lambda r: r[1])
    sinir = [0] + [((a + b) // 2) * fr for _, a, b in cuts] + [len(x)]
    parca = []
    for a, b in zip(sinir, sinir[1:]):
        seg = x[a:b]; e = np.array([np.sqrt(np.mean(seg[k:k+fr]**2)) for k in range(0, max(1, len(seg)-fr), fr)])
        on = np.where(e >= th)[0]
        if len(on): seg = seg[max(0, (on[0]-2)*fr):min(len(seg), (on[-1]+4)*fr)]
        parca.append(seg.astype('<i2').tobytes())
    return parca
res = []
if os.environ.get('GEMINI_TEK', '1') == '1' and len(lines) > 1:
    metin = "\n".join(f"{t} ..." for t in lines)
    pcm, model = istek(f"Read the following {len(lines)} lines. After each line, pause silently for about one full second before the next line.\n{metin}")
    parca = bol(pcm, len(lines))
    if parca:
        for i, (text, b) in enumerate(zip(lines, parca), 1):
            with wave.open(os.path.join(out, f"cumle-{i}.wav"), 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(b)
            res.append({"no": i, "metin": text, "sure": len(b)/2/24000, "model": model + " (tek istek)"}); print(res[-1])
        json.dump(res, open(os.path.join(out, 'sesler.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        sys.exit(0)
    print("tek istek bölünemedi, cümle cümle devam")
res = []
for i, text in enumerate(lines, 1):
    pcm = None; err = None
    for model in MODELS:
        for attempt in range(6):
            try: pcm = call(model, text); break
            except urllib.error.HTTPError as e:
                err = f"{model} HTTP {e.code}"; time.sleep(35 if e.code in (429, 500, 503) else 1)
                if e.code in (400, 404): break
            except Exception as e: err = f"{model} {e}"; time.sleep(5)
        if pcm: break
    if not pcm: sys.exit(f"cümle {i} üretilemedi: {err}")
    p = os.path.join(out, f"cumle-{i}.wav")
    with wave.open(p, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    res.append({"no": i, "metin": text, "sure": len(pcm)/2/24000, "model": model}); print(res[-1])
    time.sleep(21)  # ücretsiz kota ~3 istek/dk
json.dump(res, open(os.path.join(out, 'sesler.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
