# Generated by Django 4.2.3 on 2023-07-15 09:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trophies', '0002_alter_trophy_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trophy',
            name='rate',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
