from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, DataBase, SubCategory, Gene, Species, GeneSuggestion, Maintainer, BlastDatabaseFile, BlastSearchResult


@admin.register(Gene)
class GeneAdmin(admin.ModelAdmin):
    list_display = ["name", "species", "symbol", "approved"]
    list_filter = ["approved", "species","function", "experimental_method"]
    search_fields = ["name"]

@admin.register(BlastDatabaseFile)
class BlastDatabaseFileAdmin(admin.ModelAdmin):
    fields = ["fasta_type", "fasta", "formatted_makeblastdb_output"]
    readonly_fields = ["formatted_makeblastdb_output"]

    def formatted_makeblastdb_output(self, obj):
        return mark_safe(obj.makeblastdb_output.replace('\\n', '<br/>'))


# admin.site.register(Category)
# admin.site.register(SubCategory)
# admin.site.register(Gene)
# admin.site.register(Species)
admin.site.register(GeneSuggestion)
admin.site.register(Maintainer)
admin.site.register(BlastSearchResult)
