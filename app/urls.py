from django.urls import path

from .views import DatabaseListView


urlpatterns = [
	path('', DatabaseListView.as_view()),
]
