# Generated by Django 4.2.3 on 2023-07-14 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('term_papers', '0002_termpaper_is_taken_termpaper_user_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='termpaper',
            old_name='user_id',
            new_name='user',
        ),
    ]
