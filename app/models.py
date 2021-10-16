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

    class Meta:
        verbose_name = "Database"
        verbose_name_plural = "Databases"
        unique_together = ("name", "category",)

    def __str__(self) -> str:
        return self.name
