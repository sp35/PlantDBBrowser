# Generated by Django 3.2.8 on 2021-10-16 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20211016_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterUniqueTogether(
            name='database',
            unique_together={('name', 'category')},
        ),
    ]
