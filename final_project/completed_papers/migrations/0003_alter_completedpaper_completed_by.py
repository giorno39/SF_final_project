# Generated by Django 4.2.3 on 2023-07-16 12:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('completed_papers', '0002_remove_completedpaper_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedpaper',
            name='completed_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]