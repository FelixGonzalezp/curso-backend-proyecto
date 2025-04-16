from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from django.db import transaction, IntegrityError

from .models import *
from .serializers import *

# Serializer para mensajes de error
class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()

# Custom permission classes
class IsAdministrador(BasePermission):
    """
    Permite acceso solo a usuarios con rol de Administrador.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Administrador').exists()

class IsOrganismoSectorial(BasePermission):
    """
    Permite acceso solo a usuarios con rol de OrganismoSectorial.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='OrganismoSectorial').exists()

##### Tabla TIPO MEDIDA #######
@extend_schema(
    methods=['GET'],
    description="Devuelve la lista de tipos de medida existentes.",
    responses={200: TipoMedidaSerializer(many=True)}
)
@extend_schema(
    methods=['POST'],
    description="Crea un nuevo tipo de medida.",
    request=TipoMedidaSerializer,
    responses={
        201: TipoMedidaSerializer,
        400: OpenApiResponse(
            response=ErrorSerializer,
            description="Error de validación"
        )
    },
    examples=[
        OpenApiExample(
            "Ejemplo de solicitud",
            summary="Ejemplo de JSON para crear un tipo de medida",
            description="El cuerpo de la solicitud debe contener `nombre` y `descripcion`.",
            value={
                "nombre": "Nueva Medida",
                "descripcion": "Descripción de la nueva medida"
            },
            request_only=True
        )
    ]
)
@api_view(['GET', 'POST'])
def tipo_medida(request):
    """
    API para gestionar los tipos de medida.

    Métodos:
        - **GET**: Devuelve la lista de tipos de medida.
        - **POST**: Crea un nuevo tipo de medida.

    ### **Parámetros (POST)**
    - `nombre` (str, requerido): Nombre del tipo de medida.
    - `descripcion` (str, requerido): Descripción del tipo de medida.

    ### **Respuestas**
    - **GET 200**: Lista de tipos de medida.
    - **POST 201**: Tipo de medida creado exitosamente.
    - **POST 400**: Error de validación.
    """
    if request.method == "GET":
        # Verificar permisos manualmente
        if not (IsAuthenticated().has_permission(request, None) or 
                IsAdministrador().has_permission(request, None) or 
                IsOrganismoSectorial().has_permission(request, None)):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        return Response((TipoMedidaSerializer((TipoMedida.objects.all()), many=True)).data)
    elif request.method == "POST":
        # Verificar permisos manualmente
        if not IsAdministrador().has_permission(request, None):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        serializer = TipoMedidaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"detail": serializer.errors}, status=400)

##### Tabla MEDIDA #######
@extend_schema(
    methods=['GET'],
    description="Devuelve la lista de medidas existentes.",
    responses={200: MedidaSerializer(many=True)}
)
@extend_schema(
    methods=['POST'],
    description="Crea una nueva medida.",
    request=MedidaSerializer,
    responses={
        201: MedidaSerializer,
        400: OpenApiResponse(
            response=ErrorSerializer,
            description="Error de validación"
        )
    },
    examples=[
        OpenApiExample(
            "Ejemplo de solicitud",
            summary="Ejemplo de JSON para crear una medida",
            description="El cuerpo de la solicitud debe contener los datos de la medida.",
            value={
                "id_tipo_medida": 1,
                "nombre_corto": "Nombre corto de la medida",
                "indicador": "Indicador de la medida",
                "forma_calculo": "Forma de cálculo de la medida",
                "frecuencia_reporte": "Mensual",
                "medios_verificacion": "Medios de verificación",
                "tipo_regulatoria": "Tipo regulatoria"
            },
            request_only=True
        )
    ]
)
@api_view(['GET', 'POST'])
def medida(request):
    """
    API para gestionar las medidas.

    Métodos:
        - **GET**: Devuelve la lista de medidas.
        - **POST**: Crea una nueva medida.

    ### **Parámetros (POST)**
    - `id_tipo_medida` (int, requerido): ID del tipo de medida asociado.
    - `nombre_corto` (str, opcional): Nombre corto de la medida.
    - `indicador` (str, requerido): Indicador de la medida.
    - `forma_calculo` (str, requerido): Forma de cálculo de la medida.
    - `frecuencia_reporte` (str, requerido): Frecuencia de reporte de la medida.
    - `medios_verificacion` (str, opcional): Medios de verificación de la medida.
    - `tipo_regulatoria` (str, opcional): Tipo regulatorio de la medida.

    ### **Respuestas**
    - **GET 200**: Lista de medidas.
    - **POST 201**: Medida creada exitosamente.
    - **POST 400**: Error de validación.
    """
    if request.method == "GET":
        # Verificar permisos manualmente
        if not (IsAuthenticated().has_permission(request, None) or 
                IsAdministrador().has_permission(request, None) or 
                IsOrganismoSectorial().has_permission(request, None)):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        return Response((MedidaSerializer((Medida.objects.all()), many=True)).data)
    elif request.method == "POST":
        # Verificar permisos manualmente
        if not IsAdministrador().has_permission(request, None):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        serializer = MedidaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"detail": serializer.errors}, status=400)

