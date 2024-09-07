from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import api_restfulViewSet  # Atualizado para o nome correto

router = DefaultRouter()
router.register(r'api_restful', api_restfulViewSet)  # Atualizado para o nome correto

urlpatterns = [
    path('', include(router.urls)),
]
