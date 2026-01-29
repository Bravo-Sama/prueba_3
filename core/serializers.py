from rest_framework import serializers
from .models import Cliente, Proyecto, Tarea, SubTarea

# [cite: 39-44] Serializador para SubTareas
class SubTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTarea
        fields = '__all__'

# [cite: 32-38] Serializador para Tareas con validación de progreso
class TareaSerializer(serializers.ModelSerializer):
    # Permite visualizar las subtareas asociadas al listar tareas
    subtareas = SubTareaSerializer(many=True, read_only=True)

    class Meta:
        model = Tarea
        fields = '__all__'

    #  Validación: El progreso debe estar entre 0 y 100
    def validate_progreso(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("El progreso debe ser un número entero entre 0 y 100.")
        return value

# [cite: 24-31] Serializador para Proyectos
class ProyectoSerializer(serializers.ModelSerializer):
    # Incluye las tareas para cumplir con la visualización de avance
    tareas = TareaSerializer(many=True, read_only=True)

    class Meta:
        model = Proyecto
        fields = '__all__'
    
    #  Validación de progreso para el proyecto
    def validate_progreso(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("El progreso del proyecto debe estar entre 0 y 100.")
        return value

# [cite: 18-22] Serializador para Clientes
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'