from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from final_project.accounts.models import Specialization
from final_project.core.validators import file_size_validator  # adjust import if needed

UserModel = get_user_model()


class TermPaper(models.Model):
    TERM_PAPER_MAX_LEN = 50
    TERM_PAPER_MIN_LEN = 2
    UNIVERSITY_MAX_LEN = 50

    title = models.CharField(
        max_length=TERM_PAPER_MAX_LEN,
        validators=(validators.MinLengthValidator(TERM_PAPER_MIN_LEN),),
        null=False,
        blank=False,
    )

    specializations = models.ManyToManyField(
        Specialization,
        blank=False,
        related_name="term_papers",
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

class TermPaperRequest(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        DECLINED = 'declined', 'Declined'
        CANCELED = 'canceled', 'Canceled'

    term_paper = models.ForeignKey(
        TermPaper,
        on_delete=models.CASCADE,
        related_name='requests',
    )

    student = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='sent_term_paper_requests',
    )

    teacher = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='received_term_paper_requests',
    )

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    message = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    responded_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['term_paper', 'teacher'],
                name='unique_teacher_request_per_term_paper',
            ),
        ]

    def __str__(self):
        return f'{self.term_paper} | {self.student} -> {self.teacher} | {self.status}'