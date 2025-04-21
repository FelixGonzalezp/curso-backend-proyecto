#proyecto_final\proyecto\django_proyecto\api\urls.py
from django.urls import path
from . import views_html

urlpatterns = [
    path('', views_html.home, name='html_home'),
    path('tipo-medida/', views_html.tipo_medida, name='html_tipo_medida'),
    path('plan/', views_html.plan, name='html_plan'),
    path('plan/crear/', views_html.crear_plan_view, name='html_crear_plan'),
    path('organismo-sectorial/', views_html.organismo_sectorial, name='html_organismo_sectorial'),
]