# Generated by Django 3.2.8 on 2023-04-29 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_blastdatabasefile_fasta'),
    ]

    operations = [
        migrations.AddField(
            model_name='blastdatabasefile',
            name='makeblastdb_output',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
