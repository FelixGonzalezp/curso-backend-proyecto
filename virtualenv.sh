#!/bin/bash

# Nombre del entorno virtual
VENV_NAME=venv

# Comprobar si ya existe un entorno virtual con el mismo nombre
if [ -d "$VENV_NAME" ]; then
    echo "El entorno virtual $VENV_NAME ya existe. Activando..."
    source $VENV_NAME/Scripts/activate
else
    echo "Creando entorno virtual $VENV_NAME..."
    # Crear un entorno virtual con el nombre especificado
    python -m venv $VENV_NAME
    
    # Activar el entorno virtual
    source $VENV_NAME/Scripts/activate
    
    echo "Entorno virtual $VENV_NAME creado y activado correctamente."
fi

# Instalar los paquetes especificados en el archivo requirements.txt
echo "Instalando paquetes desde requirements.txt..."
pip install -r requirements.txt
# cd django_proyecto

if [ ! -f "db.sqlite3" ]; then
    echo "Creando db.sqlite3"
    touch db.sqlite3
fi
python manage.py makemigrations
python manage.py migrate

python manage.py runserver 8000