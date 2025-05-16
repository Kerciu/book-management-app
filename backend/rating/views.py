from rest_framework import viewsets
from .models import Rating
from .serializers import RatingSerializer

# Create your views here.
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer