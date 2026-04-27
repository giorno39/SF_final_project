from enum import Enum

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import UserManager
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from final_project.core.model_mixins import NumberChoicesEnumMixin


# Create your models here.


class TypesOfUsers(models.TextChoices):
    STUDENT = "student", _("Student")
    TEACHER = "teacher", _("Teacher")
    REVIEWER = "reviewer", _("Reviewer")


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
        choices=TypesOfUsers.choices,
        max_length=20,
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

    trust_score = models.PositiveIntegerField(
        default=50,
    )
    unassignments_count = models.PositiveIntegerField(
        default=0,
    )
    late_unassignments_count = models.PositiveIntegerField(
        default=0,
    )
    completed_on_time_count = models.PositiveIntegerField(
        default=0,
    )
    completed_early_count = models.PositiveIntegerField(
        default=0,
    )

    MIN_TRUST_SCORE = 0
    MAX_TRUST_SCORE = 100

    def decrease_trust(self, points):
        self.trust_score = max(self.MIN_TRUST_SCORE, self.trust_score - points)

    def increase_trust(self, points):
        self.trust_score = min(self.MAX_TRUST_SCORE, self.trust_score + points)

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


class SpecializationRequestStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    APPROVED = "approved", _("Approved")
    REJECTED = "rejected", _("Rejected")

class TeacherSpecializationRequest(models.Model):
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name="specialization_requests",
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        related_name="teacher_requests",
    )
    proof_file = models.FileField(
        upload_to="specialization_proofs/",
    )
    status = models.CharField(
        max_length=20,
        choices=SpecializationRequestStatus.choices,
        default=SpecializationRequestStatus.PENDING,
    )
    reviewer_note = models.TextField(
        blank=True,
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_specialization_requests",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "specialization"],
                name="unique_teacher_specialization_request",
            )
        ]

    def __str__(self):
        return f"{self.teacher.user.username} - {self.specialization.name} [{self.status}]"