from rest_framework.views import APIView
from rest_framework import status
from api.models import Itinerary
from rest_framework.response import Response
from api.serializers import ItinerarySerializer

class ItineraryListCreateView(APIView):

    def get(self, request):
        itineraries = Itinerary.objects.filter(user=request.user)
        serializer = ItinerarySerializer(itineraries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItinerarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        