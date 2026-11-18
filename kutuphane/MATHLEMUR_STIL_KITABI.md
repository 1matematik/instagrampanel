# Mathlemur Stil Kitabı — 1matematik kurumsal kimlik ve üretim algoritması

Son güncelleme: 2026-11-19 (02:30). Kullanıcının gönderdiği HER içerik bu kitaba göre yeniden tasarlanır. Kaynak ne olursa olsun çıktı tek elden, aynı imzayla çıkar. Başkasının tasarımı, metni veya görseli kopyalanmaz. Sadece matematik fikri alınır.

> Bu dosyanın asıl kopyası claude.ai projesindedir ("İNSTAGRAM YÖNETİM PANELİ" → claude/mathlemur-stil-kitabi.md). Buradaki kopya onunla aynı tutulur.

## 0. Kullanıcı kararları (19 Kas)
- **Tasarım v4 ONAYLANDI** ("olay budur işte"): aşağıdaki kimlik ve görsel dil nihai kalıptır. Kod: `yayin/v4_yama.py` (şablon sahneye uygulanan yama; `yayin/kok_uret.py` otomatik uygular).
- **Çalışma şekli:** Tasarım değişiklikleri önce GÖRSEL (kare kolajı) üzerinde gösterilir ve düzeltilir; video ancak görsel beğenilince üretilir. Kullanıcı görsel üzerinden brif de verebilir.
- **Günlük içerik sayısı: 10.** Onay olmadan yayın yok.
- **Ses: Charon** tüm tasarımlarda (sesli-video varsayılanı).
- **İçerik zenginleştirme (unutma):** Kural kartı (ör. √(a·b) = √a·√b), kırmızı çerçeveli Dikkat / yaygın hata anı, adım adım defter satırları, güçlü kapak sorusu, konuya göre farklı görsel modeller (ızgara, alan, sayı doğrusu, terazi).
- **Canva:** Bağlı (19 Kas doğrulandı, marka kiti yok). Statik tasarım ve görsel brif için kullanılabilir; videolar kendi kod sistemimizde üretilir.

## 1. Kimlik
- **Kahraman:** Mathlemur. Gri lemur, halkalı siyah-beyaz kuyruk, yuvarlak siyah çerçeveli gözlük, mavi gözler, pembe yanaklar. Karnında yazı yok.
- **Yüz (v4):** İki MİNİK tavşan dişi (kullanıcı %50 küçülttürdü; büyük diş çirkin bulundu). Konuşurken pembe ağız içi ve küçük kırmızı dil. Arada göz kırpıp küçük kırmızı dilini çıkarır (açılış, ilk sonuç, kapanış). Şaşırınca gözleri büyür.
- **Hareket (v4):** Kuyruk belirgin sallanır. Sahne geçişlerinde sağa/sola küçük zıplama. İkinci sonuçta SAĞ ekran kenarına, "Yarın yine buluşalım"da SOL kenara tutunur (belgesel tadında, yarısı ekran dışında, hafif yan yatık). **Salto/takla ve amuda kalkma YOK** (kullanıcı reddetti). Hareketler kısa, dikkat dağıtmaz.
- **Kişilik:** Meraklı, enerjik, sevimli, avcı.
- **Ses:** Gemini TTS Charon. Ücretsiz kotada **video başına tek istek** (tüm metin tek seferde okunur, sessizliklerden cümlelere bölünür; ses/gemini_tts.py). Ücretsiz kota ~10 istek/gün, ≈11:00 TRT'de yenilenir → günde ~10 video. Pro üyelik API kotası vermez; faturalandırma kapalı. Yedek: Edge tr-TR-AhmetNeural.
- **Logo:** Beyin-böcek logosu, saydam (%42), tüm video boyunca süzülür (yayin/filigran.py, otomatik).

## 2. Görsel dil
- **Zemin:** Koyu lacivert degrade (#06162e → #10386c), ince ızgara, süzülen matematik sembolleri, ışık süpürmesi, vinyet.
- **Renkler:** Altın #f6c945, Camgöbeği #6ee7ff, Beyaz #f5f7fb, Mürekkep #071a33, Uyarı kırmızısı (Dikkat anı).
- **Renk kuralı:** Altın = "dışarı çıkan / tam kare", camgöbeği = "içeride kalan".
- **Başlık (v4):** "MATHLEMUR" altın, ışıltılı (glow), "KÖK AVCISI"ndan ayrık ve biraz yukarıda (y≈268); seri adı beyaz ışıltılı. Üstte "BÖLÜM n" (y≈168) ve ince ilerleme çubuğu.
- **Alt rozet (v4):** "MATHLEMUR" yazısı altta YOK. Yerine cam (glass, iPhone/iPad estetiği) rozet içinde **www.sariakademi.com** ("sariakademi" altın), ışıltılı yazı, üstünden süzülen ışık, köşelerde parlayan yıldızlar, altta ince camgöbeği çizgi.
- **Kapanış butonu (v4):** Cam (glass) "KAYDET • TAKİP ET": yarı saydam, beyaz kenar, gölge, yer imi ve artı ikonları, dönerek giriş, ışık süpürmesi, yıldız parıltıları.
- **Hareket:** Yavaş kamera zoom'u, vurgu anlarında punch-in, konfeti ve şok halkası.
- **Altyazı:** Karaoke tarzı, konuşulan kelime altın.

## 3. Bölüm iskeleti (~40–45 sn)
1. Açılış: "Geçen cevap: …" ya da merak sorusu.
2. 1. örnek (görsel modelle).
3. 2. örnek (daha hızlı).
4. Kural kartı / Dikkat anı (zenginleştirme).
5. Sıra sende: soru, ipucu, "Cevabı yorumlara yaz ↓".
6. Kapanış: "Yarın yine buluşalım!", cam buton.

## 4. Anlatım kuralları
- 7–9 cümle, her cümle tek fikir, en fazla ~12 kelime. Emir ve oyun dili: çiz, yakala, at, böl, say.
- Sayılar yazıyla okunur, ekranda sembolle gösterilir.
- İmza cümleleri: "Merhaba, ben Matlemur!" (telaffuz için metinde "Matlemur"), "Sıra sende!", "Yarın yine buluşalım!"

## 5. Ses ve müzik
- Arşiv: kutuphane/muzik/ (12 Pixabay parçası), dönüşümlü (ses.json "muzik_dosya"). Efektler ses.json'da.

## 6. Paylaşım
- Sadece Reels. En fazla 5 etiket. Açıklama: sonuç özeti, "Sıra sende" sorusu, "Kaydet, LGS'de lazım olur 📌", "Her gün matematik için takip et 👆".
- Saatler yoğun saatlere. Kullanıcı onayı olmadan yayın yok.

## 7. Gelen içeriği dönüştürme algoritması
1. Çekirdek fikri tek cümleyle yaz.
2. Kolaydan zora 2'li örnek grupları; her "Sıra sende" bir sonraki bölümü açar.
3. Hareketli görsel model seç.
4. En yaygın öğrenci hatasını bul; en az bir "Dikkat" bölümü.
5. Kaynağın düzenini, rengini, sayılarını, metnini kullanma.
6. Her sonucu hesapla, kareleri kontrol et, önce görseli onaya sun.
