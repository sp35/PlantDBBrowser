import sys
sys.path.append('../')

import os
import xlrd
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PlantDBBrowser.settings')
django.setup()
PATH = os.path.dirname(os.path.realpath(__file__))

from app.models import DataBase, Category


def db_excel_parser():
    loc = (os.path.join(PATH ,"databases.xlsx"))
    book = xlrd.open_workbook(loc)



    for index, sheet in enumerate(book.sheets()):
        if index == 0:
            continue
        nrows = sheet.nrows
        category, _ = Category.objects.get_or_create(
            name=sheet.name.strip()
        )

        for row in range(1, nrows):
            name = sheet.cell(row, 0).value.strip()
            url = sheet.cell(row, 1).value.strip()
            desc = sheet.cell(row, 2).value.strip()
            cit = sheet.cell(row, 3).value.strip()

            db, _ = DataBase.objects.get_or_create(
                name=name,
                category=category,
            )
            db.url = url
            db.description = desc
            db.citation = cit
            db.approved = True
            db.save()


if __name__ == '__main__':
    db_excel_parser()
