from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


MODEL_CHOICES = [
    ("auto", "Auto Hybrid"),
    ("popularity", "Popularity"),
    ("content", "Content-Based"),
    ("item", "Item-Based KNN"),
    ("svd", "SVD"),
    ("hybrid", "Hybrid"),
]

SCENARIO_CHOICES = [
    ("normal", "Normal scenario"),
    ("new_user", "New user cold start"),
]


class RecommendationLabForm(forms.Form):
    user_id = forms.IntegerField(required=False, label="Target user ID")
    model = forms.ChoiceField(choices=MODEL_CHOICES, initial="hybrid", label="Model")
    scenario = forms.ChoiceField(choices=SCENARIO_CHOICES, initial="normal", label="Scenario")
    top_k = forms.IntegerField(min_value=3, max_value=30, initial=10, label="Top-K")

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)

        self.fields["user_id"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Masalan: 1",
            }
        )
        self.fields["model"].widget.attrs.update({"class": "form-select"})
        self.fields["scenario"].widget.attrs.update({"class": "form-select"})
        self.fields["top_k"].widget.attrs.update({"class": "form-control", "min": 3, "max": 30})

        if current_user and not self.is_bound:
            self.initial.setdefault("user_id", current_user.id)

    def clean_user_id(self):
        user_id = self.cleaned_data.get("user_id")
        if user_id in (None, ""):
            return None
        if not User.objects.filter(pk=user_id).exists():
            raise forms.ValidationError("Bunday user topilmadi.")
        return int(user_id)