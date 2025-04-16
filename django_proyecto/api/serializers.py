from rest_framework import serializers
from .models import TipoMedida, Plan, OrganismoSectorial, Medida, PlanOrganismoSectorial, Reporte

class TipoMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMedida
        fields = '__all__'  # O usa una lista de campos específicos si lo prefieres

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class OrganismoSectorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoSectorial
        fields = '__all__'

class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = '__all__'

class PlanOrganismoSectorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanOrganismoSectorial
        fields = '__all__'

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'
