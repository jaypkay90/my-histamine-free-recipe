from django.urls import path
# from .views import food_histamine_info
from . import views

urlpatterns = [
    # Foods - ListView
    #path('foods/', food_histamine_info, name='food_histamine_info'),
    path('foods/', views.FoodListView.as_view(), name='food_list_view'),

    # Foods - DetailView
    path('foods/<int:pk>/', views.FoodDetailView.as_view(), name='food_detail_view'),
]