from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Shelf
from .serializers import ShelfSerializer


class ShelfViewSet(viewsets.ModelViewSet):
    serializer_class = ShelfSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Shelf.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except ValidationError as e:
            raise ValidationError(e.detail)

    def perform_destroy(self, instance):
        if instance.is_default:
            raise ValidationError("Cannot delete default shelves")
        instance.delete()
