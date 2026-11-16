// Kullanım: node onizle.mjs <sahne.html> <cikti.png> t1 t2 t3 ...  -> tek kontak sayfası
import { createRequire } from 'module';
const require = createRequire('/opt/npm-tools/node_modules/');
const { chromium } = require('playwright'); import path from 'path'; import { spawnSync } from 'child_process'; import fs from 'fs';
const [,, html, out, ...ts] = process.argv;
const br = await chromium.launch({ executablePath:'/usr/bin/google-chrome', args:['--no-sandbox'] });
const pg = await br.newPage({ viewport:{width:1080,height:1920} }); await pg.goto('file://'+path.resolve(html));
const msgs=[]; pg.on('pageerror',e=>msgs.push(String(e))); pg.on('console',m=>{if(m.type()==='error')msgs.push(m.text())});
const dir='/tmp/onizle'; fs.mkdirSync(dir,{recursive:true});
for (const [i,t] of ts.entries()) { await pg.evaluate(t=>window.seek(t), +t); await pg.screenshot({path:`${dir}/${String(i).padStart(2,'0')}.png`}); }
await br.close(); if(msgs.length) console.log('HATA:',msgs.join('\n'));
spawnSync('python3',['-c',`
from PIL import Image,glob
`],{});