##### Tabla PLAN #######
@extend_schema(
    methods=['GET'],
    description="Devuelve la lista de planes existentes.",
    responses={200: PlanSerializer(many=True)}
)
@extend_schema(
    methods=['POST'],
    description="Crea un nuevo plan.",
    request=PlanSerializer,
    responses={
        201: PlanSerializer,
        400: OpenApiResponse(
            response=ErrorSerializer,
            description="Error de validación"
        )
    },
    examples=[
        OpenApiExample(
            "Ejemplo de solicitud",
            summary="Ejemplo de JSON para crear un plan",
            description="El cuerpo de la solicitud debe contener los datos del plan.",
            value={
                "nombre": "Nuevo Plan",
                "descripcion": "Descripción del nuevo plan",
                "fecha_inicio": "2024-01-01",
                "fecha_termino": "2024-12-31",
                "responsable": "Juan Pérez",
                "estado": True
            },
            request_only=True
        )
    ]
)
@api_view(['GET', 'POST'])
def plan(request):
    """
    API para gestionar los planes.

    Métodos:
        - **GET**: Devuelve la lista de planes disponibles.
        - **POST**: Crea un nuevo plan.

    ### **Parámetros (POST)**
    - `nombre` (str, requerido): Nombre único del plan.
    - `descripcion` (str, requerido): Descripción del plan.
    - `fecha_inicio` (date, requerido): Fecha de inicio del plan.
    - `fecha_termino` (date, requerido): Fecha de término del plan.
    - `responsable` (str, requerido): Nombre del responsable del plan.
    - `estado` (bool, opcional): Estado del plan (default: True).

    ### **Respuestas**
    - **GET 200**: Lista de planes.
    - **POST 201**: Plan creado exitosamente.
    - **POST 400**: Error de validación.
    """
    if request.method == "GET":
        # Verificar permisos manualmente
        if not (IsAuthenticated().has_permission(request, None) or 
                IsAdministrador().has_permission(request, None) or 
                IsOrganismoSectorial().has_permission(request, None)):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        return Response((PlanSerializer((Plan.objects.all()), many=True)).data)
    elif request.method == "POST":
        # Verificar permisos manualmente
        if not IsAdministrador().has_permission(request, None):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        # Si los datos vienen como form-data
        if request.content_type == 'application/x-www-form-urlencoded':
            data = request.POST
        # Si los datos vienen como JSON
        else:
            data = request.data
            
        serializer = PlanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Si es una solicitud API, devuelve JSON
            return Response(serializer.data, status=201)

        # Si es una solicitud API, devuelve JSON con errores
        return Response({"detail": serializer.errors}, status=400)

