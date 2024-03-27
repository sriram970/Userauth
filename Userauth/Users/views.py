from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import (
    RegistrationSerializer,
    VerificationSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

# Implement OTP generation and verification logic here (using email or other methods)

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate OTP and send verification email/SMS (if needed)
            return Response({'message': 'User created successfully. Please verify your email.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            # Implement verification logic here (using email or OTP)
            # If verified, return success message
            # ...
            return Response({'message': 'Email verified successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():

            user = User.objects
