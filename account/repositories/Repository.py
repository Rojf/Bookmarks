from django.contrib.auth.models import User

from core.repositories.base import BaseRepository
from account.models import Profile, InfoUser, SocialMediaUser


class ProfileRepository(BaseRepository):
    model = Profile


class InfoUserRepository(BaseRepository):
    model = InfoUser


class SocialMediaUserRepository(BaseRepository):
    model = SocialMediaUser
