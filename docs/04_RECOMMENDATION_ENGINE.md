# 04. Recommendation engine dokumentatsiyasi

## 4.1. Recommendation modul joylashuvi

Asosiy recommendation logikasi quyidagi papkada joylashgan:

```text
apps/recommendations/engines/
```

Ichki modullar:

- `constants.py` — model nomlari va scenario constant'lari
- `runtime.py` — runtime dataframe va cache tayyorlash
- `shared.py` — umumiy yordamchi funksiyalar
- `popularity_model.py` — popularity-based ranking
- `content_model.py` — content-based ranking
- `item_model.py` — item-based KNN logic
- `svd_model.py` — latent factor / SVD prediction ranking
- `hybrid_model.py` — weighted hybrid scoring
- `auto_model.py` — auto model tanlash logikasi
- `explainability.py` — recommendation sababini foydalanuvchiga tushuntirish
- `service.py` — tashqi facade bo'lib ishlovchi asosiy service

## 4.2. Tizim qanday ishlaydi?

`RecommendationService` ishga tushganda `RuntimeRepository` orqali quyidagi obyektlarni tayyorlaydi:

- `movies_df`
- `ratings_df`
- `movie_lookup`
- `genre_map`
- `user_item_matrix`
- `item_similarity_df`
- `content_similarity_matrix`
- `svd_prediction_df`

Bu strukturalar cache'ga yoziladi va qayta ishlatiladi.

## 4.3. Model turlari

### 1) Popularity

Filmning ommabopligi va reyting faolligi asosida ishlaydi. `popularity_score` movie agregatlaridan olinadi.

### 2) Content-Based

Movie title, overview, genre, director va cast kabi matnli signal'lar asosida content similarity hisoblaydi.

### 3) Item-Based KNN

User bergan ratinglar bilan o'xshash item'larni topib weighted score hisoblaydi.

### 4) SVD

User-item matrix asosida latent factor predict qilinadi.

### 5) Hybrid

Bir nechta model norm score'larini vaznli yig'indi orqali birlashtiradi.

### 6) Auto

User rating count va scenario'ga qarab avtomatik model tanlaydi.

## 4.4. Hybrid vaznlari

`hybrid_model.py` ichidagi amaldagi weight'lar:

### Normal scenario

- user rating count = 0
  - content: 0.55
  - item: 0.00
  - svd: 0.00
  - popularity: 0.45

- user rating count < 5
  - content: 0.45
  - item: 0.15
  - svd: 0.10
  - popularity: 0.30

- user rating count < 20
  - content: 0.30
  - item: 0.25
  - svd: 0.25
  - popularity: 0.20

- user rating count >= 20
  - content: 0.20
  - item: 0.30
  - svd: 0.35
  - popularity: 0.15

### New user scenario

- content: 0.60
- item: 0.00
- svd: 0.00
- popularity: 0.40

## 4.5. Auto model tanlash logikasi

`auto_model.py` bo'yicha:

- new user bo'lsa: preferred genres bo'lsa content, bo'lmasa popularity;
- rating count = 0: content yoki popularity;
- rating count < 5: content;
- rating count < 15: item yoki hybrid;
- rating count < 30: hybrid;
- ko'proq interaction bo'lsa va prediction mavjud bo'lsa: SVD;
- aks holda: hybrid.

## 4.6. Explainability

Loyiha tavsiyani faqat chiqarib bermaydi, balki detail page'da **nega shu film tavsiya qilingani** haqidagi explanation payload ham shakllantiradi.

Payload ichida odatda quyidagilar bo'ladi:

- explanation text
- matched genres
- reference titles
- evidence
- score breakdown
- formula

Bu BMI nuqtai nazaridan muhim, chunki recommendation system nafaqat natija, balki izohlangan sababni ham beradi.

## 4.7. Recommendation UI sahifalari

### `recommendations/for-you/`

Oddiy foydalanuvchi uchun auto recommendation natijalari.

### `recommendations/lab/`

Faqat `is_staff=True` bo'lgan foydalanuvchilar uchun. Turli user, model, scenario va `top_k` ni tanlab experiment qilish mumkin.

## 4.8. Recommendation engine'ni lokal tekshirish

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from apps.recommendations.services import RecommendationService

User = get_user_model()
user = User.objects.first()
service = RecommendationService()
result = service.recommend_for_user(user=user, model_key="auto", top_k=10, scenario="normal")

print(result["resolved_model"])
for item in result["recommendations"][:5]:
    print(item["movie"].title, item["score"])
```
