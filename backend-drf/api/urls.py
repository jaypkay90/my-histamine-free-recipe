from django.urls import path
from .views import food_histamine_info

urlpatterns = [
    path('foods/', food_histamine_info, name='food_histamine_info'),
]