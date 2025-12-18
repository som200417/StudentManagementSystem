from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect
import logging
from .models import Activelog
logger = logging.getLogger(__name__)

from .models import Activelog

class ActivityLogMixin:
    action = None

    def log_activity(self, request, obj=None, message=""):
        Activelog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=self.action or self.__class__.__name__,
            model_name=obj.__class__.__name__ if obj else '',
            object_id=obj.pk if obj else None,
            message=message,
            ip_address=self.get_client_ip(request)
        )

        # Console output
        print(
            f"[ACTIVITY] {request.user} | "
            f"{self.action} | "
            f"{obj.__class__.__name__ if obj else ''} | "
            f"{message}"
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class StaffRequiredMixin(AccessMixin):
    """Allow only staff users to access view."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, "403 Forbidden: Staff access only.")
            return redirect("student_list")
        return super().dispatch(request, *args, **kwargs)


class AdminOnlyMixin(AccessMixin):
    """Allow only superusers to access view."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "403 Forbidden: Admin access only.")
            return redirect("student_list")
        return super().dispatch(request, *args, **kwargs)


class ReadOnlyMixin(AccessMixin):
    """Allow only safe HTTP methods (GET, HEAD, OPTIONS)."""
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')

    def dispatch(self, request, *args, **kwargs):
        if request.method not in self.allowed_methods:
            messages.error(request, "403 Forbidden: Read access only.")
            return redirect("student_list")
        return super().dispatch(request, *args, **kwargs)
