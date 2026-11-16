// Kullanım: node render.mjs <sahne.html> <cikti.mp4> [saniye] [fps]
// Sahne, window.seek(t) (saniye) fonksiyonunu sunmalı; her kare deterministik çizilir.
import { createRequire } from 'module';
const require = createRequire('/opt/npm-tools/node_modules/');
const { chromium } = require('playwright');
import { spawn } from 'child_process';
import path from 'path';
const [,, html, out, dur='6', fps='30'] = process.argv;
const D = +dur, F = +fps, N = Math.round(D*F);
const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args:['--no-sandbox'] });
const page = await browser.newPage({ viewport:{width:1080,height:1920} });
await page.goto('file://'+path.resolve(html));
await page.evaluate(()=>document.fonts.ready);
const ff = spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(F),'-i','-',
  '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
for (let i=0;i<N;i++){
  await page.evaluate(t=>window.seek(t), i/F);
  const buf = await page.screenshot({type:'jpeg', quality:92});
  if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
}
ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await browser.close();
console.log('bitti', out, N,'kare');
