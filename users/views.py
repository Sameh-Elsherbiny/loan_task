from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    LoanCustomerSerializer,
    LoanProviderSerializer,
    BankSerializer
)
from .utils import genetoken


# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if "user" in self.request.data:
            user_type = self.request.data.get("user").get("user_type")
            if user_type == "LP":
                return LoanProviderSerializer
            elif user_type == "LC":
                return LoanCustomerSerializer
            elif user_type == "BK":
                return BankSerializer

    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"user": serializer.data, "message": "User created successfully"}

        return Response(data, status=status.HTTP_201_CREATED)


class UserLogin(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            "token": genetoken(serializer.validated_data["user"]),
            "user": serializer.validated_data["user"],
            "message": "Login successful",
        }

        return Response(data, status=status.HTTP_200_OK)
