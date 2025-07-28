from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or password:
        return Response({'error':'username and password are required'},status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error':'username alredy exists'},status=status.HTTP_400_BAD_REQUEST)
    User=User.objects.create_user(username=username, email=email, password=password)
    return Response({'msg':'user generated succesfully'},status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    User = authenticate(username=username, password=password)
    if User is not None:
        refresh=RefreshToken.for_user(User)
        return Response({
            'refresh' : str(refresh),
            'access' : str(refresh.access_token),
            'msg' : 'Login successful'
        },status=status.HTTP_200_OK)
    else:
        return Response({'error' : 'Invalid username or password'},status=status.HTTP_401_UNAUTHORIZED)