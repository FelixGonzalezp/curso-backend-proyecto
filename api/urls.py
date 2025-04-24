from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    TipoMedidaViewSet,
    MedidaViewSet,
    PlanViewSet,
    OrganismoSectorialViewSet,
    PlanOrganismoSectorialViewSet,
    ReporteViewSet
)

router = DefaultRouter()
router.register(r"tipo-medida", TipoMedidaViewSet)
router.register(r"medida", MedidaViewSet)
router.register(r"plan", PlanViewSet)
router.register(r"organismo-sectorial", OrganismoSectorialViewSet)
router.register(r"plan-organismo-sectorial", PlanOrganismoSectorialViewSet)
router.register(r"reporte", ReporteViewSet)

urlpatterns = [
    path("", include(router.urls))
]


