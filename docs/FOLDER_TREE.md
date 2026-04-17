# Folder tree

```text
manage.py
README.md
Procfile
render.yaml
build.sh
.github/
└── workflows/
    └── ci.yml
requirements/
├── base.txt
├── dev.txt
└── prod.txt
config/
├── settings/
│   ├── __init__.py
│   ├── base.py
│   ├── ci.py
│   ├── local.py
│   └── production.py
├── __init__.py
├── asgi.py
├── context_processors.py
├── error_views.py
├── translations.py
├── ui_views.py
├── urls.py
└── wsgi.py
apps/
├── interactions/
│   ├── management/
│   │   └── commands/
│   ├── migrations/
│   ├── templates/
│   │   └── interactions/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
├── movies/
│   ├── management/
│   │   └── commands/
│   ├── migrations/
│   ├── services/
│   │   ├── aggregates.py
│   │   ├── media.py
│   │   └── tmdb.py
│   ├── templates/
│   │   └── movies/
│   ├── templatetags/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── recommendations/
│   ├── engines/
│   │   ├── auto_model.py
│   │   ├── constants.py
│   │   ├── content_model.py
│   │   ├── explainability.py
│   │   ├── hybrid_model.py
│   │   ├── item_model.py
│   │   ├── popularity_model.py
│   │   ├── runtime.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   ├── shared.py
│   │   └── svd_model.py
│   ├── templates/
│   │   └── recommendations/
│   ├── forms.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
├── users/
│   ├── management/
│   │   └── commands/
│   ├── migrations/
│   ├── templates/
│   │   └── users/
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
└── README.md
templates/
├── errors/
├── includes/
├── base.html
└── home.html
static/
├── css/
├── images/
└── js/
scripts/
├── README.md
└── split_pages_css.py
docs/
ml-100k/
experiments/
results/
```

## Qisqacha izoh

- `apps/` — asosiy business app'lar
- `config/` — settings va global routing
- `templates/` — umumiy HTML template'lar
- `static/` — CSS, JS va image fayllar
- `docs/` — to'liq texnik dokumentatsiya
- `ml-100k/` — dataset fayllari
- `scripts/` — yordamchi scriptlar
- `experiments/` — offline experiment joyi
- `results/` — metrics va natijalar joyi
