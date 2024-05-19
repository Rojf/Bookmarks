from django.contrib.auth.models import User

from core.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User