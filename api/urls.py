from django.urls import path
from .views import get_artists_name_with_similar_work


urlpatterns = [
    path('get-artists/', get_artists_name_with_similar_work),
]
