from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes(['AllowAny'])
def register_user(request):
    username=request.data.get('username')
    email=request.data.get('email')
    password=request.data.get('password')

    if not username or password:
        return Response({'error':'username and password are required'},status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error':'username alredy exists'},status=status.HTTP_400_BAD_REQUEST)
    User=User.objects.create_user(username=username, email=email, password=password)
    return Response({'msg':'user generated succesfully'},status=status.HTTP_201_CREATED)