# Generated by Django 4.2.3 on 2023-07-15 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('term_papers', '0006_remove_termpaper_is_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='termpaper',
            name='completed',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
