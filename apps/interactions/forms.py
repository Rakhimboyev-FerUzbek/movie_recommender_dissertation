from decimal import Decimal

from django import forms

from apps.interactions.models import Comment, Rating


class RatingForm(forms.ModelForm):
    rating = forms.DecimalField(
        min_value=Decimal("0.5"),
        max_value=Decimal("5.0"),
        decimal_places=1,
        max_digits=2,
        required=True,
    )
    review = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "maxlength": "50",
                "placeholder": "Masalan: Juda zo'r film",
            }
        ),
    )

    class Meta:
        model = Rating
        fields = ("rating", "review")

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        doubled = float(rating) * 2
        if abs(doubled - round(doubled)) > 1e-9:
            raise forms.ValidationError("Reyting 0.5 qadam bilan bo‘lishi kerak.")
        return rating


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Fikringizni yozing...",
            }
        )
    )

    class Meta:
        model = Comment
        fields = ("body",)