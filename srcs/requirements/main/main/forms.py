# forms.py
from django import forms
from account.models import User
from django.core.exceptions import ValidationError


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="E-posta adresi")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Bu e-posta adresi kayıtlı değil.")
        return email