##### Tabla ORGANISMO SECTORIAL #######
@extend_schema(
    methods=['GET'],
    description="Devuelve la lista de organismos sectoriales existentes.",
    responses={200: OrganismoSectorialSerializer(many=True)}
)
@extend_schema(
    methods=['POST'],
    description="Crea un nuevo organismo sectorial.",
    request=OrganismoSectorialSerializer,
    responses={
        201: OrganismoSectorialSerializer,
        400: OpenApiResponse(
            response=ErrorSerializer,
            description="Error de validación"
        )
    },
    examples=[
        OpenApiExample(
            "Ejemplo de solicitud",
            summary="Ejemplo de JSON para crear un organismo sectorial",
            description="El cuerpo de la solicitud debe contener los datos del organismo.",
            value={
                "nombre": "Nuevo Organismo",
                "tipo": "Tipo de Organismo",
                "contacto": "contacto@organismo.com"
            },
            request_only=True
        )
    ]
)
@api_view(['GET', 'POST'])
def organismo_sectorial(request):
    """
    API para gestionar los organismos sectoriales.

    Métodos:
        - **GET**: Devuelve la lista de organismos sectoriales.
        - **POST**: Crea un nuevo organismo sectorial.

    ### **Parámetros (POST)**
    - `nombre` (str, requerido): Nombre único del organismo sectorial.
    - `tipo` (str, requerido): Tipo de organismo sectorial.
    - `contacto` (str, requerido): Información de contacto del organismo.

    ### **Respuestas**
    - **GET 200**: Lista de organismos sectoriales.
    - **POST 201**: Organismo sectorial creado exitosamente.
    - **POST 400**: Error de validación.
    """
    if request.method == "GET":
        # Verificar permisos manualmente
        if not (IsAuthenticated().has_permission(request, None) or 
                IsAdministrador().has_permission(request, None) or 
                IsOrganismoSectorial().has_permission(request, None)):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        return Response((OrganismoSectorialSerializer((OrganismoSectorial.objects.all()), many=True)).data)
    elif request.method == "POST":
        # Verificar permisos manualmente
        if not IsAdministrador().has_permission(request, None):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        serializer = OrganismoSectorialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"detail": serializer.errors}, status=400)
    
##### Tabla PLAN ORGANISMO SECTORIAL #######
@extend_schema(
    methods=['GET'],
    description="Devuelve la lista de relaciones entre planes, organismos sectoriales y medidas.",
    responses={200: PlanOrganismoSectorialSerializer(many=True)}
)
@extend_schema(
    methods=['POST'],
    description="Crea una nueva relación entre plan, organismo sectorial y medida.",
    request=PlanOrganismoSectorialSerializer,
    responses={
        201: PlanOrganismoSectorialSerializer,
        400: OpenApiResponse(
            response=ErrorSerializer,
            description="Error de validación"
        )
    },
    examples=[
        OpenApiExample(
            "Ejemplo de solicitud",
            summary="Ejemplo de JSON para crear una relación plan-organismo-medida",
            description="El cuerpo de la solicitud debe contener los IDs de plan, organismo sectorial y medida.",
            value={
                "id_plan": 1,
                "id_organismo_sectorial": 1,
                "id_media": 1
            },
            request_only=True
        )
    ]
)
@api_view(['GET', 'POST'])
def plan_organismo_sectorial(request):
    """
    API para gestionar las relaciones entre planes, organismos sectoriales y medidas.

    Métodos:
        - **GET**: Devuelve la lista de relaciones plan-organismo-medida.
        - **POST**: Crea una nueva relación plan-organismo-medida.

    ### **Parámetros (POST)**
    - `id_plan` (int, requerido): ID del plan.
    - `id_organismo_sectorial` (int, requerido): ID del organismo sectorial.
    - `media` (int, [int], requerido): ID's de la medida.

    ### **Respuestas**
    - **GET 200**: Lista de relaciones plan-organismo-medida.
    - **POST 201**: Relación creada exitosamente.
    - **POST 400**: Error de validación.
    """
    if request.method == "GET":
        # Verificar permisos manualmente
        if not (IsAuthenticated().has_permission(request, None) or 
                IsAdministrador().has_permission(request, None) or 
                IsOrganismoSectorial().has_permission(request, None)):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        return Response((PlanOrganismoSectorialSerializer((PlanOrganismoSectorial.objects.all()), many=True)).data)
    elif request.method == "POST":
        # Verificar permisos manualmente
        if not IsAdministrador().has_permission(request, None):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        data = request.data
        id_plan = data.get("id_plan")
        id_organismo = data.get("id_organismo_sectorial")
        medidas = data.get("medidas")
        
        # 2. Validar campos obligatorios
        errores = {}
        if id_plan is None:
            errores["id_plan"] = "Este campo es obligatorio."
        if id_organismo is None:
            errores["id_organismo_sectorial"] = "Este campo es obligatorio."
        if medidas is None:
            errores["medidas"] = "Este campo es obligatorio."

        if errores:
            return Response({"detail": errores}, status=400)
        
        # 3. Normalizar medidas
        if isinstance(medidas, int):
            medidas = [medidas]
        elif not isinstance(medidas, list):
            return Response({"detail": "El campo 'medidas' debe ser un entero o una lista de enteros."}, status=400)

        if len(medidas) != len(set(medidas)):
            return Response({"detail": "Existen medidas duplicadas."}, status=400)
        
        try:
            with transaction.atomic():
                instancias_creadas = []

                for id_medida in medidas:
                    existe = PlanOrganismoSectorial.objects.filter(
                        id_plan_id=id_plan,
                        id_organismo_sectorial_id=id_organismo,
                        id_media_id=id_medida
                    ).exists()

                    if existe:
                        raise serializers.ValidationError(
                            f"La medida {id_medida} ya está asociada al plan y organismo."
                        )

                    serializer = PlanOrganismoSectorialSerializer(data={
                        "id_plan": id_plan,
                        "id_organismo_sectorial": id_organismo,
                        "id_media": id_medida
                    })

                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    instancias_creadas.append(serializer.data)

            return Response({
                "mensaje": "Las medidas fueron asociadas correctamente.",
                "cantidad": len(instancias_creadas),
                "datos": instancias_creadas
            }, status=201)

        except serializers.ValidationError as e:
            return Response({"detail": e.detail}, status=400)

        except IntegrityError:
            return Response({
                "detail": "Error de integridad. No se realizaron cambios."
            }, status=500)

        except Exception as e:
            return Response({
                "detail": f"Error inesperado: {str(e)}"
            }, status=500)

        
        # serializer = PlanOrganismoSectorialSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=201)
        # return Response({"detail": serializer.errors}, status=400)

