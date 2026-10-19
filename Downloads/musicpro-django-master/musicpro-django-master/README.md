Proyecto Django de tienda de música con gestión de usuarios, roles y catálogo en JSON
# MusicPro - Sistema de Gestión e Interfaz de Tienda

## Inicialización y Estructura Base
El proyecto y la aplicación en Django se encuentran correctamente inicializados y registrados en `settings.py`, dejando operativo el entorno del caso seleccionado.

### Características del Proyecto
* **Arquitectura:** Framework Django estructurado en capas.
* **Autenticación:** Sistema de usuarios con roles diferenciados (Cliente / Administrador).
* **Persistencia de Datos:** Gestión mediante archivos JSON (`productos.json` y `usuarios.json`).
* **Interfaz:** Diseño responsivo adaptado con Tailwind CSS.

### Instrucciones para Ejecutar el Proyecto
1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/Nachtt06/musicpro-django.git](https://github.com/Nachtt06/musicpro-django.git)

   Comandos:
   python -m venv venv
   cmd: activate
   pip install django
   pip install faker
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
Abrir link y al final del enlace escribir admin y así lograremos entrar al panel del admistrador Django.
Generación de datos de prueba
python manage.py seed_datos --cantidad 100
python manage.py seed_datos --cantidad 1000
python manage.py seed_datos --cantidad 100000
python manage.py seed_datos --cantidad 1000000
Para verificar el conteo a la base de datos:
python manage.py shell
