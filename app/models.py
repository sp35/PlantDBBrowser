import subprocess

from django.db import models
from django.conf import settings
from django.db import transaction


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

    def __str__(self) -> str:
        return self.name


class DataBase(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    url = models.URLField()
    citation = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Database"
        verbose_name_plural = "Databases"
        unique_together = ("name", "category",)

    def __str__(self) -> str:
        return self.name


class Species(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"
    
    def __str__(self) -> str:
        return self.name


class Gene(models.Model):
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True) # Plant Species
    name = models.CharField(max_length=256) # Gene Name
    host = models.CharField(max_length=256) # Host in which characterized
    # transcription_factor = models.CharField(max_length=256) # Transcription Factors
    symbol = models.CharField(max_length=256) # Gene Symbol
    description = models.TextField(blank=True) # Description
    # family = models.CharField(max_length=256) # Gene Family
    # accession_number = models.CharField(max_length=256) # Accession No.
    function = models.CharField(max_length=256) # Function
    pathway_category = models.CharField(max_length=256) # Pathway Category
    phenotype = models.CharField(max_length=256) # Phenotype
    experimental_method = models.CharField(max_length=256)# Experimental Method
    references = models.CharField(max_length=256, blank=True) # Reference
    publication_year = models.CharField(max_length=256, blank=True) # Year of Publication
    publication_link = models.URLField() # Link to Publication

    linked_suggestion = models.ForeignKey("GeneSuggestion", on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Gene"
        verbose_name_plural = "Genes"


    def __str__(self) -> str:
        return self.name


class GeneSuggestion(models.Model):
    contributor_name = models.CharField(max_length=256)
    contributor_email = models.EmailField(max_length=256)
    contributor_phone_number = models.CharField(max_length=16, blank=True)
    contributor_comments = models.TextField(blank=True)

    class Meta:
        verbose_name = "GeneSuggestion"
        verbose_name_plural = "GeneSuggestions"


    def __str__(self) -> str:
        return self.contributor_name


class Maintainer(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)

    def __str__(self) -> str:
        return self.name


class GeneBlastFastaType(models.TextChoices):
    NUCLEOTIDE = 'n', 'nucleotide'
    PROTEIN = 'p', 'protein'


"""
BlastDatabaseFile: Model to maintain fasta files for blast
"""
class BlastDatabaseFile(models.Model):
    fasta_type = models.CharField(max_length=1, choices=GeneBlastFastaType.choices, default=GeneBlastFastaType.NUCLEOTIDE, unique=True)
    fasta = models.FileField(upload_to='blast/')
    makeblastdb_output = models.TextField()

    class Meta:
        verbose_name = "BlastDatabaseFile"
        verbose_name_plural = "BlastDatabaseFiles"

    def __str__(self) -> str:
        return f"blast{self.fasta_type}"
    
    def _generate_db(self):
        dbtype = "nucl"
        out_path = settings.NUCL_BLASTDB_PATH
        if self.fasta_type == GeneBlastFastaType.PROTEIN:
            dbtype = "prot"
            out_path = settings.PROT_BLASTDB_PATH
        return subprocess.run([settings.NCBI_MAKEBLASTDB_PATH, "-title", f"DREAM_blast_{dbtype}_db", "-in", self.fasta.path, "-dbtype", dbtype, "-out", out_path], capture_output=True, check=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super(BlastDatabaseFile, self).save(*args, **kwargs)
            self.makeblastdb_output = self._generate_db()
            super(BlastDatabaseFile, self).save(*args, **kwargs)


class BlastSearchResultStatus(models.TextChoices):
    PENDING = 'pending', 'pending'
    COMPLETED = 'completed', 'completed'


class BlastSearchResult(models.Model):
    query_fasta = models.FileField(upload_to='blast_search/')
    fasta_type = models.CharField(max_length=1, choices=GeneBlastFastaType.choices, default=GeneBlastFastaType.NUCLEOTIDE)
    result_file = models.FileField(upload_to='blast_search/', blank=True, null=True)
    result_json_file = models.FileField(upload_to='blast_search/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=BlastSearchResultStatus.choices, default=BlastSearchResultStatus.PENDING)

    def __str__(self) -> str:
        return f"blast{self.fasta_type}-result-{self.id}"
