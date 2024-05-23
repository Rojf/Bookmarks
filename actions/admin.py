from django.contrib import admin

from actions.repositories.Repository import ActionRepository


@admin.register(ActionRepository.model)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'verb', 'target', 'created']
    list_filter = ['created']
    search_fields = ['verb']
