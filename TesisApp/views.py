from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from TesisApp.entities import caracteristica
from TesisApp.entities import variable
from TesisApp.utils import data_variables
from TesisApp.utils import utils
import os
import pandas as pd
import json
import joblib
import lime
import lime.lime_tabular

pathArchivos = os.path.join(os.getcwd(), 'archivos')

pathDFData = os.path.join(pathArchivos, 'consumidores_df.pkl')

pathCSV = os.path.join(pathArchivos, 'df_consumo_varObjetivo.csv')
#pathJsonColumnas = os.path.join(pathArchivos, 'columnas_ames.json')
pathJsonColumnas = os.path.join(pathArchivos, 'columnas_consumidores.json')
#pathPipeline = os.path.join(pathArchivos, 'pipeline_ames.pkl')
pathPipeline = os.path.join(pathArchivos, 'pipeline_rl_best.pkl')
#pathDtypes = os.path.join(pathArchivos, 'dtypes_ames.pkl')
pathDtypes = os.path.join(pathArchivos, 'dtypes_consumidores.pkl')

@api_view(['GET'])
def lista_variables(request):
    if request.method == 'GET':
        print(len(data_variables.diccionario_variables['variables']))
        print(len(data_variables.diccionario_variables_significado['variables']))
        return JsonResponse(data_variables.diccionario_variables_significado, safe=False)
    
@api_view(['GET'])
def lista_variables_significado(request):
    if request.method == 'GET':
        lista_variables = []
        for clave, valor in data_variables.dict_caracteristicas_significado.items():
            if clave != 'CatRiesgo':
                significado = data_variables.dict_caracteristicas_significado[clave]
                objCaracteristica = variable.Variable(clave, significado)
                lista_variables.append(objCaracteristica.to_dict())
        auxDict = {'variables':lista_variables}
        return JsonResponse(auxDict, safe=False)

@api_view(['GET'])
def lista_conteo_riesgo_edad(request):
    data = joblib.load(pathDFData)
    if request.method == 'GET':
        tabla_contingencia = pd.crosstab(data['per_edad_tipo'], data['CatRiesgo'])

        dict_per_edad_tipo = tabla_contingencia.to_dict()

        # Mapear los nombres de la edad según el diccionario
        diccionario = {data_variables.diccionario_per_edad_tipo.get(clave, clave): valor for clave, valor in dict_per_edad_tipo.items()}
        diccionario = {data_variables.diccionario_riesgo[int(clave)]: valor for clave, valor in diccionario.items()}
        return JsonResponse(diccionario, safe=False)

@api_view(['GET'])
def lista_conteo_riesgo_situacion_actual(request):
    data = joblib.load(pathDFData)
    if request.method == 'GET':

        tabla_contingencia = pd.crosstab(data['situacion_tipo'], data['CatRiesgo'])

        dict_situacion_tipo = tabla_contingencia.to_dict()

        # Mapear los nombres de los niveles educativos según el diccionario
        diccionario = {data_variables.diccionario_situacion_tipo.get(clave, clave): valor for clave, valor in dict_situacion_tipo.items()}
        diccionario = {data_variables.diccionario_riesgo[int(clave)]: valor for clave, valor in diccionario.items()}
        return JsonResponse(diccionario, safe=False)


@api_view(['GET'])
def lista_conteo_riesgo_per_sexo_tipo(request):
    data = joblib.load(pathDFData)
    if request.method == 'GET':

        tabla_contingencia = pd.crosstab(data['per_sexo_tipo'], data['CatRiesgo'])

        dict_sexo_riesgo = tabla_contingencia.to_dict()

        # Mapear los nombres de los niveles educativos según el diccionario
        diccionario = {data_variables.diccionario_per_sexo_tipo.get(clave, clave): valor for clave, valor in dict_sexo_riesgo.items()}
        diccionario = {data_variables.diccionario_riesgo[int(clave)]: valor for clave, valor in diccionario.items()}

        return JsonResponse(diccionario, safe=False)

#conteo de cada valor en la columna 'frecuencia_consumo' para cada nivel educativo. se utiliza función crosstab de pandas, que crea una tabla de contingencia.
@api_view(['GET'])
def lista_conteo_nivel_edu_marihuana(request):

    filtro1_param = request.query_params.get('filtro1_param') 
    filtro2_param = request.query_params.get('filtro2_param')
    data = joblib.load(pathDFData)
    if request.method == 'GET':

        tabla_contingencia = pd.crosstab(data[filtro1_param], data[filtro2_param])

        dict_nivel_edu = tabla_contingencia.to_dict()

        return JsonResponse(dict_nivel_edu, safe=False)

