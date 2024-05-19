from django.contrib import admin

from images.repositories.Repository import ImagesRepository


@admin.register(ImagesRepository.model)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created']
    list_filter = ['created']
