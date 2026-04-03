# Chatbot E-commerce - Gemini Function Calling

Este proyecto implementa una **Prueba de Concepto (PoC)** de un chatbot para comercio electrónico capaz de interactuar con sistemas externos (inventario) mediante **Function Calling** con la API de Gemini.

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

## Funcionamiento y Herramientas

El chatbot actúa como un dependiente de una tienda de electrónica y tiene acceso a una herramienta local:

1.  **consultar_stock**: Permite al modelo Gemini consultar una base de datos simulada en Python para conocer la disponibilidad de productos en categorías como `portatiles` o `smartphones`.

El flujo utiliza un ciclo de **dos pasos**:
- **Paso 1**: Gemini recibe la duda del usuario y decide si necesita llamar a la función.
- **Paso 2**: El script ejecuta la función localmente y le devuelve el resultado a Gemini para que genere la respuesta final.

---

## Tecnologías Utilizadas

- **[Google GenAI SDK](https://github.com/google/generative-ai-python)**: La SDK más moderna para Gemini.
- **Gemini 2.5 Flash**: Modelo optimizado para latencia baja y llamadas a funciones.
- **python-dotenv**: Gestión de secretos.

---

## Conceptos Clave

- **Function Calling**: El modelo delega acciones al código.
- **Schema Validation**: Definición rigurosa de los parámetros de la función.
- **Historial de Conversación**: Seguimiento de roles (`user`, `model`, `tool`) para mantener el contexto.
