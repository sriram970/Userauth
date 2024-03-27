import random
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User
from django.core.mail import send_mail


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        # Generate random OTP (replace with your preferred method)
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        # Send OTP to user's email
        send_mail(
            subject='User Registration OTP',
            message=f'Your OTP for UserAuth registration is {otp}',
            from_email='youremail@example.com',
            recipient_list=[validated_data['email']],
        )
        return {'token': otp}  # Return OTP for verification


class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        # Implement verification logic here
        # Check if user exists with the given email
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError('User with this email does not exist.')
        # Validate OTP (replace with your preferred method)
        if otp != 'your_actual_otp':
            raise serializers.ValidationError('Invalid OTP provided.')
        user.is_verified = True
        user.save()
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        user = authenticate(email=email, password=otp)  # Assuming OTP as password
        if not user:
            raise serializers.ValidationError('Invalid email or OTP.')
        if not user.is_verified:
            raise serializers.ValidationError('Please verify your email first.')
        # Generate access and refresh tokens
        token, _ = Token.objects.get_or_create(user=user)
        return {'refresh': token.key, 'access': token.key}


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        # Implement logic to send password reset link/OTP to user's email
        # ...
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        new_password = attrs.get('new_password')
        return attrs
