from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# [cite: 18-22] Modelo Cliente: Almacena la información de la empresa contratante.
class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True) # [cite: 20] Garantiza que no existan correos duplicados.
    empresa = models.CharField(max_length=255)
    activo = models.BooleanField(default=True) # [cite: 22, 67] Para implementar la eliminación lógica.
    fecha_creacion = models.DateTimeField(auto_now_add=True) # [cite: 23] Registro automático de creación.

    def __str__(self):
        return f"{self.nombre} ({self.empresa})"

# [cite: 24-31] Modelo Proyecto: Representa el esfuerzo principal asociado a un cliente.
class Proyecto(models.Model):
    # [cite: 27] Opciones de estado según requerimiento.
    ESTADOS_PROYECTO = [
        ('Pendiente', 'Pendiente'),
        ('En Desarrollo', 'En Desarrollo'),
        ('En Pruebas', 'En Pruebas'),
        ('Finalizado', 'Finalizado'),
    ]
    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS_PROYECTO, default='Pendiente')
    # [cite: 28, 91] Validación de rango 0-100.
    progreso = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='proyectos') # [cite: 29] Relación 1:N.
    fecha_inicio = models.DateField()
    fecha_entrega = models.DateField()

    # [cite: 92, 112] Lógica avanzada: Cálculo automático del progreso basado en tareas.
    def actualizar_progreso(self):
        tareas = self.tareas.all()
        if tareas.exists():
            total_progreso = sum(t.progreso for t in tareas)
            self.progreso = int(total_progreso / tareas.count())
            self.save()

    def __str__(self):
        return self.nombre

# [cite: 32-38] Modelo Tarea: Desglose de actividades de un proyecto.
class Tarea(models.Model):
    ESTADOS_TAREA = [
        ('Pendiente', 'Pendiente'),
        ('En Progreso', 'En Progreso'),
        ('Bloqueada', 'Bloqueada'),
        ('Completada', 'Completada'),
    ]
    
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS_TAREA, default='Pendiente')
    progreso = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas') # [cite: 37]
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Sobrecarga del método save para disparar el recálculo en el Proyecto padre.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.proyecto.actualizar_progreso()

    def __str__(self):
        return f"{self.titulo} - {self.proyecto.nombre}"

# [cite: 39-44] Modelo SubTarea: Nivel mínimo de detalle de una tarea.
class SubTarea(models.Model):
    titulo = models.CharField(max_length=255)
    completada = models.BooleanField(default=False)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='subtareas') # [cite: 43]
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo