#!/usr/bin/env python3
"""Hareketli, saydam logo filigranı. Kullanım: python3 yayin/filigran.py video.mp4 [video2.mp4 ...]
Logo tüm video boyunca ekranda sürekli süzülür (alpha ~0.42). Aynı dosyaya iki kez uygulanmaz."""
import sys, os, subprocess, json
LOGO=os.path.join(os.path.dirname(os.path.abspath(__file__)),'logo','filigran.png')
SZ=165; ALPHA=0.42; SEG=4.5
# (x,y) başlangıç, (dx,dy) segment boyunca kayma — Reels arayüz alanları (sağ alt) kaçınıldı
POS=[(40,230,30,24),(870,230,-26,30),(40,860,24,-30),(870,880,-30,26),(40,1480,28,-24),(870,520,-24,28),(40,520,30,26),(870,1200,-20,-30)]
def dur(f):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode().strip())
def tags(f):
    o=subprocess.check_output(['ffprobe','-v','error','-show_entries','format_tags=comment','-of','json',f]).decode()
    return json.loads(o).get('format',{}).get('tags',{}).get('comment','')
def isle(f):
    if 'filigran2' in tags(f): print('atlandı (zaten var):',f); return
    d=dur(f)
    # tek logo, tüm video boyunca ekranda süzülür (sağ alt Reels arayüzü hariç)
    x="(40+415*(1+sin(t*0.55+0.6)))"; y="(210+640*(1+sin(t*0.37+2.1)))"
    fc=f"[1:v]format=rgba,scale={SZ}:{SZ},fade=t=in:st=0:d=0.8:alpha=1,colorchannelmixer=aa={ALPHA}[w];[0:v][w]overlay=x='{x}':y='{y}':eof_action=pass[vout]"
    tmp=f+'.tmp.mp4'
    cmd=['ffmpeg','-y','-loglevel','error','-i',f,'-loop','1','-framerate','30','-t',str(d),'-i',LOGO,'-filter_complex',fc,'-map','[vout]','-map','0:a?','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-metadata','comment=filigran2','-movflags','+faststart','-shortest',tmp]
    subprocess.check_call(cmd); os.replace(tmp,f); print('filigran eklendi:',f)
if __name__=='__main__':
    for f in sys.argv[1:]: isle(f)
