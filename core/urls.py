from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProyectoViewSet, TareaViewSet, SubTareaViewSet

# El router genera automáticamente las rutas GET, POST, PUT, DELETE
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente') # [cite: 63]
router.register(r'proyectos', ProyectoViewSet, basename='proyecto') # [cite: 68]
router.register(r'tareas', TareaViewSet, basename='tarea') # [cite: 73]
router.register(r'subtareas', SubTareaViewSet, basename='subtarea') # [cite: 79]

urlpatterns = [
    path('', include(router.urls)),
]