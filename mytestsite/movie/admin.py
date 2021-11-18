from django.contrib import admin
from .models import *

# Register your models here.

# rejestracja modeli
#admin.site.register(Movie)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "imdb")
    list_filter = ("year",)
    search_fields = ("title",)

    def save_model(self, request, obj, form, change):
        if obj.author is None:
            obj.author = request.user
        obj.save()