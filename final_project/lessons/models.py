from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from final_project.accounts.models import Specialization
from final_project.core.validators import file_size_validator

UserModel = get_user_model()


class Lesson(models.Model):
    TITLE_MIN_LEN = 2
    TITLE_MAX_LEN = 50
    SUBJECT_MIN_LEN = 2
    SUBJECT_MAX_LEN = 50

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        validators=(validators.MinLengthValidator(TITLE_MIN_LEN),),
        null=False,
        blank=False,
    )

    specializations = models.ManyToManyField(
        Specialization,
        blank=False,
        related_name='lessons',
    )

    price = models.PositiveIntegerField(
        null=False,
        blank=False
    )

    cover_image = models.ImageField(
        upload_to='lesson_covers/',
        null=True,
        blank=True,
        validators=(file_size_validator,),
        help_text='Optional cover image (max 2 MB).',
    )

    teacher = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )