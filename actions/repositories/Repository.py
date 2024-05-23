from core.repositories.base import BaseRepository
from actions.models import Action


class ActionRepository(BaseRepository):
    model = Action

