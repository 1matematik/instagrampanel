#!/usr/bin/env python3
"""Kodla ses efekti kütüphanesi üretir (hepsi orijinal, telif sorunu yok). Kullanım: python3 efekt_uret.py <cikti-klasoru>"""
import sys, os, wave, numpy as np
from scipy import signal
SR=44100; rng=np.random.default_rng(11); out=sys.argv[1]; os.makedirs(out,exist_ok=True)
def T(d): return np.arange(int(d*SR))/SR
def lp(x,fc,o=2): return signal.lfilter(*signal.butter(o,min(.99,fc/(SR/2)),'low'),x)
def hp(x,fc,o=2): return signal.lfilter(*signal.butter(o,fc/(SR/2),'high'),x)
def bp(x,f1,f2,o=2): return signal.lfilter(*signal.butter(o,[f1/(SR/2),min(.99,f2/(SR/2))],'band'),x)
def midi(m): return 440*2**((m-69)/12)
def noise(n): return rng.standard_normal(n)
def sweep_noise(d,f0,f1,shape=1.5):
    n=int(d*SR); x=noise(n); o=np.zeros(n); zi=None; ch=1024
    for i in range(0,n,ch):
        k=i/n; fc=f0+(f1-f0)*k; b,a=signal.butter(2,[max(120,fc*.5)/(SR/2),min(.95,fc*1.5/(SR/2))],'band')
        if zi is None: zi=signal.lfilter_zi(b,a)*0
        y,zi=signal.lfilter(b,a,x[i:i+ch],zi=zi); o[i:i+ch]=y
    return o*np.sin(np.pi*np.linspace(0,1,n))**shape*1.8
def sine(f,d,dk=6): t=T(d); return np.sin(2*np.pi*f*t)*np.exp(-t*dk)
def pitchsweep(f0,f1,d,dk=20,rate=30):
    t=T(d); f=f1+(f0-f1)*np.exp(-t*rate); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*dk)
def ks(f,d,damp=.9985,dk=2.2):
    n=int(d*SR); p=max(2,int(SR/f)); buf=rng.uniform(-1,1,p); o=np.empty(n)
    for i in range(n):
        j=i%p; o[i]=buf[j]; buf[j]=.5*(buf[j]+buf[(j+1)%p])*damp
    return o*np.exp(-np.arange(n)/SR*dk)
def seq(parts,gap):
    n=int((max(t for t,_ in parts)+max(len(s)/SR for _,s in parts)+.1)*SR); o=np.zeros(n)
    for t,s in parts: i=int(t*SR); o[i:i+len(s)]+=s[:n-i]
    return o
def env(x,a=.003,r=.03):
    n=len(x); e=np.ones(n); na=int(a*SR); nr=int(r*SR); e[:na]=np.linspace(0,1,na); e[-nr:]=np.linspace(1,0,nr); return x*e
