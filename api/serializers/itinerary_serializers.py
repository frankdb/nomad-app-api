from rest_framework import serializers
from api.models import Itinerary

class ItinerarySerializer(serializers.ModelSerializer):
    ai_generated_itinerary = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Itinerary
        fields = ['id', 'title', 'start_date', 'end_date', 'description', 'ai_generated_itinerary']
        read_only_fields = ['id']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data
