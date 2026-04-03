from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from final_project.accounts.models import Specialization
from final_project.core.validators import file_size_validator, pdf_only_validator

UserModel = get_user_model()


class Materials(models.Model):
    TITLE_MIN_LEN = 2
    TITLE_MAX_LEN = 50

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        validators=(validators.MinLengthValidator(TITLE_MIN_LEN),),
        null=False,
        blank=False,
    )

    specializations = models.ManyToManyField(
        Specialization,
        blank=False,
        related_name='materials',
    )

    content = models.FileField(
        null=True,
        blank=True,
        upload_to='materials_files/',
        validators=(file_size_validator, pdf_only_validator),
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

    reference_is_valid = models.BooleanField(default=False)
    reference_validation_reason = models.TextField(blank=True, null=True)
    reference_last_checked_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class MaterialComment(models.Model):
    MAX_CONTENT_LEN = 300

    material = models.ForeignKey(
        Materials,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='material_comments',
    )

    content = models.TextField(
        max_length=MAX_CONTENT_LEN,
        null=False,
        blank=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.material}'