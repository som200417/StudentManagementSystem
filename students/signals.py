from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Student, StudentAuditLog
from .middleware import get_current_user


@receiver(post_save, sender=Student)
def student_create_update_log(sender, instance, created, **kwargs):
    user = get_current_user()

    StudentAuditLog.objects.create(
        student=instance,
        student_name=instance.name,
        action='CREATE' if created else 'UPDATE',
        performed_by=user
    )


@receiver(post_delete, sender=Student)
def student_delete_log(sender, instance, **kwargs):
    user = get_current_user()

    StudentAuditLog.objects.create(
        student_name=instance.name,
        action='DELETE',
        performed_by=user
    )
