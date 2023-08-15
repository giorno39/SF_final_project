from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from final_project.core.validators import file_size_validator

# Create your models here.

UserModel = get_user_model()


class TermPaper(models.Model):
    TERM_PAPER_MAX_LEN = 50
    TERM_PAPER_MIN_LEN = 2
    SUBJECT_MAX_LEN = 50
    UNIVERSITY_MAX_LEN = 50

    title = models.CharField(
        max_length=TERM_PAPER_MAX_LEN,
        validators=(validators.MinLengthValidator(TERM_PAPER_MIN_LEN),),
        null=False,
        blank=False,
    )

    subject = models.CharField(
        max_length=SUBJECT_MAX_LEN,
        null=False,
        blank=False,
    )

    university = models.CharField(
        max_length=UNIVERSITY_MAX_LEN,
        null=False,
        blank=False,
    )

    death_line = models.DateField(
        null=False,
        blank=False,
    )

    price_cap = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    content = models.FileField(
        null=False,
        blank=False,
        upload_to='term_paper_files/',
        validators=(file_size_validator,)
    )

    completed = models.BooleanField(
        null=False,
        blank=True,
        default=False,
    )

    rated = models.BooleanField(
        null=False,
        blank=True,
        default=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    taken_by = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        related_name='taken_by_teacher',
        null=True,
        blank=True,
        default=None,
    )






