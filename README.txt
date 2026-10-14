# Sistema de Reserva de Salas INACAP - Web & API RESTful

Sistema web y servicio API RESTful para la gestión y reserva de salas y laboratorios desarrollado con Django y Django REST Framework (DRF)[cite: 6]. Esta solución evoluciona la arquitectura original hacia una plataforma integral con persistencia relacional, ciclo CRUD web, panel administrativo extendido, control estricto de sesiones y exposición de recursos mediante endpoints seguros en formato JSON[cite: 6, 8].

======================================================================
HISTORIAL DE VERSIONES
======================================================================
* v1.0: Arquitectura base basada en el tutorial oficial de Django (MVT), modelos Sala y Reserva, vistas básicas (index, detail, results), validación anti-solapamiento y estilos minimalistas.
* v2.0: Implementación de ciclo CRUD completo (Create, Read, Update, Delete), validación desacoplada con ModelForm, autenticación nativa y gestión de sesiones seguras (@login_required, expiración de cookies), Django Admin con acciones por lotes (bulk actions) y campos calculados, y nuevas plantillas frontend[cite: 8].
* v3.0 (Actual): Implementación de API RESTful con Django REST Framework (DRF)[cite: 6]. Incorporación de endpoints para recursos 'Sala' y 'Reserva', serializadores con validación de reglas de negocio, autenticación desacoplada por Token (TokenAuthentication), permisos por roles y propiedad de objetos (IsOwnerOrAdmin), respuestas consistentes en JSON con códigos de estado HTTP semánticos y suite de pruebas unitarias automatizadas para la API[cite: 6, 7, 8].

======================================================================
REQUISITOS
======================================================================
* Python 3.10+
* Pip
* Entorno virtual (.venv o env)
* Django >= 5.0
* djangorestframework[cite: 6]

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

3. Instalar dependencias del sistema y de la API:
   python -m pip install django djangorestframework

4. Aplicar migraciones del ORM (incluye tablas de Token de DRF):
   python manage.py makemigrations salas
   python manage.py migrate

5. Crear usuario administrador (Superusuario):
   python manage.py createsuperuser

6. Iniciar el servidor de desarrollo:
   python manage.py runserver

Puntos de acceso del sistema:
- Catálogo general de salas (Web): http://127.0.0.1:8000/
- Panel personal (Mis Reservas Web): http://127.0.0.1:8000/mis-reservas/
- Inicio de sesión (Login Web): http://127.0.0.1:8000/cuentas/login/
- Panel administrativo (Admin): http://127.0.0.1:8000/admin/
- API Raíz / Browsable API (DRF): http://127.0.0.1:8000/salas/api/[cite: 6]
- Endpoint obtención de Token: http://127.0.0.1:8000/salas/api/token/[cite: 6, 8]

======================================================================
ESTRUCTURA DEL PROYECTO (ACTUALIZADA V3.0)
======================================================================
|-- inacapReservas/        # Configuración principal del proyecto
|   |-- asgi.py
|   |-- settings.py        # Configuración global, BD, sesiones y DRF[cite: 6, 8]
|   |-- urls.py            # Enrutador principal y autenticación auth.urls
|   |-- wsgi.py
|-- salas/                 # Aplicación de gestión y API RESTful[cite: 6]
|   |-- migrations/        # Esquemas y migraciones del ORM
|   |-- static/salas/      # Archivos CSS y diseño responsivo
|   |   |-- style.css
|   |-- templates/         # Plantillas HTML estructuradas
|   |   |-- registration/  # Vistas de autenticación web
|   |   |   |-- login.html
|   |   |-- salas/         # Vistas frontend de la aplicación
|   |   |   |-- confirmar_eliminar.html
|   |   |   |-- detail.html
|   |   |   |-- form_reserva.html
|   |   |   |-- index.html
|   |   |   |-- mis_reservas.html
|   |   |   |-- results.html
|   |-- admin.py           # Django Admin extendido con acciones masivas[cite: 8]
|   |-- api_views.py       # Controladores ViewSet para la API RESTful[cite: 6, 7]
|   |-- apps.py            # Metadatos de la aplicación
|   |-- forms.py           # Formularios ModelForm y validación web
|   |-- models.py          # Modelos Sala y Reserva con lógica de persistencia
|   |-- permissions.py     # Clases de permisos granulares y seguridad API[cite: 7, 8]
|   |-- serializers.py     # Serializadores JSON y validación de reglas de negocio[cite: 6, 7]
|   |-- tests.py           # Pruebas automatizadas de endpoints y seguridad[cite: 8]
|   |-- urls.py            # Rutas web y registro de DefaultRouter de la API[cite: 6]
|   |-- views.py           # Controladores CRUD web y control de sesiones[cite: 8]
|-- db.sqlite3             # Base de datos relacional SQLite
|-- manage.py              # CLI de administración de Django
|-- README.txt             # Documentación técnica del proyecto[cite: 8]

