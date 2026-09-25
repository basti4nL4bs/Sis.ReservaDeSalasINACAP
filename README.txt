# Sistema de Reserva de Salas INACAP

Sistema web para la gestión y reserva de salas y laboratorios desarrollado con Django. Esta versión (v2.0) evoluciona la arquitectura inicial hacia un sistema con persistencia relacional completa, operaciones CRUD integrales, personalización avanzada de Django Admin y control estricto de sesiones de usuario[cite: 8].

======================================================================
HISTORIAL DE VERSIONES
======================================================================
* v1.0: Arquitectura base basada en el tutorial oficial de Django (MVT), modelos Sala y Reserva, vistas básicas (index, detail, results), validación anti-solapamiento y estilos minimalistas.
* v2.0 (Actual): Implementación de ciclo CRUD completo (Create, Read, Update, Delete), validación desacoplada con ModelForm, autenticación nativa y gestión de sesiones seguras (@login_required, expiración de cookies), Django Admin con acciones por lotes (bulk actions) y campos calculados, y nuevas plantillas frontend[cite: 8].

======================================================================
REQUISITOS
======================================================================
* Python 3.10+
* Pip
* Entorno virtual (.venv o env)

======================================================================
INSTALACIÓN Y CONFIGURACIÓN
======================================================================
1. Clonar el repositorio:
   git clone https://github.com/basti4nL4bs/Sis.ReservaDeSalasINACAP.git
   cd Sis.ReservaDeSalasINACAP

2. Crear y activar el entorno virtual:
   - En Windows (PowerShell):
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
   - En Linux/Mac:
     python3 -m venv .venv
     source .venv/bin/activate

3. Instalar Django:
   pip install django

4. Aplicar migraciones:
   python manage.py makemigrations salas
   python manage.py migrate

5. Crear usuario administrador:
   python manage.py createsuperuser

6. Iniciar el servidor de desarrollo:
   python manage.py runserver

Puntos de acceso del sistema:
- Catálogo general de salas: http://127.0.0.1:8000/
- Panel personal (Mis Reservas): http://127.0.0.1:8000/mis-reservas/
- Inicio de sesión (Login): http://127.0.0.1:8000/cuentas/login/
- Panel administrativo (Admin): http://127.0.0.1:8000/admin/

======================================================================
ESTRUCTURA DEL PROYECTO (ACTUALIZADA V2.0)
======================================================================
|-- inacapReservas/       # Configuración principal del proyecto
|   |-- asgi.py
|   |-- settings.py       # Configuración global, BD y políticas de sesión[cite: 8]
|   |-- urls.py           # Enrutador principal y rutas de autenticación auth.urls
|   |-- wsgi.py
|-- salas/                # Aplicación de gestión de reservas
|   |-- migrations/       # Esquemas y migraciones del ORM
|   |-- static/salas/     # Archivos CSS y diseño responsivo
|   |   |-- style.css
|   |-- templates/        # Plantillas HTML estructuradas
|   |   |-- registration/ # Vistas de autenticación
|   |   |   |-- login.html
|   |   |-- salas/        # Vistas de la aplicación
|   |   |   |-- confirmar_eliminar.html
|   |   |   |-- detail.html
|   |   |   |-- form_reserva.html
|   |   |   |-- index.html
|   |   |   |-- mis_reservas.html
|   |   |   |-- results.html
|   |-- admin.py          # Django Admin extendido con acciones masivas[cite: 8]
|   |-- apps.py           # Metadatos de la aplicación
|   |-- forms.py          # Formularios ModelForm y validación de bloques
|   |-- models.py         # Modelos Sala y Reserva con lógica de persistencia
|   |-- tests.py          # Pruebas unitarias automatizadas
|   |-- urls.py           # Rutas CRUD de la aplicación
|   |-- views.py          # Controladores CRUD y control de sesiones[cite: 8]
|-- db.sqlite3            # Base de datos relacional SQLite
|-- manage.py             # CLI de administración de Django
|-- README.txt            # Documentación técnica del proyecto

======================================================================
FUNCIONALIDADES DEL BACKEND (EVALUACIÓN 2)
======================================================================
* Operaciones CRUD Completas:
  - Create: Agendamiento de reservas vinculado automáticamente al usuario en sesión[cite: 8].
  - Read: Visualización pública de salas, disponibilidad por espacio y panel privado "Mis Reservas"[cite: 8].
  - Update: Edición de reservas existentes protegida por sesión (solo el dueño o staff pueden modificar)[cite: 8].
  - Delete: Eliminación o cancelación de reservas con pantalla intermedia de confirmación[cite: 8].

* Gestión de Sesiones y Seguridad:
  - Vistas privadas protegidas mediante el decorador @login_required[cite: 8].
  - Prevención de suplantación: validación estricta de propiedad de la reserva antes de editar o eliminar[cite: 8].
  - Políticas de sesión en settings.py: expiración de cookies al cerrar el navegador (SESSION_EXPIRE_AT_BROWSER_CLOSE), tiempo límite por inactividad y flags HTTPOnly[cite: 8].

* Django Admin Avanzado:
  - Acciones personalizadas por lote: marcar múltiples reservas seleccionadas como "Confirmadas" o "Canceladas" en un solo paso[cite: 8].
  - Campos calculados (@admin.display) para visualizar el total histórico de reservas por sala[cite: 8].
  - Filtros jerárquicos por fechas, tipo de espacio y búsqueda por usuario o nombre de sala[cite: 8].

* Persistencia y Validación en Base de Datos:
  - Validación horaria en models.py y forms.py (la hora de fin debe superar a la de inicio).
  - Intercepción y manejo de excepciones ante colisiones de reservas en la misma sala y fecha.

======================================================================
EJECUCIÓN DE PRUEBAS
======================================================================
Para correr los tests unitarios automatizados que validan los modelos y reglas de negocio:
python manage.py test

======================================================================
PROMPTS DE IA UTILIZADOS PARA EL DESARROLLO (FRONTEND)
======================================================================

Los siguientes prompt se le enviaron a gemini pro 3.1 para la agilizar la creacion del frontend:

--- PROMPT FASE 1 (Plantillas Base y Estilos Generales): ---
Actúa como un desarrollador web frontend profesional y crea el diseño visual completo para una aplicación web de Django llamada "Sistema de Reserva de Salas INACAP".

El proyecto ya tiene todo su backend programado siguiendo la lógica del tutorial oficial de Django, por lo que necesito que generes el código exacto de cuatro archivos: index.html, detail.html, results.html y style.css.

El estilo visual debe ser minimalista, limpio y moderno. Utiliza una paleta de colores actual basada en fondos claros o neutros, tipografía sans-serif legible, bordes redondeados sutiles, sombras suaves y un color de acento sobrio para botones y estados activos.

Para cada archivo, asegúrate de cumplir con los siguientes puntos:
- style.css: Debe contener estilos modulares y reutilizables para toda la app, incluyendo reset básico, variables CSS para la paleta de colores, diseño responsivo con flexbox o grid, clases para formularios, botones, tarjetas de información, badges de estado y mensajes de alerta.
- index.html: Vista principal con listado ordenado en tarjetas de todas las salas disponibles, indicando su nombre, tipo, capacidad y un botón directo para ver detalle y agendar.
- detail.html: Ficha de la sala seleccionada que muestra los datos del espacio y el formulario POST para agendar, con token CSRF, campos de fecha, hora inicio, hora fin y motivo, además de listar reservas tomadas.
- results.html: Pantalla de confirmación tras agendar, con resumen de la reserva efectuada y listado de horarios del espacio.

--- PROMPT FASE 2 (Ampliación CRUD, Sesiones y Login): ---
Actúa nuevamente como desarrollador frontend para el proyecto "Sistema de Reserva de Salas INACAP", manteniendo exactamente la misma coherencia gráfica, tipografía y paleta de colores definida en style.css.

El sistema ahora incorporó un ciclo CRUD completo y autenticación por sesiones, por lo que necesito que generes las plantillas complementarias faltantes:
1. mis_reservas.html: Panel personal del usuario autenticado donde se listen en una tabla limpia todas las reservas que ha realizado, mostrando sala, fecha, horario, motivo, estado (badge) y dos botones de acción por fila: "Editar" y "Eliminar".
2. form_reserva.html: Formulario reutilizable para crear y editar reservas, adaptado para recibir formularios ModelForm de Django ({{ form.as_p }}), con encabezado dinámico según la acción y botón de guardado.
3. confirmar_eliminar.html: Vista de advertencia y confirmación antes de borrar una reserva definitivamente, mostrando los datos de la reserva afectada y botones para confirmar la baja o cancelar y volver.
4. registration/login.html: Pantalla centrada y responsiva para el inicio de sesión de los usuarios, con manejo visual de credenciales inválidas (form.errors), inputs controlados para usuario y contraseña, y soporte para el parámetro 'next' de redirección.

Entrega el código íntegro, listo para ser utilizado en el entorno de plantillas de Django.