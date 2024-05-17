from django.contrib.auth.models import User

from account.models import Profile, InfoUser, SocialMediaUser
from . import base


class UserRepository(base.BaseRepository):
    model = User


class ProfileRepository(base.BaseRepository):
    model = Profile


class InfoUserRepository(base.BaseRepository):
    model = InfoUser


class SocialMediaUserRepository(base.BaseRepository):
    model = SocialMediaUser
