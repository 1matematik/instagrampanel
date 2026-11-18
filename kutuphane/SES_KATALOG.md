# Ses deposu kataloğu (E:\CLAUDE DEPO\SOUND, 48 mp3)
Dosyalar telif/boyut nedeniyle repoda değil; panelde `lib/depo/` altında tutulur.

- **Ritim/davul/logo (müzik yatağı, vurgu):** alexzavesa-*drums* (4–7 sn), alien_i_trust-*hi-hat* (125 bpm), bombinsound-drum-energetic-logo, studioproject-stomp-energetic-sports-logo, prettysleepy-electronic-drum-loop (31 sn)
- **Bilim/matematik müzik yatağı:** mfcc-science-science-music (20 sn), prettyjohn1-science_32sec (32 sn), olenchic-3 (15 sn)
- **Gerilim/geri sayım:** audioatlant-* (20–33 sn), kave_msri-10sec-digital-countdown, u_lfmkadc0ha-timer_countdown, motionfoxi-countdown-deep-voice, flutie8211-ticking-clock
- **Doğru/yanlış/oyun efekti:** dragon-studio-correct, tuomas_data-the-correct-answer, u_ntlsbh1e81-jawab-soal, floraphonic-arcade-ui-18 | wrong-47985, error-2, negative_beeps, u_n2rdb8hxnh-incorrect, eritnhut1992-buzzer, lose_funny_retro
- **Kutlama/kalabalık:** applause (emircanalp, soumages), small-claps, crowd-with-a-slow-beat, crowd-laughing, 90s-sitcom-laugh-track, shrek_30-pop-wow
- **Geçiş/sihir/gerilim:** primalhousemusic-swelling-transition, magical-sound-effect (19 sn), thunder, soundreality-fall-in / arcade-arped, binary-code-interface (98 sn, UI sesleri)
- **Komik:** funny-comedy-sneaky-music, giggling, old-man-laughing, baby-crying, censor, halloween-funny-horror

## Pixabay müzik listesi (kullanıcı önerisi, karışık kullanılacak)
Durum: bağlantılar kayıtlı; mp3 dosyaları henüz kütüphanede DEĞİL (sandbox pixabay.com'a erişemiyor, dosyaların kullanıcıdan gelmesi gerekir).
Kural: videolarda bu parçalar karışık/dönüşümlü kullanılır; narration üstünde düşük ses (~%12-15).
- https://pixabay.com/users/ikoliks_aj-48415707/ (sanatçı sayfası)
- https://pixabay.com/music/pop-upbeat-upbeat-music-627648/
- https://pixabay.com/users/hitslab-47305729/ (kullanıcının en çok önerdiği sanatçı, öncelikli)
- https://pixabay.com/music/corporate-upbeat-upbeat-music-602444/
- https://pixabay.com/music/corporate-upbeat-corporate-632760/
- https://pixabay.com/music/upbeat-upbeat-607558/

## Arşivdeki Pixabay müzikleri (repoda, workflow kullanabilir): kutuphane/muzik/
- sub_clair-upbeat-607558.mp3 — "Upbeat" (Sub_Clair), 1:56, Pixabay lisansı. Kullanıcı arşive ekledi (18 Kas). Karışık kullanım listesindeki 607558 numaralı parça.
- Arşive 18 Kas'ta eklenen 11 parça daha (kutuphane/muzik/, hepsi Pixabay): aberrantrealities-generally-joyful-261305 (2:08), alex_makemusic-summer-music-461169 (1:43), atlasaudio-short-trailer-617605 (2:04), audiocoffee-childrens-team-124790 (1:56), kulakovka-instagram-291452 (1:51), kulakovka-instagram-295898 (2:15), petrushkasound-upbeat-funky-background-music-428570 (2:09), thesilentthunder-happy-corporate-short-627011 (1:21), tunetank-happy-ukulele-for-children-349736 (1:55), white_records-background-perky-music-...-1min-163720 (1:00), white_records-cheerful-music-...-170013 (0:30).
- Kullanım: ses.json'a "muzik_dosya" (+ opsiyonel "muzik_baslangic" sn) yazılır; ses/muzik_dosya.py müziği süreye kırpar. Seride karışık/dönüşümlü seçilecek.
