from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import serializers
from django.shortcuts import render

from .models import *
from .serializers import *

# Serializer para mensajes de error
class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()

def home(request):
    return render(request, 'home.html')

##### Tabla TIPO MEDIDA #######
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def tipo_medida(request):
    data = TipoMedida.objects.all()
    return render(request, 'tipo_medida.html', {'tipos_medida': data})

##### Tabla PLAN #######
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def plan(request):
    planes = Plan.objects.all()
    return render(request, 'planes.html', {'planes': planes})

@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def crear_plan_view(request):
    """Vista para mostrar el formulario de creación de planes"""
    return render(request, 'crear_plan.html')

@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def organismo_sectorial(request):
    os = OrganismoSectorial.objects.all()
    return render(request, 'organismo_sectorial.html', {'organismos': os})