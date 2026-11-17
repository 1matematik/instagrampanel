#!/usr/bin/env node
// Yayın takvimi planlayıcı.
// Kullanım:  node yayin/planla.mjs [--baslangic=2026-11-18] [--gunluk=1] [--yaz] slug1 slug2 ...
//   --yaz yoksa sadece planı gösterir (kuru çalışma). --yaz ile post.json içine yayin_zamani yazar
//   (durum "onay-bekliyor" kalır; yayın ancak "onayla" ile başlar).
//
// Algoritma (Türkiye saati, TRT = UTC+3):
//  1) Tepe pencereler (hedef kitle: ortaokul/lise öğrencileri + veliler):
//       hafta içi : 16:30 (okul çıkışı)   ve 21:15 (akşam kaydırma)
//       hafta sonu: 11:00 (geç kahvaltı)  ve 21:00
//     Kaynaklar: Türkiye için 15-17 arası ve 21-23 arası yoğunluk raporları; kitle davranışı varsayımıdır,
//     gerçek veri geldikçe (Insights) tepe saatler güncellenir.
//  2) Günde en fazla --gunluk paylaşım (varsayılan 1, üst sınır 2), iki paylaşım arası >= 5 saat.
//  3) Aynı konunun 6 tema versiyonu üst üste yığılmasın diye varsayılan 1/gün; pencereler sırayla
//     dönüşümlü kullanılır (A/B testi): hangi saat daha çok izlenme/kaydetme getiriyor, veriyle bakılır.
//  4) Geçmiş zamana plan yapılmaz; başlangıç tarihi bugünden önceyse yarına alınır.
import fs from 'fs'; import path from 'path';
const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const args=process.argv.slice(2), opt={}, slugs=[];
for(const a of args){ if(a.startsWith('--')){ const [k,v]=a.slice(2).split('='); opt[k]=v??true; } else slugs.push(a); }
const GUNLUK=Math.min(2,Math.max(1,parseInt(opt.gunluk||'1',10)));
const PENCERE={hafta:['16:30','21:15'], sonu:['11:00','21:00']};
const pad=n=>String(n).padStart(2,'0');
const trtNow=new Date(Date.now()+3*3600e3);
let gun=opt.baslangic? new Date(opt.baslangic+'T00:00:00Z') : new Date(Date.UTC(trtNow.getUTCFullYear(),trtNow.getUTCMonth(),trtNow.getUTCDate()+1));
const plan=[]; let idx=0;
while(idx<slugs.length){
  const d=gun.getUTCDay(), saatler=(d===0||d===6)?PENCERE.sonu:PENCERE.hafta;
  for(let k=0;k<GUNLUK && idx<slugs.length;k++){
    // Günde 1 paylaşım: pencereleri günler arası dönüşümlü kullan (A/B). Günde 2: ikisini de kullan.
    const slot= GUNLUK===1 ? saatler[idx%2] : saatler[k];
    const iso=`${gun.getUTCFullYear()}-${pad(gun.getUTCMonth()+1)}-${pad(gun.getUTCDate())}T${slot}:00+03:00`;
    if(Date.parse(iso)>Date.now()+30*60e3) plan.push({slug:slugs[idx++],iso});
  }
  gun=new Date(gun.getTime()+86400e3);
}
// Etiketler: en fazla 5 (Instagram sınırı) = 2 geniş + 2 niş + 1 temaya özel
const TEMA={'yunan':'antikyunan','misir':'antikmısır','mezopotamya':'mezopotamya','asya':'antikçin','amerika':'maya','antarktika':'antarktika'};
const gunAdi=['Pazar','Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi'];
for(const p of plan){
  const tema=TEMA[p.slug.split('-')[0]];
  const tags=['matematik','ikikarefarkı','özdeşlikler','lgs']; if(tema) tags.push(tema);
  const gn=gunAdi[new Date(p.iso.slice(0,10)+'T12:00:00Z').getUTCDay()];
  console.log(`${p.iso.slice(0,10)} ${gn.padEnd(10)} ${p.iso.slice(11,16)}  ${p.slug}  #${tags.join(' #')}`);
  if(opt.yaz){
    const f=path.join(ROOT,'icerik',p.slug,'post.json'), o=JSON.parse(fs.readFileSync(f,'utf8'));
    o.yayin_zamani=p.iso; o.hashtagler=tags; o.ana_izgara=false; // sadece Reels sekmesi
    (o.kayit ||= []).push(new Date().toISOString()+' takvime alındı: '+p.iso);
    fs.writeFileSync(f,JSON.stringify(o,null,2)+'\n');
  }
}
if(!opt.yaz) console.log('\n(kuru çalışma — yazmak için --yaz ekle)');
