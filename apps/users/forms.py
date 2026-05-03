from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from apps.movies.models import Genre
from apps.users.models import UserProfile
from config.translations import get_translation


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        lang = kwargs.pop("lang", None)

        if lang is None and request is not None:
            lang = request.session.get("site_language", "uz")

        self.lang = lang or "uz"
        self.t = get_translation(self.lang)

        super().__init__(*args, **kwargs)

        self.apply_translations()
        self.apply_bootstrap()

    def tr(self, key, default=None):
        if default is None:
            default = key.replace("_", " ").title()
        return self.t.get(key, default)

    def apply_translations(self):
        pass

    def apply_bootstrap(self):
        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.Textarea):
                css_class = "form-control form-textarea"
            elif isinstance(widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(widget, forms.CheckboxSelectMultiple):
                css_class = ""
            else:
                css_class = "form-control"

            existing_class = widget.attrs.get("class", "").strip()
            if css_class:
                widget.attrs["class"] = f"{existing_class} {css_class}".strip()

            if field.required and not isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                widget.attrs["required"] = "required"

            if not isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                widget.attrs.setdefault("placeholder", field.label or field_name.replace("_", " ").title())

        if "password" in self.fields:
            self.fields["password"].widget.attrs["autocomplete"] = "current-password"

        if "password1" in self.fields:
            self.fields["password1"].widget.attrs["autocomplete"] = "new-password"

        if "password2" in self.fields:
            self.fields["password2"].widget.attrs["autocomplete"] = "new-password"


class LoginForm(StyledFormMixin, AuthenticationForm):
    def apply_translations(self):
        username_label = self.tr("username", "Username")
        password_label = self.tr("password", "Password")

        self.fields["username"].label = username_label
        self.fields["password"].label = password_label

        self.fields["username"].widget.attrs["placeholder"] = username_label
        self.fields["password"].widget.attrs["placeholder"] = password_label

        self.error_messages["invalid_login"] = self.tr("invalid_login", "Invalid username or password.")
        self.error_messages["inactive"] = self.tr("inactive_account", "This account is inactive.")


class RegisterForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    phone_number = forms.CharField(max_length=20, required=True)
    gender = forms.ChoiceField(
        required=True,
        choices=UserProfile.GENDER_CHOICES,
    )
    preferred_genres = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "phone_number",
            "gender",
            "preferred_genres",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        genre_names = list(Genre.objects.order_by("name").values_list("name", flat=True))
        self.fields["preferred_genres"].choices = [(name, name) for name in genre_names]

        self.fields["phone_number"].widget.attrs.update({
            "inputmode": "tel",
            "autocomplete": "tel",
        })

        self.fields["birth_date"].widget.attrs.update({
            "autocomplete": "bday",
        })

    def apply_translations(self):
        self.fields["username"].label = self.tr("username", "Username")
        self.fields["email"].label = self.tr("email", "Email")
        self.fields["first_name"].label = self.tr("first_name", "First name")
        self.fields["last_name"].label = self.tr("last_name", "Last name")
        self.fields["birth_date"].label = self.tr("birth_date", "Birth date")
        self.fields["phone_number"].label = self.tr("phone_number", "Phone number")
        self.fields["gender"].label = self.tr("gender", "Gender")

        self.fields["gender"].choices = [
            (UserProfile.MALE, self.tr("male", "Male")),
            (UserProfile.FEMALE, self.tr("female", "Female")),
        ]

        self.fields["preferred_genres"].label = self.tr("preferred_genres", "Preferred genres")
        self.fields["password1"].label = self.tr("password", "Password")
        self.fields["password2"].label = self.tr("confirm_password", "Confirm password")

        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(self.tr("email_already_registered", "This email is already registered."))
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"].strip()
        digits_only = "".join(ch for ch in phone if ch.isdigit())

        if len(digits_only) < 9:
            raise forms.ValidationError(
                self.tr("phone_number_invalid", "Phone number is invalid. It must contain at least 9 digits.")
            )
        return phone

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]
        today = timezone.localdate()

        if birth_date > today:
            raise forms.ValidationError(
                self.tr("birth_date_future_invalid", "Birth date cannot be in the future.")
            )

        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 10:
            raise forms.ValidationError(
                self.tr("minimum_age_invalid", "You must be at least 10 years old to register.")
            )

        return birth_date

    def clean_preferred_genres(self):
        genres = self.cleaned_data.get("preferred_genres") or []
        if not genres:
            raise forms.ValidationError(
                self.tr("preferred_genres_required", "Select at least one preferred genre.")
            )
        return genres

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip().lower()
        user.first_name = self.cleaned_data.get("first_name", "").strip()
        user.last_name = self.cleaned_data.get("last_name", "").strip()

        if commit:
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.birth_date = self.cleaned_data["birth_date"]
            profile.phone_number = self.cleaned_data["phone_number"].strip()
            profile.gender = self.cleaned_data["gender"]
            profile.preferred_genres = self.cleaned_data.get("preferred_genres", [])
            profile.save()

            user.profile = profile

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
        self.fields["first_name"].label = self.tr("first_name", "First name")
        self.fields["last_name"].label = self.tr("last_name", "Last name")
        self.fields["email"].label = self.tr("email", "Email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = User.objects.filter(email__iexact=email)

        if self.user_instance:
            qs = qs.exclude(pk=self.user_instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                self.tr("email_already_used", "This email is already being used by another user.")
            )
        return email


class UserProfileForm(StyledFormMixin, forms.ModelForm):
    preferred_genres = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    remove_profile_photo = forms.BooleanField(required=False)

    class Meta:
        model = UserProfile
        fields = ("bio", "birth_date", "phone_number", "gender", "profile_photo")

    def apply_translations(self):
        self.fields["bio"].label = self.tr("bio", "Bio")
        self.fields["birth_date"].label = self.tr("birth_date", "Birth date")
        self.fields["phone_number"].label = self.tr("phone_number", "Phone number")
        self.fields["gender"].label = self.tr("gender", "Gender")
        self.fields["profile_photo"].label = self.tr("profile_photo", "Profile photo")
        self.fields["preferred_genres"].label = self.tr("preferred_genres", "Preferred genres")
        self.fields["remove_profile_photo"].label = self.tr("remove_profile_photo", "Remove profile photo")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        genre_names = list(Genre.objects.order_by("name").values_list("name", flat=True))
        self.fields["preferred_genres"].choices = [(name, name) for name in genre_names]

        if self.instance and self.instance.preferred_genres:
            self.fields["preferred_genres"].initial = self.instance.preferred_genres

        self.fields["birth_date"].widget = forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "autocomplete": "bday",
            }
        )

        self.fields["phone_number"].widget.attrs.update({
            "inputmode": "tel",
            "autocomplete": "tel",
        })

        self.fields["profile_photo"].widget = forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": "image/*",
            }
        )

        self.fields["remove_profile_photo"].widget.attrs["class"] = "form-check-input"

    def clean_phone_number(self):
        phone = (self.cleaned_data.get("phone_number") or "").strip()
        if phone:
            digits_only = "".join(ch for ch in phone if ch.isdigit())
            if len(digits_only) < 9:
                raise forms.ValidationError(
                    self.tr("phone_number_invalid", "Phone number is invalid. It must contain at least 9 digits.")
                )
        return phone

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        if birth_date and birth_date > timezone.localdate():
            raise forms.ValidationError(
                self.tr("birth_date_future_invalid", "Birth date cannot be in the future.")
            )
        return birth_date

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.preferred_genres = self.cleaned_data.get("preferred_genres", [])

        if self.cleaned_data.get("remove_profile_photo"):
            profile.profile_photo = None

        if commit:
            profile.save()

        return profile