S={}
S['whoosh-kisa']=sweep_noise(.45,500,4500); S['whoosh-uzun']=sweep_noise(1.1,300,5000,1.2)
S['whoosh-yukari']=sweep_noise(.7,400,6500); S['whoosh-asagi']=sweep_noise(.7,6000,400)
for i,f in enumerate([520,760,1100],1): S[f'pop-0{i}']=pitchsweep(f*2,f,.14,dk=26,rate=34)*.9
S['tik']=sine(1800,.05,90)*.6; S['tak']=sine(900,.06,70)*.6
t=T(.5); S['tik-tak']=seq([(0,S['tik']),(.35,S['tak'])],0)
S['ding-cin']=(sine(1318.5,1.6,3)+.5*sine(1975.5,1.6,4)+.35*sine(2637,1.6,6)+.12*sine(3951,1.6,8))*.55
S['ding-lir']=ks(midi(88),1.4,dk=2.5)*.8
S['pirilti']=seq([(k*.07,sine(midi(m),.7,7)*.4) for k,m in enumerate([88,91,93,95])],0)
S['lir-glissando']=seq([(k*.055,ks(midi(m),.7,dk=3)*.5) for k,m in enumerate([69,72,76,81,84,88])],0)
S['lir-akor']=sum(np.pad(ks(midi(m),1.2,dk=2.6),(0,0))*.45 for m in [57,60,64,69])
S['riser-2sn']=(sweep_noise(2.0,300,7000,.4)*np.linspace(.1,1,int(2*SR))**2+sine(300,2.0,0)*np.linspace(0,.3,int(2*SR)))
S['darbe-bas']=pitchsweep(120,38,.9,dk=5,rate=14)*1.0+lp(noise(int(.9*SR)),200)*np.exp(-T(.9)*9)*.4
S['davul-vurus']=pitchsweep(170,60,.4,dk=12,rate=22)
S['kick']=pitchsweep(160,45,.32,dk=8.5,rate=28)
S['snare']=bp(noise(int(.25*SR)),1200,7000)*np.exp(-T(.25)*22)*.8+sine(190,.25,25)*.4
tc=T(.22); cl=bp(noise(len(tc)),900,4500)*np.exp(-tc*22)
for k in (0,.011,.022): cl+=np.where(tc>=k,np.exp(-(tc-k)*70),0)*bp(noise(len(tc)),900,4500)*.7
S['alkis-tek']=cl*.5
S['hat']=hp(noise(int(.05*SR)),7000)*np.exp(-T(.05)*70)*.7
S['davul-roll']=seq([(k*.06,pitchsweep(220,90,.15,dk=22,rate=25)*(.25+.75*k/16)) for k in range(17)],0)
S['dogru']=seq([(0,sine(midi(76),.35,5)*.7),(.12,sine(midi(83),.7,4)*.7),(.12,sine(midi(88),.7,5)*.35)],0)
S['yanlis']=env((bp(2*((110*T(.5)%1))-1,100,900)*np.exp(-T(.5)*2.5)+sine(98,.5,3)*.6)*.7,.005,.1)
S['yanlis-kisa']=env(np.sign(np.sin(2*np.pi*140*T(.28)))*lp(np.ones(int(.28*SR)),900)*.35,.005,.08)
S['coin']=seq([(0,sine(midi(83),.12,10)),(.07,sine(midi(88),.6,5)*1.0)],0)*.7
S['baloncuk']=pitchsweep(300,900,.12,dk=30,rate=-1) if False else sine(700,.1,30)*np.sin(2*np.pi*6*T(.1))
S['kagit-cevir']=bp(noise(int(.35*SR)),2000,9000)*np.sin(np.pi*np.linspace(0,1,int(.35*SR)))**2*.9
S['kalem-yazi']=sum(np.pad(bp(noise(int(.09*SR)),3000,8000)*np.exp(-T(.09)*25)*.5,(int(k*.11*SR),0)) [:int(.7*SR)] if True else 0 for k in range(6)) if False else seq([(k*.1,bp(noise(int(.09*SR)),3000,8000)*np.exp(-T(.09)*25)*.5) for k in range(6)],0)
S['tebesir']=seq([(k*.13,bp(noise(int(.1*SR)),2500,9000)*np.exp(-T(.1)*22)*.45) for k in range(4)],0)
S['vurgu']=pitchsweep(400,120,.35,dk=9,rate=18)+bp(noise(int(.35*SR)),500,3500)*np.exp(-T(.35)*18)*.4
S['fanfar']=seq([(0,sum(lp(2*((midi(m)*T(.45)%1))-1,2500)*np.exp(-T(.45)*4) for m in [60,64,67])*.25),(.2,sum(lp(2*((midi(m)*T(.9)%1))-1,3000)*np.exp(-T(.9)*2.5) for m in [67,72,76])*.3)],0)
S['mistik-cin']=(sine(midi(84),2.2,1.6)+sine(midi(84)*1.5,2.2,2)*.4+sine(midi(91),2.2,2.4)*.3)*.4
S['kalp-atisi']=seq([(0,pitchsweep(90,45,.18,dk=16,rate=20)),(.2,pitchsweep(80,40,.16,dk=18,rate=20)*.7)],0)
S['zaman-tik-tak-5sn']=np.concatenate([np.pad(S['tik' if k%2==0 else 'tak'],(0,SR-len(S['tik']))) for k in range(5)])
for k,v in S.items():
    v=np.asarray(v,float); v=env(v,.002,.02); v=v/max(1e-9,np.max(np.abs(v)))*.85
    pcm=(np.clip(v,-1,1)*32767).astype('<i2')
    with wave.open(os.path.join(out,k+'.wav'),'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(len(S),'efekt üretildi')
