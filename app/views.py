from django.urls.base import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import Category, DataBase


class DatabaseListView(ListView):
    model = DataBase
    context_object_name = "databases"

    def get_queryset(self):
        category_name = self.request.GET.get("category", None)
        if category_name is not None:
            category = Category.objects.filter(name=category_name).first()
        else:
            category = Category.objects.first()
        return DataBase.objects.filter(
            approved=True,
            category=category
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = list(Category.objects.values_list("name", flat=True))
        return context


class DatabaseSuggestView(CreateView):
    model = DataBase
    fields = ["name", "description", "url", "citation", "category", "sub_category"]

    def get_success_url(self) -> str:
        return reverse("home")
