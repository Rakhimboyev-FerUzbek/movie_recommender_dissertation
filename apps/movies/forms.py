from django import forms

from apps.movies.models import Genre, Movie


SORT_CHOICES = [
    ("", "Standart"),
    ("rating_desc", "Reyting bo'yicha"),
    ("year_desc", "Yil bo'yicha (yangi)"),
    ("year_asc", "Yil bo'yicha (eski)"),
    ("count_desc", "Baho soni bo'yicha"),
    ("title_asc", "Nom bo'yicha (A-Z)"),
    ("title_desc", "Nom bo'yicha (Z-A)"),
]


class MovieFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Qidiruv",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Film nomi bo'yicha qidiring...",
                "autocomplete": "off",
            }
        ),
    )

    year = forms.ChoiceField(
        required=False,
        label="Yil",
        choices=[],
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    genre = forms.ModelMultipleChoiceField(
        required=False,
        label="Janrlar",
        queryset=Genre.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    sort = forms.ChoiceField(
        required=False,
        label="Saralash",
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["genre"].queryset = Genre.objects.order_by("name")

        years = (
            Movie.objects.filter(is_active=True)
            .exclude(release_year__isnull=True)
            .values_list("release_year", flat=True)
            .distinct()
            .order_by("-release_year")
        )
        self.fields["year"].choices = [("", "Barcha yillar")] + [(str(y), str(y)) for y in years]