#proyecto_final\proyecto\django_proyecto\api\urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('tipo-medida/', views.tipo_medida, name='tipo_medida'),
    path('plan/', views.plan, name='plan'),
    path('organismo-sectorial/', views.organismo_sectorial, name='organismo_sectorial'),
    path('medida/', views.medida, name='medida'),
    path('plan-organismo-sectorial/', views.plan_organismo_sectorial, name='plan_organismo_sectorial'),
    path('reporte/', views.reporte, name='reporte'),
]


