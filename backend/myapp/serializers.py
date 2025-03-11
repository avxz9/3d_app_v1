from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ModelFile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ModelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelFile
        fields = ['id', 'file_name', 'file_path', 'user', 'vertices_count', 'faces_count']
        read_only_fields = ['id', 'file_name', 'file_path', 'user', 'vertices_count', 'faces_count']  
        
        



