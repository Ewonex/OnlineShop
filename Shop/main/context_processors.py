from .models import Review
from django.db import models

def footer_data(request):
    reviews_count = Review.objects.count()
    average_rating = Review.objects.aggregate(avg_rating=models.Avg('mark'))

    return {
        'reviews_count': reviews_count,
        'average_rating': average_rating['avg_rating'],
    }
