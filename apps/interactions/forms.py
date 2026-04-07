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