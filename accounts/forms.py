from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class ClientRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True, max_length=20)
    company_name = forms.CharField(required=False, max_length=150)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "company_name", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CLIENT
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        user.company_name = self.cleaned_data.get("company_name", "")
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "company_name"]
