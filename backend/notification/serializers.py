from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.Serializer):
    class Meta:
        model = Notification
        fields = "__all__"
