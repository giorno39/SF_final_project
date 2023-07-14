from enum import Enum

from django.contrib.auth import models as auth_models
from django.contrib.auth.models import UserManager
from django.core import validators
from django.db import models


from final_project.core.model_mixins import ChoicesEnumMixin


# Create your models here.


class TypesOfUsers(ChoicesEnumMixin, Enum):
    student = 'student'
    teacher = 'teacher'


class AppUser(auth_models.AbstractUser):
    FIRST_NAME_MIN_LEN = 3
    FIRST_NAME_MAX_LEN = 30
    LAST_NAME_MIN_LEN = 3
    LAST_NAME_MAX_LEN = 30

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=(validators.MinLengthValidator(FIRST_NAME_MIN_LEN),)
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=(validators.MinLengthValidator(LAST_NAME_MIN_LEN),)
    )

    email = models.EmailField(
        unique=True,
    )

    user_type = models.CharField(
        choices=TypesOfUsers.choices(),
        max_length=TypesOfUsers.max_type_length(),
    )

    objects = UserManager()


