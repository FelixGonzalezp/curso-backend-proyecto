from django.db import models
from django.utils import timezone

### Para admin
class Item(models.Model):
   """
   Modelo para representar un ítem en el sistema.

   Attributes:
       name (str): Nombre del ítem.
       description (str): Descripción del ítem.
   """
   name = models.CharField(max_length=100)
   description = models.TextField()

class TipoMedida(models.Model):
   """
   Modelo para representar un tipo de medida.

   Attributes:
       nombre (str): Nombre del tipo de medida.
       descripcion (str): Descripción del tipo de medida.
       created_at (datetime): Fecha y hora de creación del registro.
       updated_at (datetime): Fecha y hora de la última actualización del registro.
   """
   nombre = models.CharField(max_length=100, unique=True)
   descripcion = models.TextField()
   created_at = models.DateTimeField(default=timezone.now)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
       return f"{self.id} - {self.nombre}"

class Medida(models.Model):
   """
   Modelo para representar una medida.

   Attributes:
       id_tipo_medida (ForeignKey): Referencia al tipo de medida.
       nombre_corto (str): Nombre corto de la medida.
       indicador (str): Indicador de la medida.
       forma_calculo (str): Forma de cálculo de la medida.
       frecuencia_reporte (str): Frecuencia de reporte de la medida.
       medios_verificacion (str): Medios de verificación de la medida.
       tipo_regulatoria (str): Tipo regulatoria de la medida.
       created_at (datetime): Fecha y hora de creación del registro.
       updated_at (datetime): Fecha y hora de la última actualización del registro.
   """
   id_tipo_medida = models.ForeignKey('TipoMedida', models.DO_NOTHING, db_column='id_tipo_medida')
   nombre_corto = models.CharField(max_length=300, default="Actualizar")
   indicador = models.CharField(max_length=300)
   forma_calculo = models.CharField(max_length=300)
   frecuencia_reporte = models.CharField(max_length=300)
   medios_verificacion = models.CharField(max_length=300, default="Actualizar")
   tipo_regulatoria = models.CharField(max_length=300, default="Actualizar")
   created_at = models.DateTimeField(default=timezone.now)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
       return f"{self.id} - {self.nombre_corto}"

class OrganismoSectorial(models.Model):
   """
   Modelo para representar un organismo sectorial.

   Attributes:
       nombre (str): Nombre del organismo sectorial.
       tipo (str): Tipo del organismo sectorial.
       contacto (str): Información de contacto del organismo sectorial.
       created_at (datetime): Fecha y hora de creación del registro.
       updated_at (datetime): Fecha y hora de la última actualización del registro.
   """
   nombre = models.CharField(max_length=100, unique=True)
   tipo = models.CharField(max_length=100)
   contacto = models.CharField(max_length=100)
   created_at = models.DateTimeField(default=timezone.now)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
       return f"{self.id} - {self.nombre}"

class Plan(models.Model):
    """
    Modelo para representar un plan.

    Attributes:
        nombre (str): Nombre del plan.
        descripcion (str): Descripción del plan.
        fecha_inicio (date): Fecha de inicio del plan.
        fecha_termino (date): Fecha de término del plan.
        responsable (str): Responsable del plan.
        estado (str): Estado del plan (Sin iniciar, En progreso, Finalizado, Atrasado).
        created_at (datetime): Fecha y hora de creación del registro.
        updated_at (datetime): Fecha y hora de la última actualización del registro.
    """
    ESTADO_CHOICES = [
        ('sin_iniciar', 'Sin iniciar'),
        ('en_progreso', 'En progreso'),
        ('finalizado', 'Finalizado'),
        ('atrasado', 'Atrasado'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    responsable = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='sin_iniciar')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.nombre}"

class PlanOrganismoSectorial(models.Model):
   """
   Modelo para representar la relación entre un plan y un organismo sectorial.

   Attributes:
       id_plan (ForeignKey): Referencia al plan.
       id_organismo_sectorial (ForeignKey): Referencia al organismo sectorial.
       id_media (ForeignKey): Referencia a la medida.
       created_at (datetime): Fecha y hora de creación del registro.
       updated_at (datetime): Fecha y hora de la última actualización del registro.
   """
   id_plan = models.ForeignKey('Plan', models.DO_NOTHING, db_column='id_plan')
   id_organismo_sectorial = models.ForeignKey('OrganismoSectorial', models.DO_NOTHING, db_column='id_organismo_sectorial')
   id_media = models.ForeignKey('Medida', models.DO_NOTHING, db_column='id_media')
   created_at = models.DateTimeField(default=timezone.now)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
       return f"{self.id}"

class Reporte(models.Model):
   """
   Modelo para representar un reporte.

   Attributes:
       id_plan_organismo_sectorial (ForeignKey): Referencia a la relación entre el plan y el organismo sectorial.
       valor_reportado (Decimal): Valor reportado.
       fecha_reporte (date): Fecha del reporte.
       created_at (datetime): Fecha y hora de creación del registro.
       updated_at (datetime): Fecha y hora de la última actualización del registro.
   """
   id_plan_organismo_sectorial = models.ForeignKey('PlanOrganismoSectorial', models.DO_NOTHING, db_column='id_plan_organismo_sectorial')
   valor_reportado = models.DecimalField(max_digits=10, decimal_places=2)
   fecha_reporte = models.DateField()
   created_at = models.DateTimeField(default=timezone.now)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
       return f"{self.id}"
