from django.urls import path

from .views import DatabaseListView, DatabaseSuggestView


urlpatterns = [
	path('', DatabaseListView.as_view(), name="home"),
	path('suggest/', DatabaseSuggestView.as_view()),
]
