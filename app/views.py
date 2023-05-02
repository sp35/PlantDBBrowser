import json

from rest_framework import generics, status
from rest_framework.views import APIView, Response
from django.urls.base import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile


from .models import Category, DataBase, Gene, Species, BlastSearchResult
from .serializers import GeneCreateSerializer, GeneSerializer
from .tasks import run_blast_analysis


class DatabaseListView(ListView):
    model = DataBase
    context_object_name = "databases"

    def get_queryset(self):
        category_name = self.request.GET.get("category", None)
        if category_name is not None:
            category = Category.objects.filter(name=category_name).first()
        else:
            category = Category.objects.first()
        return DataBase.objects.filter(approved=True, category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = list(Category.objects.values_list("name", flat=True))
        return context


class DatabaseSuggestView(CreateView):
    model = DataBase
    fields = ["name", "description", "url", "citation", "category", "sub_category"]

    def get_success_url(self) -> str:
        return reverse("home")


class GeneList(generics.ListAPIView):
    serializer_class = GeneSerializer

    def get_queryset(self):
        species = self.request.GET.get("species", None)
        bio_fxn = self.request.GET.get("function", None)
        exp_method = self.request.GET.get("experimental_method", None)
        blastn = self.request.GET.get("blastn", "")
        blastp = self.request.GET.get("blastp", "")

        filters = Q()
        if species is not None:

            filters = filters & Q(species__name=species)
        if bio_fxn is not None:
            filters = filters & Q(function=bio_fxn)
        if exp_method is not None:
            filters = filters & Q(experimental_method=exp_method)

        return Gene.objects.filter(filters, approved=True)


class GeneMetadata(APIView):
    def get(self, request):
        species = Species.objects.values_list("name", flat=True).distinct()
        biological_functions = Gene.objects.filter(approved=True).values_list("function", flat=True).distinct()
        experimental_methods = Gene.objects.filter(approved=True).values_list(
            "experimental_method", flat=True
        ).distinct()
        return Response(
            {
                "species": species,
                "biological_functions": biological_functions,
                "experimental_methods": experimental_methods,
            }
        )


class GeneSuggest(generics.CreateAPIView):
    serializer_class = GeneCreateSerializer

# GET gene/metadata
# GET gene/search?species=x&bio_fxn=y&exp_method=z&gene_family=a


class BlastSearch(APIView):

    def get(self, request, *args, **kwargs):
        result_obj = get_object_or_404(BlastSearchResult, id=kwargs.get("result_id"))
        blast_output = ""
        blast_results = {}
        with open(result_obj.result_file.path, 'rb') as f:
            blast_output = f.read()
        try:
            with open(result_obj.result_json_file.path, 'rb') as f:
                raw_blast_json_output = json.load(f)
                blast_results = raw_blast_json_output.get("BlastOutput2")[0].get("report").get("results").get("search")
        except:
            pass

        return Response({
            "result_id": result_obj.id,
            "status": result_obj.status,
            "blast_output": blast_output,
            "blast_results":  blast_results
        })

    def post(self, request):
        query_fasta = request.FILES.get('query_fasta')
        fasta_type = request.POST.get('fasta_type')
        result_file = ContentFile(b"")
        result_obj, _ = BlastSearchResult.objects.get_or_create(
            query_fasta=query_fasta, fasta_type=fasta_type, result_file=result_file, result_json_file=result_file)
        result_obj.result_file.save('result_file.txt', result_file)
        result_obj.result_json_file.save('result_file.json', result_file)
        run_blast_analysis(result_id=result_obj.id)
        return Response({
            "result_id": result_obj.id,
            "status": result_obj.status
        })
