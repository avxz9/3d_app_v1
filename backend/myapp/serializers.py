from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ModelFile, DefectAnalysis

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.SerializerMethodField()
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_role(self, obj):
        groups = obj.groups.values_list('name', flat=True)
        return groups[0] if groups else None

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ModelFileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = ModelFile
        fields = ['id', 'file_name', 'file_path', 'user', 'vertices_count', 'faces_count', 'uploaded_at']
        read_only_fields = ['id', 'file_name', 'file_path', 'user', 'vertices_count', 'faces_count', 'uploaded_at']  

    def get_user(self, obj):
        return obj.user.username if obj.user else None       
        
class DefectAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = DefectAnalysis
        fields = ['id', 'model_file', 'status', 'defect_count', 'is_watertight', 'details', 'defect_data', 'created_at']
        read_only_fields = ['created_at', 'status', 'defect_count', 'details', 'report_path']


