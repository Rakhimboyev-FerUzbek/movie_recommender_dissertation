from django import forms

from apps.interactions.models import Comment


class RatingForm(forms.Form):
    rating = forms.DecimalField(
        min_value=0.5,
        max_value=5.0,
        decimal_places=1,
        max_digits=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0.5",
                "max": "5.0",
                "step": "0.5",
                "placeholder": "Masalan: 4.5",
            }
        ),
    )
    review = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control form-textarea",
                "rows": 4,
                "placeholder": "Qisqa fikr qoldiring (ixtiyoriy)...",
            }
        ),
    )

    def clean_rating(self):
        value = float(self.cleaned_data["rating"])
        doubled = value * 2
        if doubled != round(doubled):
            raise forms.ValidationError("Reyting 0.5 qadam bilan kiritilishi kerak.")
        return value


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control form-textarea",
                    "rows": 4,
                    "placeholder": "Fikringizni yozing...",
                }
            )
        }


class FavoriteFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Film nomi bo'yicha qidiring...",
            }
        ),
    )
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ("recent", "Yangi qo'shilganlar"),
            ("oldest", "Eski qo'shilganlar"),
            ("title_asc", "Nom bo'yicha (A-Z)"),
            ("title_desc", "Nom bo'yicha (Z-A)"),
            ("year_desc", "Yil bo'yicha (yangi)"),
            ("year_asc", "Yil bo'yicha (eski)"),
        ],
        widget=forms.Select(attrs={"class": "form-select interaction-sort-native"}),
    )


class UserRatingFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Film nomi bo'yicha qidiring...",
            }
        ),
    )
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ("recent", "Yaqinda yangilangan"),
            ("oldest", "Eski reytinglar"),
            ("rating_desc", "Reyting bo'yicha (yuqori)"),
            ("rating_asc", "Reyting bo'yicha (past)"),
            ("title_asc", "Nom bo'yicha (A-Z)"),
            ("title_desc", "Nom bo'yicha (Z-A)"),
        ],
        widget=forms.Select(attrs={"class": "form-select interaction-sort-native"}),
    )


class WatchHistoryFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Film nomi bo'yicha qidiring...",
            }
        ),
    )
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ("recent", "Yaqinda ko'rilgan"),
            ("oldest", "Eski ko'rilgan"),
            ("watch_count_desc", "Ko'rish soni bo'yicha"),
            ("title_asc", "Nom bo'yicha (A-Z)"),
            ("title_desc", "Nom bo'yicha (Z-A)"),
        ],
        widget=forms.Select(attrs={"class": "form-select interaction-sort-native"}),
    )