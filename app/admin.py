from django.contrib import admin

from .models import Category, DataBase, SubCategory, Gene, Species


@admin.register(DataBase)
class DataBaseAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "category", "sub_category"]
    list_filter = ["approved", "category","sub_category"]
    search_fields = ["name"]


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Gene)
admin.site.register(Species)
