from django import forms

from accounts.models import CustomUser


class CustomUserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        # these fields are rerquired
        fields = [
            "email",
            "username",
            "role",
            "first_name",
            "last_name",
            # "mobile_number",
            "password",
        ]
