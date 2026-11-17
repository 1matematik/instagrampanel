#!/usr/bin/env python3
"""Microsoft Edge nöral sesleri (ücretsiz, anahtarsız) ile her cümleyi ayrı WAV yapar.
Kullanım: python3 ahmet_tts.py <metin.txt> <cikti-klasoru> [ses=tr-TR-AhmetNeural] [hiz=+8%] [perde=+0Hz]
Çıktı: cumle-N.wav + sesler.json (gemini_tts.py ile aynı biçim)."""
import sys, os, json, asyncio, subprocess
import edge_tts
txt, out = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else 'tr-TR-AhmetNeural'
rate = sys.argv[4] if len(sys.argv) > 4 else '+8%'
pitch = sys.argv[5] if len(sys.argv) > 5 else '+0Hz'
os.makedirs(out, exist_ok=True)
lines = [l.strip() for l in open(txt, encoding='utf-8') if l.strip()]
async def one(i, text):
    mp3 = os.path.join(out, f"cumle-{i}.mp3"); wav = os.path.join(out, f"cumle-{i}.wav")
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(mp3); break
        except Exception as e:
            if attempt == 3: sys.exit(f"cümle {i} üretilemedi: {e}")
            await asyncio.sleep(3)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",mp3,"-ar","24000","-ac","1","-c:a","pcm_s16le",wav],check=True)
    d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",wav]))
    os.remove(mp3)
    return {"no": i, "metin": text, "sure": d, "model": voice}
async def main():
    res = []
    for i, t in enumerate(lines, 1):
        r = await one(i, t); res.append(r); print(r)
    json.dump(res, open(os.path.join(out,'sesler.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
asyncio.run(main())
