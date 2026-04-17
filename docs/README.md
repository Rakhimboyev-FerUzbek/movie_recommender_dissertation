# Dokumentatsiya markazi

Bu papkada loyiha bo'yicha to'liq texnik dokumentatsiya jamlangan.

## Mavzular

1. `01_PROJECT_OVERVIEW.md` — loyiha maqsadi, scope va asosiy imkoniyatlar
2. `02_SETUP_AND_RUN.md` — lokal muhitda ishga tushirish
3. `03_DATA_INGESTION.md` — dataset, seed, TMDB enrichment va poster cache
4. `04_RECOMMENDATION_ENGINE.md` — AI/recommendation engine arxitekturasi
5. `05_DATABASE_SCHEMA.md` — ER diagram va DB izohlari
6. `06_MANAGEMENT_COMMANDS.md` — barcha management command'lar hujjati
7. `07_ARCHITECTURE_AND_FLOWS.md` — system diagram, request flow, bootstrap flow, deploy flow
8. `08_CLONE_AND_REPRODUCE.md` — repository clone qilib bir xil holatga olib kelish
9. `09_AI_BUILD_STATEMENT.md` — AI-based loyiha haqida rasmiy statement
10. `FOLDER_TREE.md` — loyiha papkalar strukturasi

## Diagrammalar

Raw diagram fayllari:

- `diagrams/system_architecture.mmd`
- `diagrams/database_erd.mmd`
- `diagrams/recommendation_flow.mmd`
- `diagrams/bootstrap_flow.mmd`
- `diagrams/deployment_flow.mmd`

## JSON flow tavsiflari

- `flows/bootstrap_flow.json`
- `flows/recommendation_pipeline.json`
- `flows/tmdb_enrichment_flow.json`

## Ushbu versiyada muhim yangilanish

Dokumentatsiya poster cache tizimiga moslashtirilgan:

- `sync_tmdb_posters` endi asosiy bootstrap ketma-ketligining majburiy qismi sifatida ko'rsatilmaydi;
- `enrich_tmdb_movies` poster URL'ni tayyorlaydigan asosiy enrichment command sifatida tavsiflangan;
- `cache_movie_posters` lokal media poster storage bosqichi sifatida qo'shilgan;
- ER diagram va system flow diagramlarida `poster_image` va media storage qatlamlari yoritilgan.
