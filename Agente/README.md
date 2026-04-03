# Agencia de Software Virtual - CrewAI PoC

Este proyecto es una **Prueba de Concepto (PoC)** que implementa un equipo de trabajo autónomo utilizando Inteligencia Artificial para actuar como una Agencia de Software Virtual.

Utiliza el framework **CrewAI** para orquestar agentes especializados que investigan, programan y supervisan tareas de desarrollo de software (enfocado inicialmente en Web Scraping).

---

## Guía de Inicio Rápido

### 1. Requisitos
- **Python 3.10+**
- Una API Key de **Google AI Studio** ([Consíguela aquí](https://aistudio.google.com/app/apikey)).

### 2. Instalación Manual (Si no usaste el `install_all.py` de la raíz)
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configuración
Crea un archivo `.env` (o renombra el `.env.example`) y añade tu clave:
```text
GEMINI_API_KEY="TU_API_KEY_AQUÍ"
```

### 4. Ejecución
```bash
python app.py
```

---

## Flujo de Trabajo (Pipeline)

El sistema cuenta con 3 agentes que colaboran de forma secuencial:

1.  **Investigador de Tecnología**: Analiza los requerimientos y define la mejor arquitectura (ej. decidir entre `BeautifulSoup`, `Playwright` o `Scrapy`).
2.  **Programador Senior Python**: Traduce el plan en código real, modular y con manejo de errores.
3.  **Ingeniero QA**: Audita el código, busca bugs y entrega la versión final optimizada.

---

## Tecnologías Utilizadas

- **[CrewAI](https://www.crewai.com/)**: Orquestación de agentes autónomos.
- **[Google Gemini 2.5 Flash](https://ai.google.dev/)**: Cerebro de los agentes (LLM).
- **[python-dotenv](https://saurabh-kumar.com/python-dotenv/)**: Gestión de variables de entorno seguras.

---

## Conceptos Clave

- **Agentic Workflows**: Roles (`backstory`), objetivos (`goal`) y delegación.
- **Sequential Process**: El output de un agente es el input del siguiente.
- **LLM Abstraction**: Uso de variables de entorno para configurar el modelo sin hardcodearlo.
