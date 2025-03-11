import os
import io 
import open3d as o3d

from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from decouple import AutoConfig
from .models import ModelFile
from .serializers import UserSerializer, ModelFileSerializer

import xlsxwriter

config = AutoConfig(search_path=".env")



class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        return Response({"username": request.user.username, "email": request.user.email})



class ModelFileViewSet(viewsets.ModelViewSet):
    serializer_class = ModelFileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ModelFile.objects.filter(user=self.request.user)

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



def generate_report(request):
    format = request.GET.get('format', 'pdf')

    if format == 'pdf':
        return generate_pdf()
    elif format == 'excel':
        return generate_excel()

    else:
        return HttpResponse("Invalid format", status=400)

def generate_pdf():
    buffer = io.BytesIO()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="generated-file.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.drawString(100, 750, "3D Model Report")
    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return response

def generate_excel():
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
 
    worksheet.write(0, 0, "Defect 1")
    worksheet.write(0, 1, "Defect 2")

    workbook.close()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="report.xlsx"'
    return response



