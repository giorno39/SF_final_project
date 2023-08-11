from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from final_project.core.validators import file_size_validator

UserModel = get_user_model()


# Create your models here.
class Materials(models.Model):

    TITLE_MIN_LEN = 2
    TITLE_MAX_LEN = 50
    FIELD_MIN_LEN = 5
    FIELD_MAX_LEN = 50

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        validators=(validators.MinLengthValidator(TITLE_MIN_LEN),),
        null=False,
        blank=False,
    )

    field = models.CharField(
        max_length=FIELD_MAX_LEN,
        validators=(validators.MinLengthValidator(FIELD_MIN_LEN),),
        null=False,
        blank=False,
    )

    content = models.FileField(
        null=True,
        blank=True,
        upload_to='materials_files/',
        validators=(file_size_validator,)
    )

    references = models.URLField(
        null=True,
        blank=True,
    )

    uploaded_by = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

