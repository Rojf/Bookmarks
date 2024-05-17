from django.contrib import admin
from .models import Profile, InfoUser, SocialMediaUser


@admin.register(Profile, site=None)
class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']


@admin.register(InfoUser, site=None)
class InfoUserAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']


@admin.register(SocialMediaUser, site=None)
class SocialMediaUserAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
