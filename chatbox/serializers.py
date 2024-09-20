# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User  # Replace with your User model if different

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'status']  # Exclude 'avatar'
