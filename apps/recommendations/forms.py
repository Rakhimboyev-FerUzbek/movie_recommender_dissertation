from django import forms
from django.contrib.auth import get_user_model

from config.translations import get_translation


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
    user_id = forms.ChoiceField(required=False, label="Target user")
    model = forms.ChoiceField(choices=MODEL_CHOICES, initial="hybrid", label="Model")
    scenario = forms.ChoiceField(choices=SCENARIO_CHOICES, initial="normal", label="Scenario")
    top_k = forms.IntegerField(required=False, min_value=1, initial=30, label="Top-K")

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("current_user", None)
        lang = kwargs.pop("lang", "uz")
        self.t = get_translation(lang)

        super().__init__(*args, **kwargs)

        user_choices = []
        for user in User.objects.order_by("date_joined", "id").only("id", "username", "date_joined"):
            user_choices.append((str(user.id), user.username))

        self.fields["user_id"].label = self.t.get("username", "Username")
        self.fields["model"].label = self.t.get("model", "Model")
        self.fields["scenario"].label = self.t.get("scenario", "Scenario")
        self.fields["top_k"].label = self.t.get("top_k", "Top-K")

        self.fields["user_id"].choices = user_choices
        self.fields["scenario"].choices = [
            ("normal", self.t.get("normal_scenario", "Normal scenario")),
            ("new_user", self.t.get("new_user_cold_start", "New user cold start")),
        ]

        self.fields["user_id"].widget.attrs.update({"class": "form-select"})
        self.fields["model"].widget.attrs.update({"class": "form-select"})
        self.fields["scenario"].widget.attrs.update({"class": "form-select"})
        self.fields["top_k"].widget.attrs.update(
            {
                "class": "form-control",
                "min": 1,
                "placeholder": "10",
            }
        )

        if current_user and not self.is_bound:
            self.initial.setdefault("user_id", str(current_user.id))

    def clean_user_id(self):
        user_id = self.cleaned_data.get("user_id")
        if user_id in (None, ""):
            return None
        if not User.objects.filter(pk=user_id).exists():
            raise forms.ValidationError(self.t.get("user_not_found", "User not found."))
        return int(user_id)

    def clean_top_k(self):
        top_k = self.cleaned_data.get("top_k")
        if top_k in (None, ""):
            return None
        return int(top_k)
