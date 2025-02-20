from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register,login, profile, upload_model

from .views import user_model_files, generate_pdf

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('user/models/', user_model_files, name='user-model-files'),
    path('user/upload-model/', upload_model, name='upload-model'),
    path('user/generate-pdf/', generate_pdf, name='generate_pdf'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
]
