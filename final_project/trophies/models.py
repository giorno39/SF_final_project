from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

UserModel = get_user_model()


class Trophy(models.Model):
    class Meta:
        verbose_name_plural = 'Trophies'
    PROJECT_MAX_LEN = 50
    PROJECT_MIN_LEN = 2

    rate = models.FloatField(
        null=False,
        blank=True,
        default=0,
        validators=(validators.MinValueValidator(0), validators.MaxValueValidator(5))

    )

    project = models.CharField(
        max_length=PROJECT_MAX_LEN,
        validators=(validators.MinLengthValidator(PROJECT_MIN_LEN),),
        null=True,
        blank=True,
    )

    completed_by = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    obtained_at = models.DateField(
        auto_now=True,
        null=False,
        blank=False,
    )
