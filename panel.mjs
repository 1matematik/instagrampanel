#!/usr/bin/env node
// Instagram Panel CLI:  node panel.mjs durum | yeni <slug> <tur> | render <slug> | onayla <slug> | iptal <slug>
import fs from 'fs'; import path from 'path'; import { spawnSync } from 'child_process';
const ROOT = path.dirname(new URL(import.meta.url).pathname), DIR = s => path.join(ROOT,'icerik',s);
const TURLER = ['kural','ornek-soru','cozum','dusunme','zeka-oyunu','uyarlama'];
const rd = s => JSON.parse(fs.readFileSync(path.join(DIR(s),'post.json'),'utf8'));
const wr = (s,o) => fs.writeFileSync(path.join(DIR(s),'post.json'), JSON.stringify(o,null,2)+'\n');
const log = (o,m) => (o.kayit ||= []).push(new Date().toISOString()+' '+m);
const [,, cmd, slug, arg] = process.argv;
const need = () => { if(!slug||!fs.existsSync(path.join(DIR(slug),'post.json'))) { console.error('Bulunamadı:',slug); process.exit(1);} };
if (cmd==='durum') {
  for (const s of fs.readdirSync(path.join(ROOT,'icerik')).sort()) { const f=path.join(DIR(s),'post.json'); if(!fs.existsSync(f)) continue;
    const o=rd(s); console.log(s.padEnd(28), (o.durum||'?').padEnd(14), o.tur||'', o.permalink||o.hata||''); }
} else if (cmd==='yeni') {
  if(!slug||!/^[a-z0-9-]+$/.test(slug)||!TURLER.includes(arg)) { console.error('Kullanım: yeni <slug> <'+TURLER.join('|')+'>'); process.exit(1); }
  fs.mkdirSync(DIR(slug),{recursive:true});
  const o={baslik:'',tur:arg,sure:8,fps:30,caption:'',hashtagler:[],yayin_zamani:null,kaynak:'',durum:'taslak',kayit:[]}; log(o,'oluşturuldu'); wr(slug,o);
} else if (cmd==='render') {
  need(); const o=rd(slug), html=path.join(DIR(slug),'sahne.html');
  if(!fs.existsSync(html)) { console.error('sahne.html yok'); process.exit(1); }
  const r=spawnSync('node',[path.join(ROOT,'render/render.mjs'),html,path.join(DIR(slug),'video.mp4'),String(o.sure),String(o.fps),...(fs.existsSync(path.join(DIR(slug),'ses','zaman.json'))?[path.join(DIR(slug),'ses','zaman.json')]:[])],{stdio:'inherit'});
  if(r.status) process.exit(r.status);
  spawnSync('ffmpeg',['-y','-loglevel','error','-ss',String((fs.existsSync(path.join(DIR(slug),'ses','zaman.json'))?JSON.parse(fs.readFileSync(path.join(DIR(slug),'ses','zaman.json'))).sure:o.sure)*0.75),'-i',path.join(DIR(slug),'video.mp4'),'-frames:v','1',path.join(DIR(slug),'kapak.jpg')]);
  o.durum='onay-bekliyor'; log(o,'render edildi, onay bekliyor'); wr(slug,o);
} else if (cmd==='onayla') {
  need(); const o=rd(slug), err=[];
  if(o.durum!=='onay-bekliyor') err.push('durum onay-bekliyor olmalı (şu an: '+o.durum+')');
  if(!fs.existsSync(path.join(ROOT,'yayin','video',slug+'.mp4'))) err.push('yayin/video/'+slug+'.mp4 yok');
  const full=[o.caption,...(o.hashtagler||[]).map(h=>'#'+h.replace(/^#/,''))].join('\n\n');
  if(!o.caption.trim()) err.push('caption boş'); if(full.length>2200) err.push('caption+hashtag 2200 karakteri aşıyor');
  if((o.hashtagler||[]).length>5) err.push('Instagram en fazla 5 hashtag kabul ediyor');
  if(o.yayin_zamani && isNaN(Date.parse(o.yayin_zamani))) err.push('yayin_zamani geçersiz');
  if(err.length){ console.error('ONAYLANAMADI:\n- '+err.join('\n- ')); process.exit(1); }
  o.durum='onaylandi'; log(o,'kullanıcı onayladı'); wr(slug,o); console.log('onaylandı:',slug);
} else if (cmd==='iptal') { need(); const o=rd(slug); o.durum='taslak'; log(o,'iptal/geri alındı'); wr(slug,o); }
else console.log('Komutlar: durum | yeni <slug> <tur> | render <slug> | onayla <slug> | iptal <slug>');
