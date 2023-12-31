# Generated by Django 4.2.3 on 2023-07-16 14:53

from django.db import migrations, models
import final_project.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('completed_papers', '0005_alter_completedpaper_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedpaper',
            name='content',
            field=models.FileField(upload_to='term_paper_files/', validators=[final_project.core.validators.file_size_validator]),
        ),
    ]
