from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.http import Http404
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample, OpenApiResponse
from django.db import transaction, IntegrityError

from .models import TipoMedida
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

class IsAuthenticatedAndAdminOrSectorial(BasePermission):
    """
    Permite acceso solo a usuarios con rol de Administrador u OrganismoSectorial.
    """
    def has_permission(self, request, view):
        if not IsAuthenticated().has_permission(request, view):
            return False
        return (
            IsAdministrador().has_permission(request, view) or
            IsOrganismoSectorial().has_permission(request, view)
        )

@extend_schema_view(
    list=extend_schema(
        description="Devuelve la lista de tipos de medida existentes.",
        responses={200: TipoMedidaSerializer(many=True)}
    ),
    create=extend_schema(
        description="Crea un nuevo tipo de medida.",
        request=TipoMedidaSerializer,
        responses={
            201: TipoMedidaSerializer,
            400: OpenApiResponse(response=ErrorSerializer, description="Error de validación")
        },
        examples=[
            OpenApiExample(
                "Ejemplo de solicitud",
                summary="Ejemplo de JSON para crear un tipo de medida",
                description="Debe contener `nombre` y `descripcion`.",
                value={"nombre": "Nueva Medida", "descripcion": "Descripción de la nueva medida"},
                request_only=True
            )
        ]
    ),
    destroy=extend_schema(
        description="Elimina un tipo de medida por su ID.",
        responses={
            204: None,
            403: OpenApiResponse(description="No autorizado para eliminar."),
            404: OpenApiResponse(description="No encontrado.")
        }
    )
)
class TipoMedidaViewSet(ModelViewSet):
    queryset = TipoMedida.objects.filter(is_active=True)
    serializer_class = TipoMedidaSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdministrador()]
        return [IsAuthenticated()]
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail="No se encontró un registro con ese ID.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    list=extend_schema(
        description="Devuelve la lista de medidas existentes.",
        responses={200: MedidaSerializer(many=True)}
    )
)
class MedidaViewSet(ModelViewSet):
    queryset = Medida.objects.filter(is_active=True)
    serializer_class = MedidaSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdministrador()]
        elif self.action in ['list']:
            return [IsAuthenticatedAndAdminOrSectorial()]
        return [IsAuthenticated()]
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail="No se encontró un registro con ese ID.")

    @extend_schema(
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
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Elimina una medida por su ID.",
        responses={
            204: None,
            403: OpenApiResponse(description="No autorizado para eliminar."),
            404: OpenApiResponse(description="No encontrado.")
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    list=extend_schema(
        description="Devuelve la lista de planes existentes.",
        responses={200: PlanSerializer(many=True)}
    )
)
class PlanViewSet(ModelViewSet):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdministrador()]
        elif self.action == 'list':
            return [IsAuthenticatedAndAdminOrSectorial()]
        return [IsAuthenticated()]
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail="No se encontró un registro con ese ID.")

    @extend_schema(
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
                    "estado": "sin_iniciar"
                },
                request_only=True
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @extend_schema(
        description="Elimina una plan por su ID.",
        responses={
            204: None,
            403: OpenApiResponse(description="No autorizado para eliminar."),
            404: OpenApiResponse(description="No encontrado.")
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@extend_schema_view(
    list=extend_schema(
        description="Devuelve la lista de organismos sectoriales existentes.",
        responses={200: OrganismoSectorialSerializer(many=True)}
    )
)
class OrganismoSectorialViewSet(ModelViewSet):
    queryset = OrganismoSectorial.objects.filter(is_active=True)
    serializer_class = OrganismoSectorialSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdministrador()]
        elif self.action == 'list':
            return [IsAuthenticatedAndAdminOrSectorial()]
        return [IsAuthenticated()]
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail="No se encontró un registro con ese ID.")

    @extend_schema(
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
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        description="Elimina un organismo sectorial por su ID.",
        responses={
            204: None,
            403: OpenApiResponse(description="No autorizado para eliminar."),
            404: OpenApiResponse(description="No encontrado.")
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    list=extend_schema(
        description="Devuelve la lista de relaciones entre planes, organismos sectoriales y medidas.",
        responses={200: PlanOrganismoSectorialSerializer(many=True)}
    )
)
class PlanOrganismoSectorialViewSet(ModelViewSet):
    queryset = PlanOrganismoSectorial.objects.filter(is_active=True)
    serializer_class = PlanOrganismoSectorialSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdministrador()]
        elif self.action == 'list':
            return [IsAuthenticatedAndAdminOrSectorial()]
        return [IsAuthenticated()]
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail="No se encontró un registro con ese ID.")

    @extend_schema(
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
                    "id_medida": [1, 2, 3]  # Asumiendo que `id_medida` puede ser una lista de IDs
                },
                request_only=True
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        id_plan = data.get("id_plan")
        id_organismo = data.get("id_organismo_sectorial")
        id_medidas = data.get("id_media")

        # Normalizar a lista
        if isinstance(id_medidas, (int, str)):
            id_medidas = [int(id_medidas)]
        
        # Validación de campos obligatorios
        campos_obligatorios = {
            "id_plan": id_plan,
            "id_organismo_sectorial": id_organismo,
            "id_medida": id_medidas,
        }
        errores = {campo: ["Este campo es obligatorio."] for campo, valor in campos_obligatorios.items() if valor is None}
        if errores:
            print(data.get("id_media"))
            return Response({"detail": errores}, status=status.HTTP_400_BAD_REQUEST)

        # Validación de duplicados
        if len(id_medidas) != len(set(id_medidas)):
            return Response({"detail": "Existen medidas duplicadas."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                instancias_creadas = []

                relaciones_existentes = PlanOrganismoSectorial.objects.filter(
                    id_plan_id=id_plan,
                    id_organismo_sectorial_id=id_organismo,
                    id_media_id__in=id_medidas
                ).values_list('id_media_id', flat=True)
                medidas_duplicadas = set(relaciones_existentes)

                if medidas_duplicadas:
                    return Response({
                        "detail": f"Las siguientes medidas ya están asociadas: {sorted(medidas_duplicadas)}"
                    }, status=status.HTTP_400_BAD_REQUEST)

                campos_base = {
                    "id_plan": id_plan,
                    "id_organismo_sectorial": id_organismo,
                }
                for id_medida in id_medidas:
                    serializer = PlanOrganismoSectorialSerializer(data={
                        **campos_base,
                        "id_media": id_medida
                    })
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    instancias_creadas.append(serializer.data)

            return Response({
                "mensaje": "Las medidas fueron asociadas correctamente.",
                "cantidad": len(instancias_creadas),
                "datos": instancias_creadas
            }, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            return Response({
                "detail": f"Error de integridad. No se realizaron cambios. ({str(e)})"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({
                "detail": f"Error inesperado: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        description="Elimina un plan organismo sectorial por su ID.",
        responses={
            204: None,
            403: OpenApiResponse(description="No autorizado para eliminar."),
            404: OpenApiResponse(description="No encontrado.")
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@extend_schema_view(
    list=extend_schema(
        description="Devuelve la lista de reportes existentes.",
        responses={200: ReporteSerializer(many=True)}
    )
)
class ReporteViewSet(ModelViewSet):
    queryset = Reporte.objects.filter(is_active=True)
    serializer_class = ReporteSerializer

    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAuthenticated(), IsAdministrador()]
        elif self.action in ['create', 'list']:
            return [IsAuthenticatedAndAdminOrSectorial()]
        return [IsAuthenticated()]
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail="No se encontró un registro con ese ID.")
    
    @extend_schema(
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
                    "evidencia": "url de evidencia",
                    "fecha_reporte": "2024-05-15"
                },
                request_only=True
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        description="Elimina un reporte por su ID.",
        responses={
            204: None,
            403: OpenApiResponse(description="No autorizado para eliminar."),
            404: OpenApiResponse(description="No encontrado.")
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
