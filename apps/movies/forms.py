from django import forms

from apps.movies.models import Genre


SORT_CHOICES = [
    ("", "Standart"),
    ("title_asc", "Nom: A-Z"),
    ("title_desc", "Nom: Z-A"),
    ("rating_desc", "Reyting: yuqoridan"),
    ("year_desc", "Yil: eng yangisi"),
]


class MovieFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Qidiruv")
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.none(),
        required=False,
        empty_label="Barcha janrlar",
    )
    year = forms.IntegerField(required=False, label="Yil")
    sort = forms.ChoiceField(required=False, choices=SORT_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["genre"].queryset = Genre.objects.order_by("name")

        self.fields["q"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Film nomi bo‘yicha qidiring...",
        })

        self.fields["year"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Masalan: 1997",
        })