@api_view(['GET'])
def lista_conteo_depto_v2(request):
    
    filtro_param = request.query_params.get('filtro_param')
    data = joblib.load(pathDFData)
    if request.method == 'GET':
        data_depto = data[filtro_param].value_counts()

        print(len(data_depto))
        # Se obtenie los 10 principales elementos
        if len(data_depto) > 9:
            principales_deptos = data_depto.head(10)
            otros_deptos = data_depto.iloc[10:]
        else:
            principales_deptos = data_depto
            
        dict_depto = principales_deptos.to_dict()

        return JsonResponse(dict_depto, safe=False)


# Create your views here.
@api_view(['GET'])
def lista_registros(request):
    data = joblib.load(pathDFData)
    if request.method == 'GET':
        consumidoresDict = data.to_dict('records')
        return JsonResponse(consumidoresDict, safe=False)
    

@api_view(['GET'])
def lista_departamentos(request):
    if request.method == 'GET':
        return JsonResponse(data_variables.diccionario_deptos, safe=False)
    

#Funcion para obtener los departamentos por el nivel de riesgo
@api_view(['GET'])
def lista_conteo_depto(request):
    
    filtro_param = request.query_params.get('value')
    data = joblib.load(pathDFData)
    if request.method == 'GET':
        num_filtro = utils.get_tipo_riesgo(filtro_param)
        data_inicial = data['departamento'].value_counts()
        dict_data_inicial = data_inicial.to_dict()       
        
        conteo_data = data[data['CatRiesgo'] == num_filtro]['departamento'].value_counts()
        dict_data = conteo_data.to_dict()
                
        aux_dict_data = {}
        for clave_data_filtrada in dict_data:
            for clave_data_inicial in dict_data_inicial:
                if clave_data_filtrada == clave_data_inicial:
                    porcentaje = (dict_data[clave_data_filtrada] * 100)/dict_data_inicial[clave_data_inicial]
                    aux_dict_data[clave_data_filtrada] = round(porcentaje, 2)
                    break

        nuevo_diccionario = {data_variables.diccionario_deptos[clave]: valor for clave, valor in aux_dict_data.items()}
        
        return JsonResponse(nuevo_diccionario, safe=False)

#Funcion para obtener el conteo por niveles de riesgo para cada Departamento
@api_view(['GET'])
def conteo_riesgo(request):
    filtro_depto = request.query_params.get('value')
    data = joblib.load(pathDFData)
    if request.method == 'GET':
        conteo_data_riesgo = data['CatRiesgo'].value_counts()
        if filtro_depto != 'todos':
            conteo_data_riesgo = data[data['departamento'] == filtro_depto]['CatRiesgo'].value_counts()
        dict_data_riesgo = conteo_data_riesgo.to_dict()
        nuevo_diccionario_riesgo = {data_variables.diccionario_riesgo[clave]: valor for clave, valor in dict_data_riesgo.items()}
        return JsonResponse(nuevo_diccionario_riesgo, safe=False)
  
