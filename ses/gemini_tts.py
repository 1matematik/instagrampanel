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
