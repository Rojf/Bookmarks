from django.utils.text import slugify

from core.repositories.base import BaseRepository
from images.models import ImagesModels


class ImagesRepository(BaseRepository):
    model = ImagesModels

    @classmethod
    def save(cls, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = slugify(instance.title)
        instance.save()
        return instance

