### Hexlet tests and linter status:
[![Actions Status](https://github.com/Bam-Manu-182/python-project-207/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Bam-Manu-182/python-project-207/actions)



Badge de Codeclimate: [![Maintainability](https://qlty.sh/gh/Bam-Manu-182/projects/python-project-207/maintainability.svg)](https://qlty.sh/gh/Bam-Manu-182/projects/python-project-207)



🔍 Analizador de Páginas (Page Analyzer)

¡Bienvenido al **Analizador de Páginas**! Esta es una aplicación web, completamente funcional orientada al análisis e indexación SEO de sitios web. El sistema permite registrar direcciones URL, normalizarlas para evitar duplicados, guardarlas en un entorno relacional, realizar peticiones HTTP en tiempo real y extraer componentes clave para el posicionamiento web (etiquetas `<h1>`, `<title>` y meta-descripciones).

---------------------------------------------------------------------------------------------------

🎨 Diseño y Arquitectura del Sistema

El proyecto sigue una arquitectura basada en el patrón **MVC (Modelo-Vista-Controlador)** adaptado para micro-frameworks, donde la lógica de enrutamiento y la interacción con la base de datos se manejan de manera directa y transparente.


+--------------------------------+
              |      Cliente (Navegador)       |
              +--------------------------------+
                 | 1. POST /urls   ^ 4. Render
                 v                 |    show.html
     +--------------------------------------------+
     |             Flask Application              |
     +--------------------------------------------+
        | 2. Validar/Normalizar     | 3. Query DB
        v                           v
+------------------+       +------------------------+
|  BeautifulSoup4  |       |   PostgreSQL Database  |
| (Parser HTML)    |       | (Tablas: urls, checks) |
+------------------+       +------------------------+


⚡ Procesos Principales del Flujo de Trabajo

1. **Registro de URL:**
   * El usuario ingresa una dirección en la interfaz principal.
   * El sistema valida la estructura de la URL mediante expresiones regulares y validadores nativos.
   * Se ejecuta un proceso de **normalización**: se extraen únicamente el esquema (`scheme`), descartando rutas, parámetros o subcarpetas (ej. `https://sub.ejemplo.com/ruta?id=1` se convierte en `https://sub.ejemplo.com`).
   * Se verifica la existencia del dominio en la base de datos. Si ya existe, se redirige al usuario al perfil del sitio existente alertando la duplicidad. Si es nuevo, se según los requisitos del sistema.

2. **Chequeo SEO (Verificación):**
   * Al accionar "Iniciar verificación", el servidor realiza una petición `GET` utilizando un cliente HTTP con tiempos de espera (`timeout`) controlados.
   * Si la respuesta es exitosa (`200 OK`), el documento HTML es transferido al motor de parsing.
   * Se extraen los textos contenidos en `<h1>`, `<title>` y `<meta name="description">`.
   * Si alguno de los campos de texto recuperados excede los límites visuales o de base de datos, el sistema aplica un truncamiento controlado por backend para añadir el sufijo de elipsis (`...`) garantizando la integridad de la interfaz de usuario.
   * Se persiste el chequeo con su respectiva marca de tiempo (`created_at`).

---------------------------------------------------------------------------------------------------

💻 Tecnologías y Librerías Utilizadas

El ecosistema de la aplicación se compone de tecnologías estables y librerías estándar dentro del desarrollo en Python:

| Componente            | Tecnología / Librería | Versión | Descripción
| :---                  | :---                  | :---    | :---
| **Lenguaje**          | Python                | `^3.10` | Lenguaje principal de desarrollo. |
| **Framework Web**     | Flask                 | `^3.0`  | Micro-framework para la gestión de rutas y renderizado de vistas.
| **Gestor de Entorno** | uv (Astral)           | Ultima  | Administrador de paquetes y entornos virtuales de alta velocidad.
| **Base de Datos**     | PostgreSQL / Psycopg2 | `^2.9`  | Motor relacional y adaptador nativo para operaciones SQL seguras.
| **Cliente HTTP**      | Requests              | `^2.31` | Gestor de peticiones de red para inspeccionar sitios remotos.
| **Parsing HTML**      | Beautiful Soup 4      | `^4.12` | Extractor de datos estructurados desde el árbol DOM de las páginas.
| **Estilos (UI)**      | Bootstrap             | `v5.3`  | Framework CSS para el diseño responsivo de tablas y formularios.
| **Validaciones**      | Validators            | `^0.22` | Validación sintáctica formal de direcciones de red.
| **Configuración**     | Python-Dotenv         | `^1.0`  | Carga de variables de entorno críticas y llaves secretas.

---------------------------------------------------------------------------------------------------

🗄️ Diseño de la Base de Datos

La persistencia de datos está estructurada sobre dos tablas relacionales vinculadas mediante una relación de uno a muchos (`1:N`).


+----------------------------------+
|               urls               |
+----------------------------------+
| id         : SERIAL PRIMARY KEY  |
| name       : VARCHAR(255) UNIQUE |
| created_at : TIMESTAMP           |
+----------------------------------+
                 |
                 | 1
                 |
                 | N
+----------------------------------+
|            url_checks            |
+----------------------------------+
| id          : SERIAL PRIMARY KEY |
| url_id      : INT FOREIGN KEY    |
| status_code : INT                |
| h1          : VARCHAR(255)       |
| title       : VARCHAR(255)       |
| description : TEXT               |
| created_at  : TIMESTAMP          |
+----------------------------------+


✅🕕 Scripts de Inicialización SQL

```sql
-- Creación de la tabla de Sitios Web
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL
);

-- Creación de la tabla de Verificaciones SEO
CREATE TABLE url_checks (
    id SERIAL PRIMARY KEY,
    url_id INT REFERENCES urls(id) ON DELETE CASCADE,
    status_code INT,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP NOT NULL
);

---------------------------------------------------------------------------------------------------

🛠️ Requisitos del Sistema y Entorno
El software ha sido desarrollado y probado bajo las especificaciones para asegurar su portabilidad y correcto funcionamiento en despliegues remotos:

Sistema Operativo Compatible: Windows 10/11 (Entorno de desarrollo local usando PowerShell / VS Code) / Linux (Contenedores de producción).

Gestor de Dependencias: uv

Variables de Entorno Necesarias (.env):

Fragmento de código
SECRET_KEY=tu_llave_secreta_aqui
DATABASE_URL=postgresql://usuario:password@localhost:5432/nombre_bd


---------------------------------------------------------------------------------------------------

🚀 Códigos de Iniciación y Uso Local (uv)
Sigue estos pasos detallados para levantar el proyecto desde cero utilizando el gestor uv:

1. Sincronizar el entorno e instalar dependencias
Bash

➡️📂 Ingresar a la carpeta raíz del proyecto
cd python-project-174

🔄 Sincronizar e instalar el entorno virtual con uv
uv sync

2. Configurar la base de datos
Crea una base de datos PostgreSQL local, genera tu archivo .env en la raíz del proyecto basándote en la estructura de variables requerida y ejecuta los scripts de inicialización SQL provistos en la sección anterior.

3. Lanzar el Servidor de Desarrollo
Para arrancar la aplicación en modo local utilizando el entorno administrado por uv, ejecuta:

Bash
uv run flask --app page_analyzer:app run --debug
El servidor web estará disponible inmediatamente en la dirección: http://127.0.0.1:5000


---------------------------------------------------------------------------------------------------

📊 Demostración externa (Demo)

Se puede ver la aplicación funcionando en vivo en el siguiente enlace: https://python-project-207-32p0.onrender.com


---------------------------------------------------------------------------------------------------

📁 Estructura del Proyecto

python-project-174/
│
├── page_analyzer/
│   ├── __init__.py
│   └── app.py              # Lógica principal del servidor web Flask
│
├── templates/              # Vistas y componentes HTML
│   ├── index.html          # Formulario principal de registro de URLs
│   ├── show.html           # Vista detallada de un sitio y su historial SEO
│   └── urls.html           # Listado de todos los sitios web indexados
│
├── .env.example            # Ejemplo de como van las Variables de entorno locales
├── build.sh                # Configuracion de conexion con base de datos
├── pyproject.toml          # Configuración de dependencias del proyecto para uv
├── README.md               # Documentación técnica principal
└── database.sql            # Script de inicialización para PostgreSQL


---------------------------------------------------------------------------------------------------
