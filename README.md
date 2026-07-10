<!-- markdownlint-disable MD022 MD041 MD026-->
### Hexlet tests and linter status:
[![Actions Status](https://github.com/Bam-Manu-182/python-project-207/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Bam-Manu-182/python-project-207/actions)

Badge de Codeclimate: [![Maintainability](https://qlty.sh/gh/Bam-Manu-182/projects/python-project-207/maintainability.svg)](https://qlty.sh/gh/Bam-Manu-182/projects/python-project-207)

Analizador de Páginas (Page Analyzer)

¡Bienvenido al Analizador de Páginas! Esta es una aplicación web, completamente funcional orientada al análisis e indexación SEO de sitios web. El sistema permite registrar direcciones URL, normalizarlas para evitar duplicados, guardarlas en un entorno relacional, realizar peticiones HTTP en tiempo real y extraer componentes clave para el posicionamiento web (etiquetas `<h1>`, `<title>` y meta-descripciones).

Diseño y Arquitectura del Sistema

El proyecto sigue una arquitectura basada en el patrón MVC (Modelo-Vista-Controlador) adaptado para micro-frameworks, donde la lógica de enrutamiento y la interacción con la base de datos se manejan de manera directa y transparente.

Procesos Principales del Flujo de Trabajo

1. Registro de URL:
   * El usuario ingresa una dirección en la interfaz principal.
   * El sistema valida la estructura de la URL mediante expresiones regulares y validadores nativos.
   * Se ejecuta un proceso de normalización: se extraen únicamente el esquema (`scheme`), descartando rutas, parámetros o subcarpetas (ej. `https://sub.ejemplo.com/ruta?id=1` se convierte en `https://sub.ejemplo.com`).
   * Se verifica la existencia del dominio en la base de datos. Si ya existe, se redirige al usuario al perfil del sitio existente alertando la duplicidad. Si es nuevo, se según los requisitos del sistema.

2. Chequeo SEO (Verificación):
   * Al accionar "Iniciar verificación", el servidor realiza una petición `GET` utilizando un cliente HTTP con tiempos de espera (`timeout`) controlados.
   * Si la respuesta es exitosa (`200 OK`), el documento HTML es transferido al motor de parsing.
   * Se extraen los textos contenidos en `<h1>`, `<title>` y `<meta name="description">`.
   * Si alguno de los campos de texto recuperados excede los límites visuales o de base de datos, el sistema aplica un truncamiento controlado por backend para añadir el sufijo de elipsis (`...`) garantizando la integridad de la interfaz de usuario.
   * Se persiste el chequeo con su respectiva marca de tiempo (`created_at`).

Requisitos del Sistema y Entorno
El software ha sido desarrollado y probado bajo las especificaciones para asegurar su portabilidad y correcto funcionamiento en despliegues remotos:

Sistema Operativo Compatible: Windows 10/11 (Entorno de desarrollo local usando PowerShell / VS Code)

Gestor de Dependencias: uv

Variables de Entorno Necesarias (.env):

Fragmento de código
SECRET_KEY=tu_llave_secreta_aqui
DATABASE_URL=postgresql://usuario:password@localhost:5432/nombre_bd

Códigos de Iniciación y Uso Local (uv)
Sigue estos pasos detallados para levantar el proyecto desde cero utilizando el gestor uv:

1 Sincronizar el entorno e instalar dependencias

Ingresar a la carpeta raíz del proyecto
cd python-project-174

Sincronizar e instalar el entorno virtual con uv
uv sync

2 Configurar la base de datos
Crea una base de datos PostgreSQL local, genera tu archivo .env en la raíz del proyecto basándote en la estructura de variables requerida y ejecuta los scripts de inicialización SQL provistos en la sección anterior.

3 Lanzar el Servidor de Desarrollo
Para arrancar la aplicación en modo local utilizando el entorno administrado por uv, ejecuta:

uv run flask --app page_analyzer:app run --debug
El servidor web estará disponible inmediatamente en la dirección: <http://127.0.0.1:5000>

Demostración externa (Demo)

Se puede ver la aplicación funcionando en vivo en el siguiente enlace: <https://python-project-207-32p0.onrender.com>
