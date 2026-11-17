#!/usr/bin/env python3
"""Hareketli, saydam logo filigranı. Kullanım: python3 yayin/filigran.py video.mp4 [video2.mp4 ...]
Her ~4.5 sn'de logo ekranın başka bir yerinde beliriyor/siliniyor (alpha ~0.38). Aynı dosyaya iki kez uygulanmaz."""
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
    if 'filigran1' in tags(f): print('atlandı (zaten var):',f); return
    d=dur(f); n=max(1,int((d-1.5)//SEG)+ (1 if (d-1.5)%SEG>2 else 0)); n=min(n,len(POS)*2)
    fc=f"[1:v]format=rgba,scale={SZ}:{SZ},split={n}"+''.join(f'[a{i}]' for i in range(n))+';'
    for i in range(n):
        fc+=f"[a{i}]fade=t=in:st=0:d=0.6:alpha=1,fade=t=out:st={SEG-0.6}:d=0.6:alpha=1,colorchannelmixer=aa={ALPHA},setpts=PTS+{1.5+i*SEG}/TB[w{i}];"
    prev='0:v'
    for i in range(n):
        x,y,dx,dy=POS[i%len(POS)]; ts=1.5+i*SEG
        out=f'o{i}' if i<n-1 else 'vout'
        fc+=f"[{prev}][w{i}]overlay=x='{x}+{dx}*(t-{ts})/{SEG}':y='{y}+{dy}*(t-{ts})/{SEG}':enable='between(t,{ts},{ts+SEG})':eof_action=pass[{out}];"
        prev=out
    fc=fc.rstrip(';')
    tmp=f+'.tmp.mp4'
    cmd=['ffmpeg','-y','-loglevel','error','-i',f,'-loop','1','-framerate','30','-t',str(d),'-i',LOGO,'-filter_complex',fc,'-map','[vout]','-map','0:a?','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-metadata','comment=filigran1','-movflags','+faststart','-shortest',tmp]
    subprocess.check_call(cmd); os.replace(tmp,f); print('filigran eklendi:',f,f'({n} konum)')
if __name__=='__main__':
    for f in sys.argv[1:]: isle(f)