======================================================================
FUNCIONALIDADES DEL BACKEND (V2.0 - WEB & PERSISTENCIA)
======================================================================
* Operaciones CRUD Completas:
  - Create: Agendamiento de reservas vinculado automáticamente al usuario en sesión[cite: 8].
  - Read: Visualización pública de salas, disponibilidad por espacio y panel privado "Mis Reservas"[cite: 8].
  - Update: Edición de reservas existentes protegida por sesión (solo el dueño o staff pueden modificar)[cite: 8].
  - Delete: Eliminación o cancelación de reservas con pantalla intermedia de confirmación[cite: 8].

* Gestión de Sesiones y Seguridad Web:
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
FUNCIONALIDADES DE LA API RESTFUL (V3.0 - UNIDAD 3)
======================================================================
* Especificación y Endpoints RESTful[cite: 6, 7, 8]:
  1. Autenticación y Emisión de Token:
     - POST /salas/api/token/
       Solicitud (JSON): {"username": "usuario", "password": "password"}
       Respuesta (200 OK): {"token": "...", "user_id": 1, "username": "usuario", "is_staff": false}[cite: 7]
  
  2. Recurso Salas (/salas/api/salas/)[cite: 7, 8]:
     - GET    /salas/api/salas/         -> Lista pública de salas activas (200 OK)[cite: 7]
     - POST   /salas/api/salas/         -> Crear sala (Restringido a Staff) (201 Created)[cite: 7]
     - GET    /salas/api/salas/{id}/     -> Detalle individual de sala (200 OK)[cite: 7]
     - PUT    /salas/api/salas/{id}/     -> Actualización total (Solo Staff) (200 OK)[cite: 7]
     - PATCH  /salas/api/salas/{id}/     -> Edición parcial (Solo Staff) (200 OK)[cite: 7]
     - DELETE /salas/api/salas/{id}/     -> Eliminar sala (Solo Staff) (204 No Content)[cite: 7]

  3. Recurso Reservas (/salas/api/reservas/)[cite: 7, 8]:
     (Requiere cabecera HTTP: 'Authorization: Token <token_key>')[cite: 6, 7]
     - GET    /salas/api/reservas/      -> Lista privada de reservas del usuario (200 OK)[cite: 7]
     - POST   /salas/api/reservas/      -> Crear reserva validando colisiones (201 Created)[cite: 7]
     - GET    /salas/api/reservas/{id}/  -> Detalle si es dueño o staff (200 OK / 404 Not Found)[cite: 7]
     - PUT    /salas/api/reservas/{id}/  -> Modificación total de reserva propia (200 OK)[cite: 7]
     - PATCH  /salas/api/reservas/{id}/  -> Edición parcial de reserva propia (200 OK)[cite: 7]
     - DELETE /salas/api/reservas/{id}/  -> Cancelación de reserva propia (204 No Content)[cite: 7]

