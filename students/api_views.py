from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from .models import Activelog
from .serializers import ActivityLogSerializer
from rest_framework.renderers import JSONRenderer

class ActivityLogViewSet(ModelViewSet):
    queryset = Activelog.objects.all().order_by('-created_at')
    serializer_class = ActivityLogSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAdminUser]
