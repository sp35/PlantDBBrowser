from django.db import models


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


class GeneBlast(models.Model):
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE, related_name="blasts")
    fasta_type = models.CharField(max_length=1, choices=GeneBlastFastaType.choices, default=GeneBlastFastaType.NUCLEOTIDE)
    fasta = models.TextField()

    def __str__(self) -> str:
        return f"{self.gene} - blast{self.fasta_type}"

    def save(self, *args, **kwargs):
        self.fasta = "".join(self.fasta.split())
        super(GeneBlast, self).save(*args, **kwargs)
