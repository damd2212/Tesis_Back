from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import os
import pandas as pd
import json
import joblib
import shap

pathArchivos = os.path.join(os.getcwd(), 'archivos')

pathCSV = os.path.join(pathArchivos, 'df_consumo_varObjetivo.csv')
#pathJsonColumnas = os.path.join(pathArchivos, 'columnas_ames.json')
pathJsonColumnas = os.path.join(pathArchivos, 'columnas_consumidores.json')
#pathPipeline = os.path.join(pathArchivos, 'pipeline_ames.pkl')
pathPipeline = os.path.join(pathArchivos, 'pipeline_rf_best.pkl')
#pathDtypes = os.path.join(pathArchivos, 'dtypes_ames.pkl')
pathDtypes = os.path.join(pathArchivos, 'dtypes_consumidores.pkl')

diccionario_deptos = {'Antioquia': 'Antioquia', 'Cundinamarca': 'Cundinamarca', 'Caldas': 'Caldas', 'Valle': 'Valle del Cauca', 'Bolivar': 'Bolívar', 'Santander': 'Santander', 'Atlantico': 'Atlántico', 'Meta': 'Meta', 'Nariño': 'Nariño', 'Risaralda': 'Risaralda', 'Boyaca': 'Boyacá', 'Tolima': 'Tolima', 'Norte de Santander': 'Norte de Santander', 'Cordoba': 'Córdoba', 'Cesar': 'Cesar', 'Sucre': 'Sucre', 'Guaviare': 'Guaviare', 'Cauca': 'Cauca', 'Magdalena': 'Magdalena', 'Quindio': 'Quindío', 'La Guajira': 'La Guajira', 'Caqueta': 'Caquetá', 'Huila': 'Huila', 'Choco': 'Chocó', 'Casanare': 'Casanare', 'Arauca': 'Arauca', 'Putumayo': 'Putumayo', 'Guainia': 'Guainía', 'Amazonas': 'Amazonas', 'San Andres': 'San Andrés', 'Vichada': 'Vichada', 'Vaupes': 'Vaupés'}
diccionario_riesgo = {0:'Muy bajo', 1:'Bajo', 2:'Medio', 3:'Alto',4:'Muy alto'}
diccionario_nivel_educ = {'d2_05_Media': 'd2_05_Media', 'd2_05_Tecnico/Tecnologo': 'd2_05_Tecnico/Tecnologo', 'd2_05_Universitario': 'd2_05_Universitario', 'd2_05_Basica_secundaria': 'd2_05_Basica_secundaria', 'd2_05_Basica_primaria': 'd2_05_Basica_primaria', 'd2_05_Postgrado': 'd2_05_Postgrado', 'd2_05_Ninguno': 'd2_05_Ninguno', 'd2_05_Preescolar': 'd2_05_Preescolar'}


#conteo de cada valor en la columna 'frecuencia_consumo' para cada nivel educativo. se utiliza función crosstab de pandas, que crea una tabla de contingencia.
@api_view(['GET'])
def lista_conteo_nivel_edu_marihuana(request):

    data = pd.read_csv(pathCSV)

    if request.method == 'GET':

        tabla_contingencia = pd.crosstab(data['d2_05_nivel_educativo_tipo'], data['frecuencia_consumo_marihuana_tipo'])

        dict_nivel_edu = tabla_contingencia.to_dict()

        # Mapear los nombres de los niveles educativos según el diccionario_nivel_educ
        diccionario = {diccionario_nivel_educ.get(clave, clave): valor for clave, valor in dict_nivel_edu.items()}

        return JsonResponse(diccionario, safe=False)

#conteo de cada valor en la columna 'frecuencia_consumo' para cada nivel educativo. se utiliza función crosstab de pandas, que crea una tabla de contingencia.
@api_view(['GET'])
def lista_conteo_nivel_edu_cocaina(request):

    data = pd.read_csv(pathCSV)

    if request.method == 'GET':

        tabla_contingencia = pd.crosstab(data['d2_05_nivel_educativo_tipo'], data['frecuencia_consumo_cocaina_tipo'])

        dict_nivel_edu = tabla_contingencia.to_dict()

        # Mapear los nombres de los niveles educativos según el diccionario_nivel_educ
        diccionario = {diccionario_nivel_educ.get(clave, clave): valor for clave, valor in dict_nivel_edu.items()}

        return JsonResponse(diccionario, safe=False)


