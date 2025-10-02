from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from foods.models import Food, FoodName, HistamineInfo
from api.serializers import FoodSerializer
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView

'''@api_view(['GET'])
def food_histamine_info(request):
    query = request.GET.get('query', '').strip()
    if not query:
        return Response({'error': 'query parameter is required'}, status=400)

    # Suche nach FoodName (case-insensitive, first match)
    try:
        food_name = FoodName.objects.select_related('food__histamineinfo').get(name__iexact=query)
    except FoodName.DoesNotExist:
        return Response({'error': 'Food not found'}, status=404)

    histamine = getattr(food_name.food, 'histamineinfo', None)
    if not histamine:
        return Response({'error': 'No histamine info available'}, status=404)

    return Response({
        'food': food_name.name,
        'language': food_name.language,
        'compatibility_score': histamine.compatibility_score,
        'rapid_histamine_formation': histamine.rapid_histamine_formation,
        'other_amines': histamine.other_amines,
        'liberator': histamine.liberator,
        'blocker': histamine.blocker,
        'notes': histamine.notes,
        'information_source': histamine.information_source.name if histamine.information_source else None
    })
'''
class FoodListView(ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class FoodDetailView(generics.RetrieveAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'pk'

