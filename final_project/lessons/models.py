from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

# Create your models here.

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

    subject = models.CharField(
        max_length=SUBJECT_MAX_LEN,
        validators=(validators.MinLengthValidator(SUBJECT_MIN_LEN),),
        null=False,
        blank=False,
    )

    price = models.PositiveIntegerField(
        null=False,
        blank=False
    )

    teacher = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
