# Generated by Django 3.2.8 on 2023-04-30 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_blastsearchresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='blastsearchresult',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('completed', 'completed')], default='pending', max_length=10),
        ),
    ]