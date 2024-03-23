from django.urls import re_path
from TesisApp import views

urlpatterns = [
    re_path(r'^registros$', views.lista_registros),
    re_path(r'^predecir$', views.predecir),
    re_path(r'^filtro$', views.lista_conteo_depto),
    re_path(r'^num_riesgo$', views.conteo_riesgo),
    re_path(r'^departamentos$', views.lista_departamentos),
    re_path(r'^conteo_depto$', views.lista_conteo_depto_v2),
    re_path(r'^conteo_nivel_edu_marihuana$', views.lista_conteo_nivel_edu_marihuana),
    re_path(r'^conteo_riesgo_edad$', views.lista_conteo_riesgo_edad),
    re_path(r'^conteo_riesgo_situacion_actual$', views.lista_conteo_riesgo_situacion_actual),
    re_path(r'^conteo_riesgo_sexo_tipo$', views.lista_conteo_riesgo_per_sexo_tipo),
    re_path(r'^lista_variables$', views.lista_variables)
]
