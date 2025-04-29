import os
import open3d as o3d

from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.files.storage import FileSystemStorage

from decouple import AutoConfig
from ..models import ModelFile, DefectAnalysis
from ..serializers import ModelFileSerializer
from ..tasks import analyze_model_file

config = AutoConfig(search_path=".env")


class ModelFileViewSet(viewsets.ModelViewSet):
    serializer_class = ModelFileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def is_admin(self, user):
        return user.groups.filter(name='admin').exists()
    
    def retrieve(self, request, pk=None):
        user = request.user
        try:
            if self.is_admin(user):
                model = ModelFile.objects.get(pk=pk)
            else:
                model = ModelFile.objects.get(pk=pk, user=user)
        except ModelFile.DoesNotExist:
            return Response({"detail": "Model not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(model)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        return ModelFile.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        model_file = self.request.FILES.get("model_file")

        if not user.is_authenticated:
            raise serializers.ValidationError({"detail": "User authentication required."})

        if not model_file:
            raise serializers.ValidationError({"detail": "No file uploaded."})

        file_directory = os.path.join(config("NGINX_PATH"), user.username)
        fs = FileSystemStorage(location=file_directory)
        file_name = fs.save(model_file.name, model_file)
        file_path = os.path.join(file_directory, file_name).replace("\\", "/")

        try:
            mesh = o3d.io.read_triangle_mesh(file_path)
            vertices_count, faces_count = len(mesh.vertices), len(mesh.triangles)
        except Exception:
            raise serializers.ValidationError({"detail": "Invalid 3D model file."})

        serializer.save(
            user=user,
            file_name=file_name,
            file_path=file_path,
            vertices_count=vertices_count,
            faces_count=faces_count,
        )

    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        try:
            model_file = self.get_object()

            existing_analysis = DefectAnalysis.objects.filter(
                model_file=model_file,
                status__in=["pending", "processing"]
            ).first()

            if existing_analysis:
                return Response(
                    {"message": f"Analysis already in progress (ID: {existing_analysis.id})"},
                    status=status.HTTP_409_CONFLICT
                )

            analysis = DefectAnalysis.objects.create(
                model_file=model_file,
                status="pending"
            )

            task = analyze_model_file.apply_async(args=[model_file.id])
            analysis.task_id = task.id
            analysis.save()

            return Response(
                {
                    "message": "Analysis started, status will update soon",
                    "analysis_id": analysis.id,
                    "task_id": task.id
                },
                status=status.HTTP_202_ACCEPTED
            )
        except ModelFile.DoesNotExist:
            return Response({"error": "Model file not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def all_models(self, request):
        user = request.user
        if not user.groups.filter(name='admin').exists():
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        all_models = ModelFile.objects.all()
        serializer = self.serializer_class(all_models, many=True)
        return Response(serializer.data)
