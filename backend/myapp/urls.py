from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from myapp.views import (
    AuthViewSet,
    UserViewSet,
    ModelFileViewSet,
    DefectAnalysisViewSet,
    analysis_report
)

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth') 
router.register(r'model-files', ModelFileViewSet, basename='model-files') 
router.register(r'analysis', DefectAnalysisViewSet, basename='analysis')
router.register(r'users', UserViewSet, basename='users') 
urlpatterns = [
    path('', include(router.urls)), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('model/<int:modelid>/report/', analysis_report, name='analysis_report'),
]