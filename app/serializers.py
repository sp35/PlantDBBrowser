from rest_framework import serializers as rfs

from .models import Gene, Species, GeneSuggestion


class SpeciesSerializer(rfs.ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"


class GeneSerializer(rfs.ModelSerializer):
    species = SpeciesSerializer()

    class Meta:
        model = Gene
        fields = "__all__"


class GeneSuggestSerializer(rfs.ModelSerializer):
    class Meta:
        model = GeneSuggestion
        fields = "__all__"
