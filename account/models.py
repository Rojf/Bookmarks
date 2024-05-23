from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models

from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'Profile of {self.user.username}'


class InfoUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=2000, blank=True)
    birthday = models.DateField(null=True, blank=True)
    country = CountryField(blank=True)
    phone_number = models.CharField(validators=[RegexValidator(regex=r'(?:([+]\d{1,4})[-.\s]?)?(?:[(](\d{1,3})[)][-.\s]?)?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9})')], max_length=15, null=True,
                                    blank=True, unique=True)
    regex = r'^\+?[0-9]'

    def __str__(self):
        return f'Profile of {self.user.username}'


class SocialMediaUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    twitter = models.URLField(max_length=200, blank=True)
    facebook = models.URLField(max_length=200, blank=True)
    google = models.URLField(max_length=200, blank=True)
    linkedIn = models.URLField(max_length=200, blank=True)
    instagram = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self', through=Contact, related_name='followers',
                                               symmetrical=False))
