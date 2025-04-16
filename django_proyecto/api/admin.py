from django.contrib import admin
from .models import (
    Item,
    TipoMedida,
    Medida,
    OrganismoSectorial,
    Plan,
    PlanOrganismoSectorial,
    Reporte
)

# Register your models here.
admin.site.register(Item)
admin.site.register(TipoMedida)
admin.site.register(Medida)
admin.site.register(OrganismoSectorial)
admin.site.register(Plan)
admin.site.register(PlanOrganismoSectorial)
admin.site.register(Reporte)
