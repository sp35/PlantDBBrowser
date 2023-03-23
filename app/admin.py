from django.contrib import admin

from .models import Category, DataBase, SubCategory, Gene, Species, GeneSuggestion


@admin.register(Gene)
class GeneAdmin(admin.ModelAdmin):
    list_display = ["name", "species", "approved"]
    list_filter = ["approved", "species","function", "experimental_method"]
    search_fields = ["name"]


# admin.site.register(Category)
# admin.site.register(SubCategory)
# admin.site.register(Gene)
# admin.site.register(Species)
admin.site.register(GeneSuggestion)
