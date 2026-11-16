#!/usr/bin/env bash
# Kullanım: miksaj.sh <icerik-klasoru> [stil: kuru|eko|sanatsal] [ses-kaydi]
# video.mp4 (sessiz) + ses/music.wav + ses/sfx.wav (+ ses kaydı) -> final.mp4
set -euo pipefail
D="$1"; STIL="${2:-sanatsal}"; VOICE="${3:-}"; V="$D/video.mp4"; OUT="${OUT:-$D/final.mp4}"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
case "$STIL" in
 kuru)     FX="highpass=f=85,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=4,loudnorm=I=-15:TP=-1.5:LRA=7" ;;
 eko)      FX="highpass=f=85,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=7,aecho=0.85:0.55:160:0.25" ;;
 sanatsal) FX="highpass=f=90,acompressor=threshold=-20dB:ratio=3.5:attack=5:release=90:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=7,aecho=0.8:0.7:110|240|420:0.4|0.28|0.16,equalizer=f=3500:t=q:w=1:g=2" ;;
 *) echo "stil: kuru|eko|sanatsal"; exit 1 ;;
esac
if [ -n "$VOICE" ]; then
  ffmpeg -y -loglevel error -i "$V" -i "$D/ses/music.wav" -i "$D/ses/sfx.wav" -i "$VOICE" -filter_complex \
   "[3:a]aresample=44100,${FX},apad,atrim=0:${DUR},asplit=2[v][vs];[1:a]volume=0.2[m];[m][vs]sidechaincompress=threshold=0.04:ratio=9:attack=15:release=350[md];[2:a]volume=0.8[x];[md][x][v]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
   -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t "$DUR" "$OUT"
else
  ffmpeg -y -loglevel error -i "$V" -i "$D/ses/music.wav" -i "$D/ses/sfx.wav" -filter_complex \
   "[1:a]volume=0.8[m];[2:a]volume=0.8[x];[m][x]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
   -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t "$DUR" "$OUT"
fi
echo "hazır: $OUT"
