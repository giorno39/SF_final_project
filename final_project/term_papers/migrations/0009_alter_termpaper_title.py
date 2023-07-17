# Generated by Django 4.2.3 on 2023-07-16 12:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('term_papers', '0008_termpaper_rated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termpaper',
            name='title',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]
