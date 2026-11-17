// Onaylı (durum=onaylandi) ve zamanı gelmiş içerikleri Instagram'a Reels olarak yayınlar.
// Gerekli ortam değişkenleri: IG_USER_ID, IG_TOKEN, RAW_BASE (örn. https://raw.githubusercontent.com/KULLANICI/DEPO/main)
// --dry-run: hiçbir şey göndermez.
import fs from 'fs'; import path from 'path';
const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..'), DRY=process.argv.includes('--dry-run');
const {IG_USER_ID,IG_TOKEN,RAW_BASE}=process.env, API='https://graph.facebook.com/v21.0';
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function g(method,url,params){ const u=new URL(API+url); const body=new URLSearchParams({...params,access_token:IG_TOKEN});
  const res= method==='GET' ? await fetch(u+'?'+body) : await fetch(u,{method,body}); const j=await res.json();
  if(!res.ok||j.error) throw new Error(JSON.stringify(j.error||j)); return j; }
let failed=0;
for(const s of fs.readdirSync(path.join(ROOT,'icerik')).sort()){
  const f=path.join(ROOT,'icerik',s,'post.json'); if(!fs.existsSync(f)) continue;
  const o=JSON.parse(fs.readFileSync(f,'utf8')); const save=()=>fs.writeFileSync(f,JSON.stringify(o,null,2)+'\n');
  const note=m=>(o.kayit ||= []).push(new Date().toISOString()+' '+m);
  if(o.durum!=='onaylandi') continue;
  if(o.yayin_zamani && Date.parse(o.yayin_zamani)>Date.now()) { console.log(s,'zamanı gelmedi'); continue; }
  const caption=[o.caption,...(o.hashtagler||[]).slice(0,5).map(h=>'#'+h.replace(/^#/,''))].join('\n\n');
  const videoFile=path.join(ROOT,'yayin','video',s+'.mp4');
  if(!fs.existsSync(videoFile)){ console.log(s,'video yayin/video/ klasöründe yok; atlandı'); continue; }
  const videoUrl=`${RAW_BASE}/yayin/video/${s}.mp4`;
  if(DRY){ console.log('[dry-run] yayınlanırdı:',s,videoUrl,'\n',caption.slice(0,80)); continue; }
  if(!(IG_USER_ID&&IG_TOKEN&&RAW_BASE)){ console.error(s+': yayın için IG_USER_ID, IG_TOKEN, RAW_BASE gerekli; atlandı'); failed++; continue; }
  // Çift paylaşımı önlemek için önce durumu "yayinlaniyor" yap ve kaydet; çökerse kullanıcı elle kontrol eder.
  o.durum='yayinlaniyor'; note('yayın başladı'); save();
  try{
    const c=await g('POST',`/${IG_USER_ID}/media`,{media_type:'REELS',video_url:videoUrl,caption,share_to_feed:'false'});
    for(let i=0;i<60;i++){ const st=await g('GET',`/${c.id}`,{fields:'status_code,status'});
      if(st.status_code==='FINISHED') break; if(st.status_code==='ERROR'||st.status_code==='EXPIRED') throw new Error('işlem hatası: '+st.status);
      if(i===59) throw new Error('video işleme zaman aşımı'); await sleep(10000); }
    const p=await g('POST',`/${IG_USER_ID}/media_publish`,{creation_id:c.id});
    const m=await g('GET',`/${p.id}`,{fields:'permalink'});
    o.durum='yayinlandi'; o.permalink=m.permalink; o.yayin_id=p.id; delete o.hata; note('yayınlandı '+m.permalink);
  }catch(e){ o.durum='hata'; o.hata=String(e.message).slice(0,500); note('HATA '+o.hata); failed++; }
  save(); console.log(s,o.durum,o.permalink||o.hata||'');
}
process.exit(failed?1:0);