* Mecanismos de Seguridad y Autenticación en la API[cite: 6, 7, 8]:
  - TokenAuthentication: Permite consumo seguro por clientes externos y aplicaciones móviles sin exponer credenciales recurrentemente sobre la red[cite: 6, 7].
  - Control de Acceso por Objeto (IsOwnerOrAdmin): Previene la vulnerabilidad de acceso directo a objetos (BOLA / IDOR). Cada usuario regular solo puede consultar, editar o borrar sus propios registros[cite: 7].
  - Validación en Serializadores (ReservaSerializer): Comprobación estricta de coherencia horaria y bloqueo preventivo de reservas solapadas en la misma sala y fecha, retornando error semántico 400 Bad Request en JSON[cite: 7].

======================================================================
EJECUCIÓN DE PRUEBAS AUTOMATIZADAS
======================================================================
Para ejecutar la suite completa de pruebas unitarias y de integración que validan modelos, reglas de negocio, endpoints y seguridad[cite: 8]:
python manage.py test

Pruebas cubiertas en la API:
1. Listado público de salas sin autenticación (200 OK)[cite: 7].
2. Obtención exitosa de Token mediante credenciales válidas (200 OK)[cite: 7].
3. Bloqueo de creación de reservas sin autenticación (401 Unauthorized)[cite: 7].
4. Creación exitosa de reservas vinculando al usuario del Token (201 Created)[cite: 7].
5. Rechazo inmediato ante intentos de solapamiento de horarios (400 Bad Request)[cite: 7].
6. Aislamiento estricto de datos: usuarios no pueden acceder a reservas ajenas (404 Not Found)[cite: 7].

======================================================================
PROMPTS DE IA UTILIZADOS PARA EL DESARROLLO
======================================================================

Los siguientes prompts se le enviaron a modelos de IA para agilizar y optimizar las distintas etapas del desarrollo[cite: 6, 8]:

--- PROMPT FASE 1 (Plantillas Base y Estilos Generales - Frontend): ---
Actúa como un desarrollador web frontend profesional y crea el diseño visual completo para una aplicación web de Django llamada "Sistema de Reserva de Salas INACAP".

El proyecto ya tiene todo su backend programado siguiendo la lógica del tutorial oficial de Django, por lo que necesito que generes el código exacto de cuatro archivos: index.html, detail.html, results.html y style.css.

El estilo visual debe ser minimalista, limpio y moderno. Utiliza una paleta de colores actual basada en fondos claros o neutros, tipografía sans-serif legible, bordes redondeados sutiles, sombras suaves y un color de acento sobrio para botones y estados activos.

Para cada archivo, asegúrate de cumplir con los siguientes puntos:
- style.css: Debe contener estilos modulares y reutilizables para toda la app, incluyendo reset básico, variables CSS para la paleta de colores, diseño responsivo con flexbox o grid, clases para formularios, botones, tarjetas de información, badges de estado y mensajes de alerta.
- index.html: Vista principal con listado ordenado en tarjetas de todas las salas disponibles, indicando su nombre, tipo, capacidad y un botón directo para ver detalle y agendar.
- detail.html: Ficha de la sala seleccionada que muestra los datos del espacio y el formulario POST para agendar, con token CSRF, campos de fecha, hora inicio, hora fin y motivo, además de listar reservas tomadas.
- results.html: Pantalla de confirmación tras agendar, con resumen de la reserva efectuada y listado de horarios del espacio.

--- PROMPT FASE 2 (Ampliación CRUD, Sesiones y Login - Frontend): ---
Actúa nuevamente como desarrollador frontend para el proyecto "Sistema de Reserva de Salas INACAP", manteniendo exactamente la misma coherencia gráfica, tipografía y paleta de colores definida en style.css.

