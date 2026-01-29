from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Cliente, Proyecto, Tarea, SubTarea
from .serializers import ClienteSerializer, ProyectoSerializer, TareaSerializer, SubTareaSerializer

# [cite: 50-58] Permiso Personalizado para diferenciar entre Administrador y Cliente
class IsAdminOrReadOnlyClient(permissions.BasePermission):
    def has_permission(self, request, view):
        # El Administrador tiene permiso total (CRUD) 
        if request.user.is_staff:
            return True
        # El Cliente solo tiene permisos de lectura (GET) [cite: 54, 57]
        return request.method in permissions.SAFE_METHODS

# [cite: 63-67] ViewSet de Clientes
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.filter(activo=True) # Solo lista clientes activos 
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAdminUser] # Solo el admin gestiona clientes [cite: 51]

    #  Implementación de Eliminación Lógica
    def perform_destroy(self, instance):
        instance.activo = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

# [cite: 68-72] ViewSet de Proyectos con Aislamiento de Datos
class ProyectoViewSet(viewsets.ModelViewSet):
    serializer_class = ProyectoSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnlyClient]

    def get_queryset(self):
        user = self.request.user
        # Si es Admin, ve todo [cite: 53]
        if user.is_staff:
            return Proyecto.objects.all()
        # Si es Cliente, solo ve sus proyectos (Aislamiento de datos) [cite: 55, 58]
        return Proyecto.objects.filter(cliente__email=user.email)

# [cite: 73-78] ViewSet de Tareas
class TareaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnlyClient]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Tarea.objects.all()
        # El cliente solo ve tareas de sus proyectos [cite: 56, 58]
        return Tarea.objects.filter(proyecto__cliente__email=user.email)

# [cite: 79-83] ViewSet de SubTareas
class SubTareaViewSet(viewsets.ModelViewSet):
    serializer_class = SubTareaSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnlyClient]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return SubTarea.objects.all()
        # El cliente solo ve subtareas de sus tareas [cite: 56, 58]
        return SubTarea.objects.filter(tarea__proyecto__cliente__email=user.email)