from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import ModelFile

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserSerializer, ModelFileSerializer

from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage
import os

from decouple import AutoConfig
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

config = AutoConfig(search_path='.env')


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    """
    Login a user and return access and refresh tokens.
    """

    print("Here in login")
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(password):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

  
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

   
    return Response({
        'refresh': str(refresh),
        'access': str(access_token),
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user  
    return Response({
        'username': user.username,
        'email': user.email,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def user_model_files(request):
    print(request.user)
    user_models =ModelFile.objects.filter(user=request.user)
    serializer = ModelFileSerializer(user_models, many=True)
    return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_model(request):
    print("In add model")
   
    parser_classes = [MultiPartParser, FormParser]
    
    
    if 'model_file' not in request.FILES:
        return Response({'detail': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    model_file = request.FILES['model_file']
    file_directory = request.user.username 

  
    fs = FileSystemStorage(location=os.path.join(config("NGINX_PATH"), file_directory))  # Path where files will be stored
    file_name = fs.save(model_file.name, model_file)
    file_path = fs.url(file_name)  

   
    model_instance = ModelFile.objects.create(
        user=request.user,
        file_name=file_name,
        file_path=file_path  
    )
    
    return Response({
        'message': 'File uploaded successfully'
    }, status=status.HTTP_201_CREATED)







def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="generated-file.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    
    pdf.drawString(100, 750, "Report")

    pdf.showPage()
    pdf.save()

    return response
