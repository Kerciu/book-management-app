from django.shortcuts import render

# Create your views here.
class BookRatingViewSet(viewsets.ModelViewSet):
    queryset = BookRatings.objects.all()
    serializer_class = BookRatingSerializer