# AI_Proyect

SISTEMA FINANCIERO PARA STARTUP DE PRODUCTOS DE LIMPIEZA AL POR MAYOR

1. DESCRIPCIÓN DEL PROYECTO
Este proyecto es un sistema de gestión financiera para una startup que vende productos de limpieza para casas al por mayor. Su objetivo es ayudar a controlar inventario, ventas, compras, gastos operativos, clientes y resumen financiero en un entorno simple y visual.

La aplicación permite registrar operaciones diarias, supervisar la rentabilidad de la empresa y exportar los datos a una planilla de Excel para su análisis o entrega.

2. OBJETIVOS
- Gestionar inventario de productos de limpieza.
- Controlar ventas y compras.
- Registrar clientes y límites de crédito.
- Llevar un control de gastos operativos.
- Revisar indicadores financieros básicos.
- Exportar reportes en formato Excel.
- Tener una interfaz web local para uso práctico.

3. FUNCIONALIDADES PRINCIPALES
- Registro de productos con código, nombre, categoría, costo, precio y stock.
- Registro de clientes con nombre, segmento y contacto.
- Registro de compras de insumos y productos.
- Registro de ventas con tipo de pago (contado o crédito).
- Control de stock disponible y análisis de mínimos.
- Registro de gastos operativos.
- Resumen financiero con ventas, utilidad bruta, utilidad neta y margen.
- Visualización de tablas con datos en la interfaz web.
- Exportación de la información a un archivo Excel (.xlsx).

4. TECNOLOGÍAS USADAS
- Python
- LocalHost
- Conexión con GitHub
4.1. LIBRERÍAS
- Flask
- Pandas
- OpenPyXL

5. REQUISITOS DEL SISTEMA
- Python 3.10 o superior
- Sistema operativo Windows, Linux o macOS
- Conexión local para acceder a la interfaz web

6. INSTALACIÓN
1. Abre una terminal en la carpeta del proyecto.
2. Crea un entorno virtual (opcional pero recomendado):
   python -m venv .venv
3. Activa el entorno virtual(terminal):
   - Windows:
     .\.venv\Scripts\activate
   - Linux/macOS:
     source .venv/bin/activate
4. Instala las dependencias:
   pip install flask pandas openpyxl

7. EJECUCIÓN
Para iniciar la aplicación, ejecuta el siguiente comando desde la carpeta del proyecto:

python recommendation_system.py

Luego abre en un entorno web o navegador:

http://127.0.0.1:5000

8. USO DE LA APLICACIÓN
Una vez abierta la interfaz, podrás:
- Agregar nuevos productos.
- Registrar clientes y sus límites de crédito.
- Ingresar ventas y compras.
- Registrar gastos del negocio.
- Revisar los indicadores financieros en tiempo real.
- Descargar la planilla Excel con todos los datos.

9. ESTRUCTURA DEL PROYECTO
AI_Proyect/
├── README.txt
├── recommendation_system.py
├── planilla_financiera.xlsx   (generado al exportar)
├── reporte_financiero.csv     (si se usa exportación CSV)
├── reporte_financiero.json    (si se usa exportación JSON)
└── .venv/                     (entorno virtual, si existe)

10. EXPORTACIÓN DE EXCEL
La aplicación incluye una opción para exportar la información financiera a una hoja de cálculo Excel llamada:

planilla_financiera.xlsx

Este archivo contiene varias hojas con información organizada por:
- Resumen
- Productos
- Clientes
- Ventas
- Compras
- Gastos

11. CONSIDERACIONES DE NEGOCIO
Este sistema está pensado para una empresa que opera al por mayor, por lo que es útil para:
- gestionar grandes volúmenes de stock,
- controlar ventas por cliente,
- tener un seguimiento de costos,
- analizar rentabilidad del negocio,
- y facilitar decisiones financieras internas.

12. LIMITACIONES
Es una versión funcional de gestión financiera y administrativa. No reemplaza un ERP completo ni un sistema con autenticación de usuarios, base de datos profesional o multiples sucursales.

13. FUTURAS MEJORAS
- Agregar autenticación de usuarios.
- Guardar información en SQLite o MySQL.
- Generar gráficos de ventas y margen.
- Añadir dashboard con métricas avanzadas.
- Crear módulo de nómina y proveedores.
- Integrar exportación PDF.

14. AUTOR / RESPONSABLE
Proyecto desarrollado como ejemplo de gestión financiera para una startup de productos de limpieza al por mayor.

15. CONTACTO
Ingrese aquí el nombre del desarrollador o el correo para consultas adicionales.

16. LICENCIA
Este proyecto puede ser usado con fines educativos o de demostración. Si se desea distribuirlo de manera pública, es recomendable añadir una licencia apropiada, como MIT o Apache 2.0.

17. RESUMEN CORTO
Sistema de gestión financiera para una startup de limpieza al por mayor, creado en Python con Flask y pandas. Permite controlar inventario, ventas, compras, gastos, clientes y exportar datos a Excel para análisis y toma de decisiones.
