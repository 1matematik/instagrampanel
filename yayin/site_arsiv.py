#!/usr/bin/env python3
"""Site arşivi üretici (22 Kas kararı): biten videoları okul ağı için 720p / ~3-5 MB sıkıştırır, kapak (açılış sahnesi) çıkarır,
arsiv manifest.json'unu yazar. Artımlıdır: var olan sıkıştırılmış dosyayı atlar; yeni biten videolar eklenir.
Kullanım: python3 yayin/site_arsiv.py <hedef-klasör>        (hedef: ÖZEL depo/klasör; bu depo herkese açık, oraya YAZMA)
Eklenme kuralı: post.json durum 'yayinlandi' olanlar + EK listesi. Maarif Radarı vb. yayına çıkınca otomatik girer."""
import os, sys, json, glob, subprocess, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEDEF = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/site-arsiv')
EK = {'tum-av-04', 'duello-01', 'duello-02'}      # yayın durumundan bağımsız siteye alınanlar (kullanıcı kararı: ekleme)
KAPAK_SN = 2.6

BOLGE = {'yunan': 'Yunan', 'misir': 'Mısır', 'mezopotamya': 'Mezopotamya', 'asya': 'Asya', 'amerika': 'Amerika', 'antarktika': 'Antarktika'}
SERILER = {   # seri_id: (seri adı, konu, sıra)
    'iki-kare-farki': ('İki Kare Farkı  a² − b²', 'Özdeşlikler', 10),
    'arti-kare': ('Artı İfadenin Karesi  (a + b)²', 'Özdeşlikler', 11),
    'eksi-kare': ('Eksi İfadenin Karesi  (a − b)²', 'Özdeşlikler', 12),
    'kok-avcisi': ('Kök Avcısı', 'Kareköklü İfadeler', 20),
    'tum-av': ('Tüm Av', 'Kareköklü İfadeler', 21),
    'duello': ('Üslü Sayı Düellosu', 'Üslü İfadeler', 30),
    'maarif': ('Maarif Radarı (LGS 2028)', 'Yeni Müfredat', 40),
}

def sinifla(slug, baslik):
    """slug -> (seri_id, seri_sira, kısa başlık)"""
    for tip in ('iki-kare-farki', 'arti-kare', 'eksi-kare'):
        if slug.endswith(tip):
            b = BOLGE[slug[:-len(tip) - 1]]
            return tip, list(BOLGE).index(slug[:-len(tip) - 1]) + 1, f'{SERILER[tip][0].split("  ")[1]} · {b} teması'
    m = re.match(r'tum-av-(\d+)$', slug)
    if m: n = int(m[1]); return 'tum-av', n, re.sub(r'^Mathlemur ', '', baslik)
    if slug == 'kok-avcisi-v3': return 'kok-avcisi', 1, re.sub(r'^Mathlemur ', '', baslik)
    m = re.match(r'kok-avcisi-b(\d+)$', slug)
    if m: return 'kok-avcisi', int(m[1]), re.sub(r'^Mathlemur ', '', baslik)
    m = re.match(r'duello-(\d+)$', slug)
    if m: return 'duello', int(m[1]), re.sub(r'\^(\d+)', lambda x: x[1].translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')), baslik)
    m = re.match(r'lgs28-(\d+)-', slug)
    if m: return 'maarif', int(m[1]), re.sub(r'^Maarif Radarı \d+: ', '', baslik)
    return None, 0, baslik

def sure(p): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode())

def sikistir(src, dst):
    # 720x1280, H.264 yüksek profil, ~0.8-1.1 Mbps, aac 96k, faststart. Sağ alttaki filigran videoya zaten gömülü.
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', 'scale=720:1280:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow',
                           '-crf', '27', '-maxrate', '1100k', '-bufsize', '2200k', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-c:a', 'aac', '-b:a', '96k',
                           '-movflags', '+faststart', '-map_metadata', '-1', dst])

def main():
    os.makedirs(f'{HEDEF}/video', exist_ok=True); os.makedirs(f'{HEDEF}/kapak', exist_ok=True)
    liste = []
    for pj in sorted(glob.glob(f'{R}/icerik/*/post.json')):
        slug = os.path.basename(os.path.dirname(pj)); p = json.load(open(pj, encoding='utf-8'))
        src = f'{R}/yayin/video/{slug}.mp4'
        if not os.path.exists(src): continue
        if p.get('durum') != 'yayinlandi' and slug not in EK: continue
        seri, sira, kisa = sinifla(slug, p.get('baslik', slug))
        if not seri: continue
        dst, kap = f'{HEDEF}/video/{slug}.mp4', f'{HEDEF}/kapak/{slug}.jpg'
        if not os.path.exists(dst): sikistir(src, dst)
        if not os.path.exists(kap):
            subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(KAPAK_SN), '-i', dst, '-frames:v', '1', '-vf', 'scale=405:720', '-q:v', '4', kap])
        s_ad, konu, s_sira = SERILER[seri]
        liste.append(dict(id=slug, seri=seri, seri_adi=s_ad, konu=konu, seri_sirasi=s_sira, bolum=sira, baslik=kisa, video=f'video/{slug}.mp4', kapak=f'kapak/{slug}.jpg',
                          sure_sn=round(sure(dst), 1), boyut_mb=round(os.path.getsize(dst) / 1048576, 2), yayin_durumu=p.get('durum'), yayin_zamani=p.get('yayin_zamani', ''),
                          aciklama=(p.get('caption', '').split('\n\n')[0])[:240]))
    liste.sort(key=lambda x: (x['seri_sirasi'], x['bolum']))
    json.dump({'surum': 1, 'video_sayisi': len(liste), 'videolar': liste}, open(f'{HEDEF}/manifest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(liste), 'video;', round(sum(x['boyut_mb'] for x in liste), 1), 'MB toplam')

if __name__ == '__main__': main()
