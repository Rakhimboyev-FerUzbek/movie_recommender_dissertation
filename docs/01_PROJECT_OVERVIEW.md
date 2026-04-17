# 01. Loyiha umumiy tavsifi

## 1.1. Loyiha nomi

**Online Cinema / Movie Recommender**

## 1.2. Loyiha maqsadi

Mazkur loyiha foydalanuvchiga filmlarni ko'rish, qidirish, baholash, saralash va individual tavsiyalar olish imkonini beruvchi web platformani yaratishga qaratilgan.

Loyiha ikki yo'nalishni birlashtiradi:

1. **Online cinema komponenti** — foydalanuvchi katalog, detail page, trailer, rating, comment, favorite va watch history bilan ishlaydi.
2. **AI-based recommendation komponenti** — foydalanuvchi xatti-harakati va movie metadata asosida tavsiyalar shakllantiriladi.

## 1.3. Asosiy imkoniyatlar

### Foydalanuvchi qismi

- registratsiya va login;
- profilni ko'rish va tahrirlash;
- preferred genres saqlash;
- movie catalog sahifasida qidiruv, janr bo'yicha filter, yil bo'yicha filter, sorting;
- movie detail sahifasi;
- rating va review yozish;
- comment yozish va like bosish;
- favorite ro'yxati;
- watch history yuritish;
- personalized recommendation ko'rish.

### Admin / staff qismi

- admin panel orqali movie va genre boshqaruvi;
- custom `create_admin` command orqali moderator/superuser yaratish;
- recommendation lab sahifasi orqali demo yoki staff rejimda model behavior'ni tahlil qilish.

## 1.4. Asosiy Django app'lar

### `apps/users`

Autentifikatsiya, profil va account management uchun javob beradi.

### `apps/movies`

Movie modeli, katalog, detail page, filter, TMDB enrichment va media bilan ishlaydi.

### `apps/interactions`

Rating, review, favorite, watch history, comment va comment like logikasini saqlaydi.

### `apps/recommendations`

Recommendation engine, auto model tanlash, hybrid scoring, explainability va recommendation UI bilan ishlaydi.

## 1.5. Recommendation engine nega alohida app ichida?

Loyihada recommendation modulini alohida ajratish quyidagi sabablar bilan to'g'ri arxitektura hisoblanadi:

- business logic'ni UI dan ajratadi;
- model turlarini kengaytirishni osonlashtiradi;
- runtime dataframe va scoring pipeline'ni bir joyda saqlaydi;
- explanation payload va recommendation lab funksiyalarini izchil boshqaradi.

## 1.6. Foydalanilgan tashqi manbalar

- **MovieLens 100K** — dastlabki rating va movie seed ma'lumotlari uchun.
- **TMDB API** — movie metadata, poster va trailer ma'lumotlarini boyitish uchun.

## 1.7. Loyiha foydalanuvchi nuqtai nazaridan qanday ishlaydi?

1. User saytga kiradi.
2. Movie katalogdan film tanlaydi.
3. Filmga rating/review qoldiradi yoki favorite qiladi.
4. Bu interaction'lar bazaga yoziladi.
5. Recommendation engine shu signal va metadata asosida tavsiyalar tayyorlaydi.
6. User “For You” sahifasida personal tavsiyalarni ko'radi.
7. Detail sahifada tavsiyaning sababi explainability blokida ko'rsatiladi.
