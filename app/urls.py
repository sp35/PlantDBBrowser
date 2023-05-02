from django.urls import path

from .views import DatabaseListView, DatabaseSuggestView, GeneList, GeneMetadata, GeneSuggest, BlastSearch


urlpatterns = [
    # path("", DatabaseListView.as_view(), name="home"),
    # path("suggest", DatabaseSuggestView.as_view()),
    path("genes", GeneList.as_view()),
	path("genes/metadata", GeneMetadata.as_view()),
	path("genes/suggest", GeneSuggest.as_view()),
	path("blast-search", BlastSearch.as_view()),
	path("blast-search/results/<int:result_id>", BlastSearch.as_view()),
]
