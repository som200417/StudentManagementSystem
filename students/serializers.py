from rest_framework import serializers
from .models import Activelog

class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Activelog
        fields = '__all__'
