from django.urls import path
from api.views.itinerary_views import ItineraryListCreateView

urlpatterns = [
    path('itineraries/', ItineraryListCreateView.as_view(), name='itinerary-list-create')
]