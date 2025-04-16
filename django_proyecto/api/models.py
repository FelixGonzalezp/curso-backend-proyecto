from django.db import models
from django.utils import timezone

### Para admin
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
###


class TipoMedida(models.Model):
    id_tipo_medida = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_tipo_medida} - {self.nombre}"

class Medida(models.Model):
    id_media = models.AutoField(primary_key=True)
    id_tipo_medida = models.ForeignKey('TipoMedida', models.DO_NOTHING, db_column='id_tipo_medida')
    nombre_corto = models.CharField(max_length=300, default="Actualizar")
    indicador = models.CharField(max_length=300)
    forma_calculo = models.CharField(max_length=300)
    frecuencia_reporte = models.CharField(max_length=300)
    medios_verificacion = models.CharField(max_length=300, default="Actualizar")
    tipo_regulatoria = models.CharField(max_length=300, default="Actualizar")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_media} - {self.nombre_corto}"

class OrganismoSectorial(models.Model):
    id_organismo_sectorial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_organismo_sectorial} - {self.nombre}"

class Plan(models.Model):
    id_plan = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    responsable = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_plan} - {self.nombre}"
    
class PlanOrganismoSectorial(models.Model):
    id_plan_organismo_sectorial = models.AutoField(primary_key=True)
    id_plan = models.ForeignKey('Plan', models.DO_NOTHING, db_column='id_plan')
    id_organismo_sectorial = models.ForeignKey('OrganismoSectorial', models.DO_NOTHING, db_column='id_organismo_sectorial')
    id_media = models.ForeignKey('Medida', models.DO_NOTHING, db_column='id_media')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_plan_organismo_sectorial}"
    

class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    id_plan_organismo_sectorial = models.ForeignKey('PlanOrganismoSectorial', models.DO_NOTHING, db_column='id_plan_organismo_sectorial')
    valor_reportado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_reporte = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id_reporte}"
    