@api_view(['POST'])   
def predecir(request):
    try:
        print("entro a predecir______")
        with open(pathJsonColumnas) as fname:
            pipeline_columnas = json.load(fname)
        print("Cargo jsonColumnas______")
        pipeline = joblib.load(pathPipeline)
        print("Cargo Pipeline______")
        pipeline_dtypes = joblib.load(pathDtypes)
        print("Cargo tipos de datos______")
        data = joblib.load(pathDFData)
        print("Cargo data______")
        print("Se obtuvo los arvhicos para predecir____________")
        
        if request.method =='POST':
            respuesta = {}
            
                
            data_formulario = JSONParser().parse(request)
            #Para predecir y obtener la importancia de las caracteristicas para la nueva prediccion
            
            #Se obtiene el estimador y el procesador de los datos
            estimador_pipeline = pipeline.named_steps['estimador']
            procesador_pipeline = pipeline.named_steps['procesador']
            
            #La data que llega del front se convierte en diccionario
            obs_df = utils.dict_a_df(data_formulario, pipeline_columnas, pipeline_dtypes)
            
            #Se transforma o procesa la data y se realiza la prediccion
            nueva_data_transformada = procesador_pipeline.transform(obs_df)
            prediccion_nueva = estimador_pipeline.predict(nueva_data_transformada)
            prediccion = int(str(prediccion_nueva[0]))
            
            print("Obtuvo el nueva data con prediccion::::::::::::::::::::::::::")
            
            #Se obtiene el nombre las caracteristicas
            nombres_caracteristicas_procesadas = []

            for nombre, transformador in procesador_pipeline.transformer_list:
                if hasattr(transformador, 'get_feature_names_out'):
                    nombres_generados = transformador.get_feature_names_out()
                    nombres_caracteristicas_procesadas.extend(nombres_generados)
                else:
                    nombres_caracteristicas_procesadas.append(nombre)
            
            num_features = len(nombres_caracteristicas_procesadas)
            explainer = lime.lime_tabular.LimeTabularExplainer(
                training_data=procesador_pipeline.transform(data),
                feature_names=nombres_caracteristicas_procesadas,
                class_names=[0, 1, 2, 3, 4],
                mode='classification'
            )
            
            exp = explainer.explain_instance(
                data_row=nueva_data_transformada[0],
                predict_fn=estimador_pipeline.predict_proba,
                num_features=num_features
            )
            
            lista_importancia_caracteristicas = exp.as_list()
            
            lista_caracteristicas = []
            lista_val_caracteristicas = []
            for feature, importance in lista_importancia_caracteristicas:
                partes = feature.split(' ')
                if partes[0].startswith('transformador'):
                    lista_caracteristicas.append(partes[0])
                elif partes[1].startswith('transformador'):
                    lista_caracteristicas.append(partes[1])
                elif partes[2].startswith('transformador'):
                    lista_caracteristicas.append(partes[2])
                lista_val_caracteristicas.append(importance)
            
            resultados = []

            # Iterar sobre cada elemento del arreglo original
            for elemento in lista_caracteristicas:
                # Dividir la cadena por el caracter '_' y seleccionar la última parte
                partes = elemento.split('__')
                ultima_parte = partes[-1]
                
                # Agregar la última parte al nuevo arreglo
                resultados.append(ultima_parte)
            
            
            # #Se une los nombres de las caracteristicas con los datos obtenidos por la libreria sha
            # importancia_caracteristicas_dict = dict(zip(nombres_caracteristicas_procesadas, valores_shap[0][0]))
            importancia_caracteristicas_dict = dict(zip(resultados, lista_val_caracteristicas))
            
            # #Se usa para unir las caracteristicas que tienen un nombre similar 
            dict_procesado = utils.obtenerDictProcesado(pipeline_columnas, importancia_caracteristicas_dict)
            print(dict_procesado)
            # #El diccionario obtenido se orrdena de forma descendente
            dict_ordenado = dict(sorted(dict_procesado.items(), key=lambda item: item[1], reverse=True))
            # #Se obtiene las 10 caracteristicas que tuvieron mayor impacto
            dict_10_caracteristicas = dict(list(dict_ordenado.items())[:5])

            #Obtener sumatoria de la importancia de las caracteristicas
            total = utils.obtener_total_importancia(dict_ordenado)
            
            # #Se obtiene La lista 
            lista_caracteristicas = utils.crearListaCaracteristicas(dict_10_caracteristicas, total)
            
            # #Se convierte la prediccion a string
            # prediccion = int(str(prediccion_nueva[0]))
            str_prediccion = utils.obtenerStrPrediccion(prediccion)
            # print("Se obtuvo informacion de la prediccion y caracteristicas____________")
            # #Se guarda el nuevo registro
            
            guardarNuevoRegistro(prediccion, obs_df)
            print("Se guardo el nuevo registro____________")
            
            #Se crea la respuesta y se retorna
            #respuesta['prediccion'] = {'prediccion': str_prediccion,'significado':data_variables.dict_prediccion_significado[prediccion], 'caracteristicas':lista_caracteristicas}
            respuesta['prediccion'] = str_prediccion
            respuesta['significado'] = data_variables.dict_prediccion_significado[prediccion]
            respuesta['caracteristicas'] = lista_caracteristicas
            #respuesta['success'] = True
            #respuesta['message'] = "Termino"
            
            return JsonResponse(respuesta)
    except Exception as e:
        print("¡Error! Ocurrió una excepción:", e)
        


def guardarNuevoRegistro(prediccion, obs_df):
    data = joblib.load(pathDFData)
    obs_df['CatRiesgo'] = prediccion
    obs_df = obs_df.reindex(columns=data.columns)
    data = pd.concat([data, obs_df], ignore_index=True)
    joblib.dump(data, pathDFData)
