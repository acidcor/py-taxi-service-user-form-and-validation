from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) < 8:
            return ValidationError(
                "License number should be at least 8 characters long"
            )

        if license_number[:3] != license_number[:3].upper():
            return ValidationError(
                "First 3 characters should be uppercase letters"
            )

        if not license_number[-5:].isdigit():
            return ValidationError(
                "Last 5 characters should be numbers"
            )

        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
