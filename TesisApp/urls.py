from django.urls import re_path
from TesisApp import views

urlpatterns = [
    re_path(r'^registros$', views.lista_registros),
    re_path(r'^predecir$', views.predecir),
    re_path(r'^filtro$', views.lista_conteo_depto),
    re_path(r'^num_riesgo$', views.conteo_riesgo),
    re_path(r'^departamentos$', views.lista_departamentos),
]
