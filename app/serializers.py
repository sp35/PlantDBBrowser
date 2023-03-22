from rest_framework import serializers as rfs
from django.db import transaction

from .models import Gene, Species, GeneSuggestion


class SpeciesSerializer(rfs.ModelSerializer):
    class Meta:
        model = Species
        exclude = ('id', )


class GeneSuggestSerializer(rfs.ModelSerializer):
    class Meta:
        model = GeneSuggestion
        exclude = ('id', )


class GeneSerializer(rfs.ModelSerializer):
    species = SpeciesSerializer()
    linked_suggestion = GeneSuggestSerializer()

    class Meta:
        model = Gene
        exclude = ('id', )
    
    def to_representation(self, instance: Gene):
        ret = super().to_representation(instance)
        ret['species_name'] = instance.species.name if instance.species else None
        return ret

    def create(self, validated_data):
        with transaction.atomic():
            linked_suggestion_data = validated_data.pop("linked_suggestion")
            species_data = validated_data.pop("species")
            linked_suggestion = GeneSuggestion(**linked_suggestion_data)
            linked_suggestion.save()
            species = Species.objects.get_or_create(name=species_data["name"])[0]
            gene = Gene(**validated_data, linked_suggestion=linked_suggestion, species=species)
            gene.save()
            return gene
