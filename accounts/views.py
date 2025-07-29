from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import json

@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):

    try:
        payload = json.loads(request.body)
        username = payload.get('username')
        email = payload.get('email')
        password = payload.get('password')

        if not username or not password:
            return Response({'error':'username and password are required'},status=status.HTTP_400_BAD_REQUEST)
        
        existingUser = CustomUser.objects.filter(username=username).exists()
        print(existingUser, 'user')
        
        if existingUser:
            return Response({'error':'username alredy exists'},status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.create_user(username=username , email=email , password=password)
        print('User created')
        
        return Response({'msg':'user generated succesfully'},status=status.HTTP_201_CREATED)
    
    except:

        return Response({ 'message': "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )


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