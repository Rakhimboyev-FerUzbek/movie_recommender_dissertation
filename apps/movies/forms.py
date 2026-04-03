from django import forms

from apps.movies.models import Genre
from config.translations import get_translation


class MovieFilterForm(forms.Form):
    q = forms.CharField(required=False)
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.none(),
        required=False,
    )
    year = forms.IntegerField(required=False)
    sort = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop("lang", "uz")
        self.t = get_translation(lang)
        super().__init__(*args, **kwargs)

        self.fields["q"].label = self.t["search"]
        self.fields["genre"].label = self.t["genre"]
        self.fields["year"].label = self.t["year"]
        self.fields["sort"].label = self.t["sort"]

        self.fields["genre"].queryset = Genre.objects.order_by("name")
        self.fields["genre"].empty_label = self.t["all_genres"]

        self.fields["sort"].choices = [
            ("", self.t["default_sort"]),
            ("title_asc", self.t["sort_title_asc"]),
            ("title_desc", self.t["sort_title_desc"]),
            ("rating_desc", self.t["sort_rating_desc"]),
            ("year_desc", self.t["sort_year_desc"]),
        ]

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["q"].widget.attrs["placeholder"] = self.t["search_placeholder"]