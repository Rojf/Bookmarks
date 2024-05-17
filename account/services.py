from django.contrib.auth import forms

from account.repositories.Repository import (UserRepository, ProfileRepository, InfoUserRepository,
                                             SocialMediaUserRepository)
from account import forms as account_forms


def get_registration_form(data):
    return account_forms.RegistrationForm(data)


def profile_form(data):
    return account_forms.ProfileForm(data)


def info_user_form(data):
    return account_forms.InfoUserForm(data)


def social_media_form(data):
    return account_forms.SocialMediaUserForm(data)


def user_create(cleaned_data):
    username = cleaned_data.get('username')
    email = cleaned_data.get('email')
    firstname = cleaned_data.get('firstname')
    password = cleaned_data.get('password')

    user = UserRepository.model.objects.create_user(username, email, password, first_name=firstname)
    user.save()

    create_profile(user)
    create_info_user(user)
    create_social_media_user(user)


def create_profile(*args, **kwargs):
    return ProfileRepository.create(*args, **kwargs)


def create_info_user(*args, **kwargs):
    return InfoUserRepository.create(*args, **kwargs)


def create_social_media_user(*args, **kwargs):
    return SocialMediaUserRepository.create(*args, **kwargs)


def clean_password2(self):
    """Reject password2 that differ from the password."""
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")

    if password1 and password2 and password1 != password2:
        raise forms.ValidationError(
            password2.error_messages["password_mismatch"],
            code="password_mismatch",
        )
    return password1


def clean_username(self):
    """Reject usernames that differ only in case."""
    username = self.cleaned_data.get("username")

    if (
        username
        and UserRepository.model.objects.filter(username__iexact=username).exists()
    ):
        forms.ValidationError({"username": ""})
    else:
        return username


def clean_email(self):
    """Reject email that differ only in case."""
    email = self.cleaned_data.get("email")
    if (
        email
        and UserRepository.model.objects.filter(email=email).exists()
    ):
        forms.ValidationError({"email": ""})
    else:
        return email
