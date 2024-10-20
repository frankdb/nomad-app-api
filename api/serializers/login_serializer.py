from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import CustomUser

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid email or password')

        refresh = RefreshToken.for_user(user)

        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)

        return data