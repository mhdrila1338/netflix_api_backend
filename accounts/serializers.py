from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'is_premium']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # 🔐 hash password
        return super().create(validated_data)