El sistema ahora incorporó un ciclo CRUD completo y autenticación por sesiones, por lo que necesito que generes las plantillas complementarias faltantes:
1. mis_reservas.html: Panel personal del usuario autenticado donde se listen en una tabla limpia todas las reservas que ha realizado, mostrando sala, fecha, horario, motivo, estado (badge) y dos botones de acción por fila: "Editar" y "Eliminar".
2. form_reserva.html: Formulario reutilizable para crear y editar reservas, adaptado para recibir formularios ModelForm de Django ({{ form.as_p }}), con encabezado dinámico según la acción y botón de guardado.
3. confirmar_eliminar.html: Vista de advertencia y confirmación antes de borrar una reserva definitivamente, mostrando los datos de la reserva afectada y botones para confirmar la baja o cancelar y volver.
4. registration/login.html: Pantalla centrada y responsiva para el inicio de sesión de los usuarios, con manejo visual de credenciales inválidas (form.errors), inputs controlados para usuario y contraseña, y soporte para el parámetro 'next' de redirección.

--- PROMPT FASE 3 (Arquitectura API RESTful y Seguridad - Backend): ---
Actúa como un arquitecto de software backend senior especialista en Django REST Framework[cite: 6].
Diseña una API RESTful profesional para el sistema de reserva de salas que cumpla con los siguientes requerimientos:
1. Configuración de DRF utilizando autenticación por Tokens (TokenAuthentication) y soporte para sesiones de desarrollo[cite: 6].
2. Serializadores para 'Sala' y 'Reserva' que entreguen respuestas JSON consistentes y repliquen las validaciones de negocio del sistema: la hora de término debe ser mayor a la de inicio y no pueden existir solapamientos de horario para la misma sala y fecha[cite: 6, 7].
3. ViewSets y enrutamiento con DefaultRouter aplicando principios RESTful, verbos HTTP correctos (GET, POST, PUT, PATCH, DELETE) y códigos de estado semánticos[cite: 7].
4. Políticas de seguridad y permisos: el catálogo de salas debe ser público en lectura pero restringido a administradores para modificaciones; las reservas deben ser privadas por usuario (un usuario regular solo puede consultar, modificar o cancelar sus propias reservas)[cite: 7].
5. Suite de tests unitarios de integración utilizando APITestCase para verificar los endpoints y el aislamiento de datos[cite: 8].

======================================================================
EVIDENCIA DE USO CRÍTICO Y RESPONSABLE DE INTELIGENCIA ARTIFICIAL (CRITERIO 7)
======================================================================
Durante el desarrollo se contrastaron rigurosamente las recomendaciones proporcionadas por la IA, detectando riesgos y aplicando las siguientes adaptaciones clave[cite: 6, 7]:

1. Detección y Mitigación de Vulnerabilidad BOLA / IDOR (Broken Object Level Authorization):
   - Recomendación inicial de la IA: Proponía un 'ModelViewSet' estándar con 'queryset = Reserva.objects.all()'.
   - Riesgo identificado: Cualquier usuario autenticado con token podía enumerar y consultar reservas de otros usuarios mediante peticiones directas 'GET /salas/api/reservas/{id}/', exponiendo información privada institucional.
   - Modificación aplicada: Se sobrescribió 'get_queryset()' para retornar estrictamente 'Reserva.objects.filter(usuario=self.request.user)' y se implementó la clase de permiso 'IsOwnerOrAdmin', retornando '404 Not Found' ante accesos no autorizados[cite: 7].

2. Prevención de Suplantación de Identidad en Creación de Registros:
   - Recomendación inicial de la IA: Sugería incluir el campo 'usuario' en el cuerpo JSON del POST para reservas.
   - Riesgo identificado: Permitía manipulación del payload para crear reservas a nombre de terceros.
   - Modificación aplicada: Se marcó 'usuario' como 'read_only_fields' en 'ReservaSerializer' y se forzó su asignación en el servidor mediante 'serializer.save(usuario=self.request.user)' dentro del método 'perform_create()'[cite: 7].

3. Resolución de Restricciones del Entorno de Ejecución:
   - Recomendación inicial: Ejecutar comandos directos como 'pip install djangorestframework'.
   - Problema detectado: Bloqueo de binarios por políticas de control de aplicaciones en PowerShell en sistemas Windows.
   - Solución técnica adoptada: Ejecución estructurada a través del intérprete Python ('python -m pip install djangorestframework') asegurando compatibilidad del entorno virtual.