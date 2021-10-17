from django.shortcuts import render
from django.views.generic import ListView

from .models import DataBase


class DatabaseListView(ListView):
    model = DataBase
    context_object_name = "databases"
    queryset = DataBase.objects.filter(approved=True)