#conteo de cada valor en la columna 'frecuencia_consumo' para cada nivel educativo. se utiliza función crosstab de pandas, que crea una tabla de contingencia.
@api_view(['GET'])
def lista_conteo_nivel_edu_bazuco(request):

    data = pd.read_csv(pathCSV)

    if request.method == 'GET':

        tabla_contingencia = pd.crosstab(data['d2_05_nivel_educativo_tipo'], data['frecuencia_consumo_basuco_tipo'])

        dict_nivel_edu = tabla_contingencia.to_dict()

        # Mapear los nombres de los niveles educativos según el diccionario_nivel_educ
        diccionario = {diccionario_nivel_educ.get(clave, clave): valor for clave, valor in dict_nivel_edu.items()}

        return JsonResponse(diccionario, safe=False)

@api_view(['GET'])
def lista_conteo_depto_v2(request):
    
    data = pd.read_csv(pathCSV)

    if request.method == 'GET':
        data_depto = data['departamento'].value_counts()

        # Se obtenie los 7 principales departamentos
        principales_deptos = data_depto.head(10)
        otros_deptos = data_depto.iloc[10:]

        # Suma el conteo de los departamentos restantes y agrega a la categoría "Otros"
        #otros_count = otros_deptos.sum()
        #principales_deptos['Otros'] = otros_count

        dict_depto = principales_deptos.to_dict()
        diccionario = {diccionario_deptos.get(clave, clave): valor for clave, valor in dict_depto.items()}

        return JsonResponse(diccionario, safe=False)


# Create your views here.
@api_view(['GET'])
def lista_registros(request):

    consumidores = pd.read_csv(pathCSV)
    
    if request.method == 'GET':
        consumidoresDict = consumidores.to_dict('records')
        return JsonResponse(consumidoresDict, safe=False)
    

@api_view(['GET'])
def lista_departamentos(request):
    if request.method == 'GET':
        return JsonResponse(diccionario_deptos, safe=False)
    

#Funcion para obtener los departamentos por el nivel de riesgo
@api_view(['GET'])
def lista_conteo_depto(request):
    
    filtro_param = request.query_params.get('value')
    consumidores = pd.read_csv(pathCSV)
    
    if request.method == 'GET':
        num_filtro = get_tipo_riesgo(filtro_param)
        data_inicial = consumidores['departamento'].value_counts()
        dict_data_inicial = data_inicial.to_dict()       
        
        conteo_data = consumidores[consumidores['CatRiesgo'] == num_filtro]['departamento'].value_counts()
        dict_data = conteo_data.to_dict()
                
        aux_dict_data = {}
        for clave_data_filtrada in dict_data:
            for clave_data_inicial in dict_data_inicial:
                if clave_data_filtrada == clave_data_inicial:
                    porcentaje = (dict_data[clave_data_filtrada] * 100)/dict_data_inicial[clave_data_inicial]
                    aux_dict_data[clave_data_filtrada] = round(porcentaje, 2)
                    break

        nuevo_diccionario = {diccionario_deptos[clave]: valor for clave, valor in aux_dict_data.items()}
        
        return JsonResponse(nuevo_diccionario, safe=False)
    
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

#Funcion para obtener el conteo por niveles de riesgo para cada Departamento
@api_view(['GET'])
def conteo_riesgo(request):
    filtro_depto = request.query_params.get('value')
    consumidores = pd.read_csv(pathCSV)
    
    if request.method == 'GET':
        conteo_data_riesgo = consumidores['CatRiesgo'].value_counts()
        if filtro_depto != 'todos':
            conteo_data_riesgo = consumidores[consumidores['departamento'] == filtro_depto]['CatRiesgo'].value_counts()
        dict_data_riesgo = conteo_data_riesgo.to_dict()
        nuevo_diccionario_riesgo = {diccionario_riesgo[clave]: valor for clave, valor in dict_data_riesgo.items()}
        return JsonResponse(nuevo_diccionario_riesgo, safe=False)
  
