from django.db import migrations


DEFAULT_SPECIALIZATIONS = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "Programming",
    "Engineering",
    "Statistics",
    "Economics",
    "Business & Management",
    "Accounting",
    "Law",
    "Political Science",
    "Psychology",
    "Sociology",
    "Philosophy",
    "History",
    "Geography",
    "Literature",
    "Linguistics",
    "English Language",
    "Japanese Language",
    "Spanish Language",
    "French Language",
    "Art & Design",
    "Drawing & Illustration",
    "Music",
    "Education & Pedagogy",
]


def seed_specializations(apps, schema_editor):
    Specialization = apps.get_model("accounts", "Specialization")
    for name in DEFAULT_SPECIALIZATIONS:
        Specialization.objects.get_or_create(name=name)


def unseed_specializations(apps, schema_editor):
    Specialization = apps.get_model("accounts", "Specialization")
    Specialization.objects.filter(name__in=DEFAULT_SPECIALIZATIONS).delete()


class Migration(migrations.Migration):
    dependencies = [
        # IMPORTANT: update this to the migration that created Specialization/Profiles
        ("accounts", "0002_specialization_teacherprofile_studentprofile"),
    ]

    operations = [
        migrations.RunPython(seed_specializations, unseed_specializations),
    ]
