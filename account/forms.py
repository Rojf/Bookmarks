from django import forms

from django_countries.fields import CountryField


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    firstname = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=250)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=150)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=150)


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(max_length=250)
    photo = forms.ImageField(required=False)
    confirmed = forms.BooleanField(required=False)


class InfoUserForm(forms.Form):
    bio = forms.CharField(max_length=2000, required=False)
    birthday = forms.DateField(required=False)
    country = CountryField().formfield(required=False)
    phone_number = forms.RegexField(regex=r'(?:([+]\d{1,4})[-.\s]?)?(?:[(](\d{1,3})[)][-.\s]?)?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9})', max_length=15, required=False)


class SocialMediaUserForm(forms.Form):
    twitter = forms.URLField(max_length=200, required=False)
    facebook = forms.URLField(max_length=200, required=False)
    google = forms.URLField(max_length=200, required=False)
    linkedIn = forms.URLField(max_length=200, required=False)
    instagram = forms.URLField(max_length=200, required=False)
