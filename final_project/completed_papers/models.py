from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from final_project.core.validators import file_size_validator

UserModel = get_user_model()


# Create your models here.
class CompletedPaper(models.Model):
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

    content = models.FileField(
        null=False,
        blank=False,
        upload_to='term_paper_files/',
        validators=(file_size_validator,)
    )

    completed_by = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )
