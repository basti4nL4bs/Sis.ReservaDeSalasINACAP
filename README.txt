# Sistema de Reserva de Salas INACAP

Sistema web para la gestión y reserva de salas y laboratorios desarrollado con Django, siguiendo el flujo y arquitectura del tutorial oficial.

======================================================================
REQUISITOS
======================================================================
* Python 3.10+
* Pip
* Entorno virtual (venv)

======================================================================
INSTALACIÓN Y CONFIGURACIÓN
======================================================================
1. Clonar el repositorio:
   git clone https://github.com/basti4nL4bs/Sis.ReservaDeSalasINACAP.git
   cd Sis.ReservaDeSalasINACAP

2. Crear y activar el entorno virtual:
   - En Windows:
     python -m venv env
     env\Scripts\activate
   - En Linux/Mac:
     python3 -m venv env
     source env/bin/activate

3. Instalar Django:
   pip install django

4. Aplicar migraciones:
   python manage.py makemigrations
   python manage.py migrate

5. Crear usuario administrador:
   python manage.py createsuperuser

6. Iniciar el servidor de desarrollo:
   python manage.py runserver

Acceso al sitio: http://127.0.0.1:8000/
Panel de administración: http://127.0.0.1:8000/admin/

======================================================================
ESTRUCTURA DEL PROYECTO
======================================================================
|-- inacapreservas/       # Configuración principal del proyecto
|   |-- asgi.py
|   |-- settings.py       # Configuración global, BD y apps
|   |-- urls.py           # Enrutador principal
|   |-- wsgi.py
|-- salas/                # Aplicación de gestión de reservas
|   |-- migrations/       # Archivos de esquema de BD
|   |-- static/salas/     # Archivos CSS / estáticos
|   |-- templates/salas/  # Plantillas HTML (index, detail, results)
|   |-- admin.py          # Registro en el panel administrativo
|   |-- apps.py           # Metadatos de la app
|   |-- models.py         # Modelos Sala y Reserva con validación
|   |-- tests.py          # Pruebas unitarias
|   |-- urls.py           # Rutas de la app
|   |-- views.py          # Lógica de negocio (index, detail, reservar, results)
|-- db.sqlite3            # Base de datos local
|-- manage.py             # Utilidad de comandos de Django

======================================================================
FUNCIONALIDADES DEL BACKEND
======================================================================
* Catálogo de Salas: Registro de salas (laboratorios, teóricas, auditorios) con control de capacidad y estado activo.
* Control de Reservas: Agendamiento por fecha y bloque horario asociado a usuarios del sistema.
* Validaciones Integradas:
  - La hora de fin debe ser posterior a la de inicio.
  - Detección y bloqueo automático de reservas solapadas en la misma sala.
* Panel de Administración: Gestión completa de modelos con filtros por fecha, tipo de sala y estado.

======================================================================
EJECUCIÓN DE PRUEBAS
======================================================================
Para correr los tests unitarios automatizados:
python manage.py test


Para el Front-End se utilizo ia para agilizar el proceso de programacion. El siguiente prompt se le entrego a gemini flash 3.8 para la
creacion del Front-End: 

Actúa como un desarrollador web frontend profesional y crea el diseño visual completo para una aplicación web de Django llamada "Sistema de Reserva de Salas INACAP".

El proyecto ya tiene todo su backend programado siguiendo la lógica del tutorial oficial de Django, por lo que necesito que generes el código exacto de cuatro archivos: index.html, detail.html, results.html y style.css.

El estilo visual debe ser minimalista, limpio y moderno. Utiliza una paleta de colores actual basada en fondos claros o neutros, tipografía sans-serif legible, bordes redondeados sutiles, sombras suaves y un color de acento sobrio para botones y estados activos.

Para cada archivo, asegúrate de cumplir con los siguientes puntos:

style.css: Debe contener estilos modulares y reutilizables para toda la app, incluyendo reset básico, variables CSS para la paleta de colores, diseño responsivo con flexbox o grid, clases para formularios, botones, tarjetas de información, badges de estado y mensajes de alerta.

index.html: Es la vista principal. Debe mostrar un listado ordenado en tarjetas de todas las salas disponibles, indicando su nombre, tipo, capacidad y un botón directo para ver detalle y agendar.

detail.html: Es la ficha de la sala seleccionada. Debe mostrar los datos del espacio y contener el formulario POST que envía la reserva a la vista correspondiente, incluyendo token CSRF y los campos de fecha, hora de inicio, hora de fin y motivo, además de listar las reservas ya programadas.

results.html: Es la pantalla de confirmación y resultados. Debe mostrar un mensaje de éxito tras agendar, el resumen de la reserva efectuada y el historial de reservas activas de dicha sala, con un enlace para volver a la lista principal.

Entrega únicamente el código completo, funcional y listo para copiar y pegar en sus respectivas carpetas dentro de la estructura estática y de plantillas de Django, sin omitir partes ni dejar bloques a medias.