# Instagram Yönetim Paneli

Akış: kaynak (link/görsel) -> Claude üretir (icerik/<slug>/) -> taslak videoyu kullanıcıya gösterir
-> kullanıcı onaylar -> `panel.mjs onayla` -> git push -> GitHub Actions (yayin.yml) Instagram'a yayınlar.

Durumlar: taslak -> onay-bekliyor -> onaylandi -> yayinlaniyor -> yayinlandi | hata

Komutlar: node panel.mjs durum | yeni <ascii-slug> <tur> | render <slug> | onayla <slug> | iptal <slug>
Türler: kural, ornek-soru, cozum, dusunme, zeka-oyunu, uyarlama

Gerekli GitHub Secrets: IG_USER_ID, IG_TOKEN (Instagram Graph API, Business/Creator hesap).
Yayın kodu (yayin/publish.mjs) henüz gerçek hesapta denenmedi; yalnızca --dry-run test edildi.

## Gizlilik
Bu depo herkese açıktır. Anahtarlar (IG_USER_ID, IG_TOKEN, GEMINI_API_KEY) yalnızca GitHub > Settings > Secrets bölümünde tutulur, depoya yazılmaz.
Videolar depoya yalnızca onaylandıktan sonra eklenir (Instagram videoyu bu adresten çeker).
