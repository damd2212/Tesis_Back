# Back-tesis

#### Para instalar virtualenv desde el cmd
```bash
pip install virtualenv
```

#### Una vez descargado el paquete para entornos virtuales, dentro de la carpeta principal del proyecto se realiza lo siguiente

#### Paso 1: Crear el entorno virtual con el siguiente comando:
```bash
python -m venv env
```

#### Paso 2: Acivar el entorno virtual creado con el siguiente comando
```bash
env/Scripts/activate
```

#### Paso 3: Instalar los paquetes para el correcto funcionamiento de la app
```bash
pip install -r .\requirements.txt
```

#### Paso 4: Verificar el listado de los paquetes instalados
```bash
pip list
```


#### Paso 5: Aarrancar el proyecto con los siguientes comando
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### Para desactivar el entorno virtual
```bash
desactivate
```