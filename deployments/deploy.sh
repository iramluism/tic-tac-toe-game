#!/bin/sh
# start.sh

# Ejecutar las migraciones
python manage.py makemigrations
python manage.py migrate

# Iniciar el servidor
exec python manage.py runserver 0.0.0.0:8000