from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    RefreshSerializer,
    LogoutSerializer,
    UserSerializer,
)
from .services.user import register_user
from .services.auth import login_user, refresh_tokens, logout_tokens

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = register_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
        )
        return Response(result)
            

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        creds = serializer.validated_data
        result = login_user(creds["username"], creds["password"])
        if not result:
            return Response({"detail": "Invalid credentials"}, status=401)

        return Response(result)
            

class RefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = refresh_tokens(serializer.validated_data["refresh"])
        return Response(result)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blocked = logout_tokens(
            refresh_token=serializer.validated_data.get("refresh"),
            access_token=serializer.validated_data.get("access"),
            current_auth=request.auth,
        )
        return Response({"detail": "Tokens revoked", "blocked": blocked})


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
