from .models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import json

User = get_user_model()

@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    try:
        payload = json.loads(request.body)
        username = payload.get('username')
        email = payload.get('email')
        password = payload.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'msg': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'message': "Internal server error", 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    login_input = request.data.get("username") or request.data.get("email")
    password = request.data.get("password")

    if not login_input or not password:
        return Response({"error": "Username/Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_obj = User.objects.get(email=login_input)
        username = user_obj.username
    except User.DoesNotExist:
        username = login_input

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'msg': 'Login successful',
            'user': user.username
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username/email or password'}, status=status.HTTP_401_UNAUTHORIZED)
