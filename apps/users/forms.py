from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from apps.users.models import UserProfile
from config.translations import get_translation


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        request = kwargs.get("request")
        lang = kwargs.pop("lang", None)

        if lang is None and request is not None:
            lang = request.session.get("site_language", "uz")

        self.lang = lang or "uz"
        self.t = get_translation(self.lang)

        super().__init__(*args, **kwargs)
        self.apply_translations()
        self.apply_bootstrap()

    def apply_translations(self):
        pass

    def apply_bootstrap(self):
        for field_name, field in self.fields.items():
            css_class = "form-control form-textarea" if isinstance(field.widget, forms.Textarea) else "form-control"
            existing_class = field.widget.attrs.get("class", "").strip()
            field.widget.attrs["class"] = f"{existing_class} {css_class}".strip()
            field.widget.attrs.setdefault("placeholder", field.label or field_name.replace("_", " ").title())

        if "password" in self.fields:
            self.fields["password"].widget.attrs["autocomplete"] = "current-password"
        if "password1" in self.fields:
            self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        if "password2" in self.fields:
            self.fields["password2"].widget.attrs["autocomplete"] = "new-password"


class LoginForm(StyledFormMixin, AuthenticationForm):
    def apply_translations(self):
        self.fields["username"].label = self.t["username"]
        self.fields["password"].label = self.t["password"]

        self.fields["username"].widget.attrs["placeholder"] = self.t["username"]
        self.fields["password"].widget.attrs["placeholder"] = self.t["password"]

        self.error_messages["invalid_login"] = self.t["invalid_login"]
        self.error_messages["inactive"] = self.t["inactive_account"]


class RegisterForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def apply_translations(self):
        self.fields["username"].label = self.t["username"]
        self.fields["email"].label = self.t["email"]
        self.fields["first_name"].label = self.t["first_name"]
        self.fields["last_name"].label = self.t["last_name"]
        self.fields["password1"].label = self.t["password"]
        self.fields["password2"].label = self.t["confirm_password"]

        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(self.t["email_already_registered"])
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip().lower()
        user.first_name = self.cleaned_data.get("first_name", "").strip()
        user.last_name = self.cleaned_data.get("last_name", "").strip()
        if commit:
            user.save()
        return user


class UserUpdateForm(StyledFormMixin, forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

    def apply_translations(self):
        self.fields["first_name"].label = self.t["first_name"]
        self.fields["last_name"].label = self.t["last_name"]
        self.fields["email"].label = self.t["email"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = User.objects.filter(email__iexact=email)
        if self.user_instance:
            qs = qs.exclude(pk=self.user_instance.pk)
        if qs.exists():
            raise forms.ValidationError(self.t["email_already_used"])
        return email


class UserProfileForm(StyledFormMixin, forms.ModelForm):
    preferred_genres_text = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ("bio", "birth_year")

    def apply_translations(self):
        self.fields["bio"].label = self.t["bio"]
        self.fields["birth_year"].label = self.t["birth_year"]
        self.fields["preferred_genres_text"].label = self.t["preferred_genres"]
        self.fields["preferred_genres_text"].help_text = self.t["preferred_genres_help"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.preferred_genres:
            self.fields["preferred_genres_text"].initial = ", ".join(self.instance.preferred_genres)

    def clean_birth_year(self):
        birth_year = self.cleaned_data.get("birth_year")
        if birth_year is not None and (birth_year < 1900 or birth_year > 2100):
            raise forms.ValidationError(self.t["birth_year_invalid"])
        return birth_year

    def clean_preferred_genres_text(self):
        raw = self.cleaned_data.get("preferred_genres_text", "")
        items = [item.strip() for item in raw.split(",") if item.strip()]
        return items

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.preferred_genres = self.cleaned_data.get("preferred_genres_text", [])
        if commit:
            profile.save()
        return profile