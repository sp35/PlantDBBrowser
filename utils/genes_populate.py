import sys

sys.path.append("../")

import os
import xlrd
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PlantDBBrowser.settings")
django.setup()
PATH = os.path.dirname(os.path.realpath(__file__))

from app.models import Gene, Species


def gene_excel_parser():
    loc = os.path.join(PATH, "genes.xlsx")
    book = xlrd.open_workbook(loc)

    ordered_columns = [
        "species",
        "name",
        "host",
        "transcription_factor",
        "symbol",
        "description",
        "family",
        "accession_number",
        "function",
        "pathway_category",
        "phenotype",
        "experimental_method",
        "references",
        "year",
        "publication_link",
    ]

    for index, sheet in enumerate(book.sheets()):

        nrows = sheet.nrows
        ncols = sheet.ncols

        gene_dict = {}
        for row in range(1, nrows):
            species, _ = Species.objects.get_or_create(name=str(sheet.cell(row, 1).value).strip())

            for col in range (2, ncols):
                gene_dict[ordered_columns[col-1]] = str(sheet.cell(row, col).value).strip()
            gene, _ = Gene.objects.get_or_create(**gene_dict, species=species, approved=True)


if __name__ == "__main__":
    gene_excel_parser()
