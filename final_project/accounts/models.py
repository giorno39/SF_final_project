from enum import Enum

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import UserManager
from django.core import validators
from django.db import models

from final_project.core.model_mixins import NumberChoicesEnumMixin


# Create your models here.


class TypesOfUsers(NumberChoicesEnumMixin, Enum):
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

    def __str__(self):
        return f'{self.user_type};{self.username}'


class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )
    specializations = models.ManyToManyField(
        Specialization,
        blank=True,
        related_name="teachers",
    )

    def __str__(self):
        return f"TeacherProfile<{self.user.username}>"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    def __str__(self):
        return f"StudentProfile<{self.user.username}>"
