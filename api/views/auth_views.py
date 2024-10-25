import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import LoginSerializer, RegisterSerializer, UserSerializer

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "message": "User created successfully",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"Logout attempt for user: {request.user.email}")
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                logger.warning(
                    f"Logout failed for user {request.user.email}: Refresh token not provided"
                )
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            logger.info(f"User {request.user.email} logged out successfully")
            return Response(
                {"success": "User logged out successfully"}, status=status.HTTP_200_OK
            )

        except TokenError as e:
            logger.error(
                f"Logout failed for user {request.user.email}: Invalid token - {str(e)}"
            )
            return Response(
                {"error": f"Invalid token: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.exception(
                f"Unexpected error during logout for user {request.user.email}: {str(e)}"
            )
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
