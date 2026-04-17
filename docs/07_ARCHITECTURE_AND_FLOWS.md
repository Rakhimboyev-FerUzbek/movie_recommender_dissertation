# 07. Arxitektura va flow diagrammalari

## 7.1. System architecture

```mermaid
flowchart TD
    U[User / Browser] --> T[Django Templates UI]
    T --> V1[apps.users.views]
    T --> V2[apps.movies.views]
    T --> V3[apps.interactions.views]
    T --> V4[apps.recommendations.views]

    V1 --> DB[(PostgreSQL)]
    V2 --> DB
    V3 --> DB
    V4 --> S[RecommendationService]

    S --> R[RuntimeRepository]
    R --> DB
    R --> C[Django Cache]

    V2 --> M[MEDIA_ROOT / media files]

    CMD1[seed_movielens] --> DB
    CMD2[enrich_tmdb_movies] --> TMDB[TMDB API]
    CMD2 --> DB
    CMD3[fetch_all_trailer_urls] --> TMDB
    CMD3 --> DB
    CMD4[cache_movie_posters] --> DB
    CMD4 --> IMG[TMDB Image CDN]
    CMD4 --> M

    GH[GitHub Repository] --> CI[GitHub Actions CI]
    CI --> RD[Render Deploy]
```

## 7.2. HTTP request flow

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant DjangoView
    participant Service
    participant DB
    participant Template

    User->>Browser: Sahifani ochadi
    Browser->>DjangoView: HTTP request
    DjangoView->>DB: Kerakli ma'lumotlarni oladi
    DjangoView->>Service: Recommendation kerak bo'lsa service chaqiriladi
    Service->>DB: Ratings va movie ma'lumotlari olinadi
    Service-->>DjangoView: Tavsiyalar qaytariladi
    DjangoView->>Template: Context uzatiladi
    Template-->>Browser: HTML response
    Browser-->>User: Sahifa ko'rsatiladi
```

## 7.3. Recommendation pipeline

```mermaid
flowchart TD
    A[User tanlandi] --> B[RuntimeRepository.load]
    B --> C[movies_df va ratings_df tayyorlanadi]
    C --> D[user_item_matrix]
    C --> E[content profiles]
    C --> F[item similarity]
    C --> G[svd prediction]

    D --> H[Model selection]
    E --> H
    F --> H
    G --> H

    H --> I{requested model}
    I -->|popularity| J[popularity_scores]
    I -->|content| K[content_scores]
    I -->|item| L[item_scores]
    I -->|svd| M[svd_scores]
    I -->|hybrid| N[hybrid_scores]
    I -->|auto| O[resolve_auto_model]
    O --> I

    J --> P[materialize_items]
    K --> P
    L --> P
    M --> P
    N --> P

    P --> Q[build_explanation_payload]
    Q --> R[UI da recommendation cards]
    Q --> S[Movie detail explainability block]
```

## 7.4. Data bootstrap flow

```mermaid
flowchart TD
    A[Clone repository] --> B[Create .env]
    B --> C[Install dependencies]
    C --> D[Create PostgreSQL database]
    D --> E[python manage.py migrate]
    E --> F[seed_movielens]
    F --> G[enrich_tmdb_movies]
    G --> H[fetch_all_trailer_urls]
    H --> I[seed_rating_reviews]
    I --> J[fill_random_profile_data]
    J --> K[create_admin]
    K --> L[cache_movie_posters]
    L --> M[runserver]
```

## 7.5. Poster pipeline flow

```mermaid
flowchart LR
    A[Movie record] --> B[enrich_tmdb_movies]
    B --> C[poster_url saved in DB]
    C --> D[cache_movie_posters]
    D --> E[download image file]
    E --> F[save to media/movies/posters]
    F --> G[poster_image saved in DB]
    G --> H[template uses poster_src]
    C --> H
```

## 7.6. Deploy / CI flow

```mermaid
flowchart LR
    A[Developer pushes code to GitHub] --> B[.github/workflows/ci.yml]
    B --> C[Install dependencies]
    C --> D[manage.py check]
    D --> E[makemigrations --check --dry-run]
    E --> F[migrate]
    F --> G[collectstatic]
    G --> H[CI success]
    H --> I[Render build.sh]
    I --> J[pip install -r requirements/prod.txt]
    J --> K[collectstatic]
    K --> L[migrate]
    L --> M[gunicorn config.wsgi:application]
```

## 7.7. Nega shu arxitektura tanlangan?

- Django Templates kichik va o'rta hajmdagi BMI loyihasi uchun sodda va tez integratsiya qiladi.
- PostgreSQL relational interaction datasi uchun mos.
- Recommendation engine'ni app ichida alohida modulga ajratish maintainability beradi.
- TMDB API movie metadata va trailer/poster kabi boyituvchi ma'lumotlarni beradi.
- Poster cache qatlamı tashqi image host'ga bog'liqlikni kamaytiradi.
- GitHub Actions va Render bilan deploy pipeline soddalashtirilgan.
