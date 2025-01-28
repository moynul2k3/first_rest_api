from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.conf import settings
from .validators import CustomPasswordValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import random
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User

@api_view(['GET'])
@permission_classes([AllowAny])
def check_user_exists(request):
    email = request.query_params.get('email')
    if User.objects.filter(email=email).exists():
        return Response({'exists': True})
    return Response({'exists': False})


@api_view(['POST'])
def signin_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            "status": "success", 
            "message": "Login successful"
        }, status=200)
    return Response({"status": "failed", "message": "Invalid Password. Please try again."}, status=400)


@api_view(['POST'])
def signup_view(request):
    custom_validator = CustomPasswordValidator()
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    if User.objects.filter(email=email).exists():
        return Response({'error': 'User already exists'}, status=400)
    try:
        custom_validator.validate(password)
        if password != confirm_password:
            return Response({'message': "Confirm Password doesn't matched."})
        else:
            user = User.objects.create_user(
                email=email, password=confirm_password)
    except ValidationError as e:
        return JsonResponse({'status': 'failed', 'message': str(e)})
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            "status": "success",
            "message": "Welcome!!!"
        }, status=200)
    return Response({"error": "Invalid credentials"}, status=400)


@api_view(['POST'])
def send_otp(request):
    email = request.data.get('email')
    otp = random.randint(100000, 999999)
    if User.objects.filter(email=email).exists():
        TemporaryOTP.objects.get_or_create(
            user=User.objects.get(email=email),
            otp = otp
        )

        # send the otp in email code will be here
        return Response({"status": "success", "message": f"OTP sent to {email}. It will expire in 1 minutes."})
    else:
        return Response({'error': 'User not found. Please try again'}, status=400)



@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otpValue')
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        temporaryOTP = TemporaryOTP.objects.filter(user=user).last()
        if not temporaryOTP.otp:
            return JsonResponse({"status": "failed", "message": "OTP expired or not found"})
        if temporaryOTP.otp == otp:
            return Response({"status": "success", "message": f"Verified. Congratulations, enter your new password."})
    else:
        return Response({'error': 'User not found. Please try again'}, status=400)

    return Response({"error": "Invalid OTP"}, status=400)


@api_view(['POST'])
def forgot_password(request):
    custom_validator = CustomPasswordValidator()
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    # Check if the email exists in the database
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"status": "failed", 'message': 'User not found. Please try again.'})

    # Validate the password with the custom validator
    try:
        custom_validator.validate(password)
        if password != confirm_password:
            return Response({"status": "failed", 'message': "Confirm Password doesn't match."})

        # Update password
        user.password = make_password(password)  # Hash the new password
        user.save()

        # Log the user in automatically after resetting the password
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            "status": "success",
            "message": "Password reset successful. You are now logged in."
        }, status=200)
    except ValidationError as e:
        return JsonResponse({'status': 'failed', 'message': str(e)})

