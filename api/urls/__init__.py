from django.urls import path, include

urlpatterns = [
    path('', include('api.urls.auth_urls')),
    path('', include('api.urls.itinerary_urls')),
]