from django.shortcuts import render

# Create your views here.
class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReviews.objects.all()
    serializer_class = BookReviewSerializer
