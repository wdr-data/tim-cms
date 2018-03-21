from django.contrib import admin

from ..models.genre import Genre
from ..references.dialogflow import get_entity_uuid, add_entry, delete_entry, Entity


class GenreAdmin(admin.ModelAdmin):
    actions = ['delete_model']

    class Meta:
        model = Genre
        fields = "__all__"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        genre_uuid = get_entity_uuid(Entity.GENRES)
        add_entry(obj.name, genre_uuid)

    def delete_model(self, request, obj):
        try:
            for o in obj:
                super().delete_model(request, o)

                genre_uuid = get_entity_uuid(Entity.GENRES)
                delete_entry(o.name, genre_uuid)
        except TypeError:
                super().delete_model(request, obj)

                genre_uuid = get_entity_uuid(Entity.GENRES)
                delete_entry(obj.name, genre_uuid)

    delete_model.short_description = "Ausgewählte Gernes löschen"

# Register your model here
admin.site.register(Genre, GenreAdmin)
