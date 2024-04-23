from TesisApp.entities import caracteristica
from TesisApp.utils import data_variables
import pandas as pd
import os

def get_tipo_riesgo(prm_filtro):
    if prm_filtro == "riesgo_muy_alto":
        return 4
    elif prm_filtro == "riesgo_alto":
        return 3
    elif prm_filtro == "riesgo_medio":
        return 2
    elif prm_filtro == "riesgo_bajo":
        return 1
    elif prm_filtro == "riesgo_muy_bajo":
        return 0
    else:
        return -1  

#Funcion para procesar las caracteristicas en su valor inicial
def obtenerDictProcesado(pipeline_columnas,importancia_caracteristicas_dict):
    nuevo_dict_caracteristicas_procesadas = {}
    sumatoria = 0
    promedio = 0
    num_caracteristicas = 0;
    for columna in pipeline_columnas:
        
        if columna == "residentes_hogar":
            importancia_caracteristicas_dict["residentes_hogar"] = importancia_caracteristicas_dict["residentes_hogar"]
        elif columna == "d2_04_num_hijos":
            nuevo_dict_caracteristicas_procesadas["d2_04_num_hijos"] = importancia_caracteristicas_dict["d2_04_num_hijos"]
        else:
            for clave in importancia_caracteristicas_dict:
                if columna in clave:
                    sumatoria = sumatoria + importancia_caracteristicas_dict[clave]
                    num_caracteristicas = num_caracteristicas + 1
            
            if num_caracteristicas > 1:
                promedio = sumatoria / num_caracteristicas
                nuevo_dict_caracteristicas_procesadas[columna] = promedio
            else:
                nuevo_dict_caracteristicas_procesadas[columna] = sumatoria
            
            sumatoria = 0
            promedio = 0
            num_caracteristicas = 0;
    
    return nuevo_dict_caracteristicas_procesadas

#Funcion para retornar el string de la prediccion obtenida
def obtenerStrPrediccion(prediccion):
    if prediccion == 0:
        return 'Riesgo muy bajo'
    elif prediccion == 1:
        return 'Riesgo bajo'
    elif prediccion == 2:
        return 'Riesgo medio'
    elif prediccion == 3:
        return 'Riesgo alto'
    else:
        return 'Riesgo muy alto'

def crearListaCaracteristicas(dict_caracteristicas):
    lista_caracteristicas = []
    for clave, valor in dict_caracteristicas.items():
        if clave != 'CatRiesgo':
            significado = data_variables.dict_caracteristicas_significado[clave]
            objCaracteristica = caracteristica.Caracteristica(clave, significado, round(valor, 6))
            lista_caracteristicas.append(objCaracteristica.to_dict())
        
    return lista_caracteristicas

#Funcion para convertir el json a diccionario
def dict_a_df(obs, columnas, dtypes):
    obs_df = pd.DataFrame([obs])
    for col, dtype in dtypes.items():
        if col in obs_df.columns:
            obs_df[col] = obs_df[col].astype(dtype)
        else:
            obs_df[col] = None
    
    return obs_df

def select_columns(X, columns):
    return X[columns]