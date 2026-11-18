import sys,glob,re,subprocess,os
d,out=sys.argv[1],sys.argv[2]
fs=sorted(glob.glob(os.path.join(d,'cumle-*.wav')),key=lambda f:int(re.findall(r'(\d+)\.wav',f)[0]))
if not fs: sys.exit('dosya yok: '+d)
args=[];[args.extend(['-i',f]) for f in fs]
fc=''.join(f'[{i}:a]aresample=24000,apad=pad_dur=0.35[a{i}];' for i in range(len(fs)))+''.join(f'[a{i}]' for i in range(len(fs)))+f'concat=n={len(fs)}:v=0:a=1[o]'
subprocess.check_call(['ffmpeg','-y','-loglevel','error',*args,'-filter_complex',fc,'-map','[o]','-b:a','128k',out]); print('ok',out)
