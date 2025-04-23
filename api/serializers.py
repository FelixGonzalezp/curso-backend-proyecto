from rest_framework import serializers
from .models import TipoMedida, Plan, OrganismoSectorial, Medida, PlanOrganismoSectorial, Reporte
from datetime import datetime
from django.utils import timezone

class TipoMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMedida
        fields = '__all__'  # O usa una lista de campos específicos si lo prefieres

    def validate_nombre(self, value):
        if not value:
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

    def validate_fecha_inicio(self, value):
        fecha_termino = self.initial_data.get('fecha_termino')
        if fecha_termino:
            fecha_termino = datetime.strptime(fecha_termino, '%Y-%m-%d').date()
            if value > fecha_termino:
                raise serializers.ValidationError("La fecha de inicio no puede ser mayor que la fecha de término.")
        return value

    def validate_fecha_termino(self, value):
        fecha_inicio = self.initial_data.get('fecha_inicio')
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            if value < fecha_inicio:
                raise serializers.ValidationError("La fecha de término no puede ser menor que la fecha de inicio.")
        return value

class OrganismoSectorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoSectorial
        fields = '__all__'

    def validate_nombre(self, value):
        if not value:
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = '__all__'

    def validate_nombre_corto(self, value):
        if not value:
            raise serializers.ValidationError("El nombre corto no puede estar vacío.")
        return value

class PlanOrganismoSectorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanOrganismoSectorial
        fields = '__all__'

    def validate_id_plan(self, value):
        if not value:
            raise serializers.ValidationError("El plan no puede estar vacío.")
        return value

    def validate_id_organismo_sectorial(self, value):
        if not value:
            raise serializers.ValidationError("El organismo sectorial no puede estar vacío.")
        return value

    def validate_id_media(self, value):
        if not value:
            raise serializers.ValidationError("La medida no puede estar vacía.")
        return value

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'

    def validate_fecha_reporte(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("La fecha de reporte no puede ser en el futuro.")
        return value
