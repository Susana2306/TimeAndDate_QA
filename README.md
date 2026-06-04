# TimeAndDate_QA

Proyecto de **Calidad de Software** aplicado al sitio web [timeanddate.com](https://www.timeanddate.com). El objetivo es garantizar el correcto funcionamiento de las funcionalidades principales del aplicativo mediante pruebas automatizadas con enfoque BDD (Behavior Driven Development).

## Alcance del proyecto

El proyecto abarca la automatización de escenarios de prueba sobre los módulos clave de **timeanddate.com**, incluyendo:

- **Autenticación y personalización de usuario** — inicio de sesión, configuración de perfil, preferencias de ciudad e idioma.
- **Zonas horarias y reloj mundial** — consulta y conversión entre husos horarios, visualización de relojes por ciudad.
- **Gestión de eventos** — creación y cancelación de eventos personales.
- **Clima y astronomía** — consulta de temperatura, condiciones climáticas y datos astronómicos por ubicación.
- **Herramientas de tiempo** — temporizador, cronómetro, calculadora de fechas y uso combinado de funciones de tiempo.
- **Interacción social** — contribuciones de contenido y suscripción a newsletter.

Cada escenario contempla **rutas críticas** (flujo exitoso esperado) y **rutas alternas** (manejo de errores, validaciones y casos límite).

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| [Python](https://www.python.org/) | Lenguaje base del proyecto |
| [Behave](https://behave.readthedocs.io/) | Framework BDD para escribir y ejecutar escenarios en lenguaje Gherkin |
| [Selenium WebDriver](https://www.selenium.dev/) | Automatización de interacciones en el navegador |
| [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager) | Gestión automática de drivers de navegador |
| [behave-html-formatter](https://github.com/behave/behave-html-formatter) | Generación de reportes HTML de los resultados de prueba |

## Estructura del proyecto

```
TimeAndDate_QA/
├── features/
│   ├── environment.py              # Hooks globales: inicialización del navegador y captura de pantalla en fallos
│   ├── steps/                      # Definiciones de pasos (step definitions) en Python
│   └── ESC_XXX_<Nombre>/           # Un directorio por escenario de prueba
│       └── escenario_XXX.feature   # Escenarios escritos en Gherkin (español)
├── behave.ini                       # Configuración del formatter HTML y salida de behave
├── requirements.txt                 # Dependencias del proyecto
├── requirements.py                  # Script auxiliar para verificar e instalar dependencias automáticamente
├── reporte_pruebas.html             # Reporte HTML generado con los resultados de la última ejecución
└── evidencias_fallas/               # Capturas de pantalla generadas automáticamente cuando un escenario falla
```

## Requisitos previos

- Python 3.8 o superior
- Navegador Google Chrome instalado
- Conexión a Internet (el sitio timeanddate.com debe estar accesible)

## Instalación de dependencias

### Opción 1: Script automático

```bash
python requirements.py
```

Este script verifica si las dependencias están instaladas y, en caso contrario, las instala automáticamente.

### Opción 2: pip manual

```bash
pip install -r requirements.txt
```

## Ejecución de las pruebas

### Ejecutar todos los escenarios

```bash
behave
```

### Ejecutar escenarios por etiqueta

```bash
# Solo rutas críticas
behave --tags=RutaCritica

# Solo rutas alternas
behave --tags=RutaAlterna

# Escenarios de un módulo específico
behave features/ESC_009_Zonas_Horarias_Basico/
```

### Generar reporte HTML

El proyecto está configurado para generar automáticamente un reporte HTML:

```bash
behave -f html -o reporte_pruebas.html
```

O directamente (la configuración en `behave.ini` ya lo habilita):

```bash
behave
```

## Características del framework de pruebas

- **Hooks automáticos**: antes de cada escenario se inicializa una instancia limpia de Chrome maximizado; después de cada escenario el navegador se cierra para liberar recursos.
- **Esperas implícitas**: configuradas a 8 segundos para manejar la carga dinámica del sitio.
- **Evidencias en fallos**: si un escenario falla, se captura automáticamente una screenshot en `evidencias_fallas/<nombre_escenario>.png` para facilitar el análisis.
- **Idioma Gherkin en español**: todos los escenarios están escritos en español (`# language: es`).
- **Separación por escenarios**: cada funcionalidad tiene su propio directorio con archivos `.feature` independientes, lo que permite mantenimiento y ejecución modular.

## Autores

Proyecto desarrollado como parte de la asignatura **Calidad de Software**.
