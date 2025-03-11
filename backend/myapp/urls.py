from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ModelFileViewSet, AuthViewSet, generate_report


router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth') 
router.register(r'model-files', ModelFileViewSet, basename='model-files') 

urlpatterns = [
    path('', include(router.urls)), 
    path("generate-report/", generate_report, name="generate-report"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]