##### Tabla REPORTE #######
@extend_schema(
    methods=['GET'],
    description="Devuelve la lista de reportes existentes.",
    responses={200: ReporteSerializer(many=True)}
)
@extend_schema(
    methods=['POST'],
    description="Crea un nuevo reporte.",
    request=ReporteSerializer,
    responses={
        201: ReporteSerializer,
        400: OpenApiResponse(
            response=ErrorSerializer,
            description="Error de validación"
        )
    },
    examples=[
        OpenApiExample(
            "Ejemplo de solicitud",
            summary="Ejemplo de JSON para crear un reporte",
            description="El cuerpo de la solicitud debe contener los datos del reporte.",
            value={
                "id_plan_organismo_sectorial": 1,
                "valor_reportado": 95.50,
                "fecha_reporte": "2024-05-15"
            },
            request_only=True
        )
    ]
)
@api_view(['GET', 'POST'])
def reporte(request):
    """
    API para gestionar los reportes.

    Métodos:
        - **GET**: Devuelve la lista de reportes.
        - **POST**: Crea un nuevo reporte.

    ### **Parámetros (POST)**
    - `id_plan_organismo_sectorial` (int, requerido): ID de la relación plan-organismo-medida.
    - `valor_reportado` (decimal, requerido): Valor numérico reportado.
    - `fecha_reporte` (date, requerido): Fecha del reporte.

    ### **Respuestas**
    - **GET 200**: Lista de reportes.
    - **POST 201**: Reporte creado exitosamente.
    - **POST 400**: Error de validación.
    """
    if request.method == "GET":
        # Verificar permisos manualmente
        if not (IsAuthenticated().has_permission(request, None) or 
                IsAdministrador().has_permission(request, None) or 
                IsOrganismoSectorial().has_permission(request, None)):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        return Response((ReporteSerializer((Reporte.objects.all()), many=True)).data)
    elif request.method == "POST":
        # Verificar permisos manualmente
        if not (IsAdministrador().has_permission(request, None) or 
                IsOrganismoSectorial().has_permission(request, None)):
            return Response({"detail": "No tiene permisos para realizar esta acción."}, status=403)
        
        serializer = ReporteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"detail": serializer.errors}, status=400)
