from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import TeacherProfile, StudentProfile, TypesOfUsers


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_role_profile(sender, instance, created, **kwargs):
    """
    Auto-create the correct profile when a user is created.
    Works if user_type is set at creation time.
    """
    if not created:
        return

    if instance.user_type == TypesOfUsers.TEACHER:
        TeacherProfile.objects.get_or_create(user=instance)
    elif instance.user_type == TypesOfUsers.STUDENT:
        StudentProfile.objects.get_or_create(user=instance)