@api_view(['POST'])   
def predecir(request):
    
    with open(pathJsonColumnas) as fname:
        pipeline_columnas = json.load(fname)
    
    pipeline = joblib.load(pathPipeline)
    pipeline_dtypes = joblib.load(pathDtypes)
    
    if request.method =='POST':
        data_formulario = JSONParser().parse(request)
        
        #Para predecir y obtener la importancia de las caracteristicas para la nueva prediccion
        
        #Se obtiene el estimador y el procesador de los datos
        estimador_pipeline = pipeline.named_steps['estimador']
        procesador_pipeline = pipeline.named_steps['procesador']
        
        #La data que llega del frony se convierte en diccionario
        obs_df = dict_a_df(data_formulario, pipeline_columnas, pipeline_dtypes)
        
        #Se transforma o procesa la data y se realiza la prediccion
        nueva_data_transformada = procesador_pipeline.transform(obs_df)
        prediccion_nueva = estimador_pipeline.predict(nueva_data_transformada)
        
        #Con la libreria shap se obtiene la importancia para las nuevas predicciones que llegan
        explainer = shap.Explainer(estimador_pipeline)
        
        #Se obtiene la informacion de las caracateristicas
        valores_shap = explainer.shap_values(nueva_data_transformada)
        
        #Se obtiene el nombre las caracteristicas
        nombres_caracteristicas_procesadas = []
        for nombre, transformador in procesador_pipeline.transformer_list:
            nombres_caracteristicas_procesadas.extend(transformador.steps[-1][1].get_feature_names_out())
        
        #Se une los nombres de las caracteristicas con los datos obtenidos por la libreria sha
        importancia_caracteristicas_dict = dict(zip(nombres_caracteristicas_procesadas, valores_shap[0][0]))
        
        #Se usa para unir las caracteristicas que tienen un nombre similar 
        dict_procesado = obtenerDictProcesado(pipeline_columnas, importancia_caracteristicas_dict)
        
        #El diccionario obtenido se orrdena de forma descendente
        dict_ordenado = dict(sorted(dict_procesado.items(), key=lambda item: item[1], reverse=True))
        
        #Se obtiene las 10 caracteristicas que tuvieron mayor impacto
        dict_10_caracteristicas = dict(list(dict_ordenado.items())[:10])
        
        #Se convierte la prediccion a string
        prediccion = int(str(prediccion_nueva[0]))
        str_prediccion = obtenerStrPrediccion(prediccion)
        
        #Se crea la respuesta y se retorna
        respuesta = {'prediccion': str_prediccion, 'caracteristicas':dict_10_caracteristicas}
        return JsonResponse(respuesta)

#Funcion para procesar las caracteristicas en su valor inicial
def obtenerDictProcesado(pipeline_columnas,importancia_caracteristicas_dict):
    nuevo_dict_caracteristicas_procesadas = {}
    sumatoria = 0
    promedio = 0
    num_caracteristicas = 0;
    for columna in pipeline_columnas:
        
        if columna == "residentes_hogar":
            nuevo_dict_caracteristicas_procesadas["residentes_hogar"] = importancia_caracteristicas_dict["x0"]
        elif columna == "d2_04_num_hijos":
            nuevo_dict_caracteristicas_procesadas["d2_04_num_hijos"] = importancia_caracteristicas_dict["x1"]
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

#Funcion para convertir el json a diccionario
def dict_a_df(obs, columnas, dtypes):
    obs_df = pd.DataFrame([obs])
    for col, dtype in dtypes.items():
        if col in obs_df.columns:
            obs_df[col] = obs_df[col].astype(dtype)
        else:
            obs_df[col] = None
    
    return obs_df
       

