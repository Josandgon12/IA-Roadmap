# IA Local - RAG con Ollama

Este proyecto demuestra cómo implementar un sistema de **Retrieval-Augmented Generation (RAG)** que se ejecuta de forma 100% local y privada, sin enviar datos a la nube.

---

## Guía de Inicio Rápido

### 1. Requisitos
- **Python 3.10+**
- **Ollama**: [Descargar e instalar Ollama](https://ollama.com/)
- **Modelo Llama 3.2**: Ejecuta `ollama run llama3.2` en tu terminal para descargar el modelo.

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

### 3. Ejecución
```bash
python rag_local.py
```

---

## Cómo funciona

El script utiliza **Ollama** para ejecutar el modelo `llama3.2` en tu propia CPU/GPU. El flujo es el siguiente:
1.  Se define un **contexto privado** (simulando una base de conocimiento).
2.  Se recibe la pregunta del usuario.
3.  Se construye un **Prompt Enriquecido** que combina el contexto con la pregunta.
4.  El modelo local genera una respuesta basada exclusivamente en la información provista.

---

## Tecnologías Utilizadas

- **[Ollama](https://ollama.com/)**: Motor de ejecución de LLMs en local.
- **Llama 3.2**: Modelo de lenguaje de Meta optimizado para eficiencia.
- **Librería `ollama` (Python)**: Wrapper oficial para interactuar con el servidor de Ollama.

---

## Conceptos Clave

- **RAG Local**: Privacidad total de los datos.
- **Inferencia en CPU**: Ejecución sin necesidad de hardware de servidor.
- **Prompt Engineering**: Técnicas para forzar al modelo a seguir el contexto.

### ¿Qué es RAG (Retrieval-Augmented Generation)?

Los modelos de lenguaje (LLMs) como Llama, ChatGPT o Claude están pre-entrenados con gigantescas cantidades de información pública de internet hasta una fecha concreta, pero **no conocen los datos privados de tu empresa** (tus políticas internas, tu historial de tickets, manuales de tu producto, saldo de un cliente, etc.). 

Si le preguntas sobre tu negocio, la IA tratará de adivinar o "alucinará" una respuesta porque no tiene esa información.

**RAG** soluciona este problema mediante dos pasos fundamentales:
1.  **Retrieval (Recuperación / Búsqueda):** Cuando el usuario hace una pregunta, primero se busca en tus datos privados la información que podría ayudar a responder esa pregunta en particular. (En nuestro script simple, nos saltamos la búsqueda en base de datos y cargamos todo el mini-contexto `contexto_privado`).
2.  **Augmented Generation (Generación Aumentada):** Ese contexto recuperado se "pega" o "aumenta" en el mensaje ("prompt") original del usuario antes de enviárselo al modelo de IA. De esta forma, le estamos diciendo a la IA: *"Responde a la pregunta del usuario utilizando este texto como tu única fuente de verdad"*, lo que vuelve al sistema altamente preciso y adaptado a tus necesidades y datos.

### ¿Por qué ejecutarlo "Local"?

*   **Privacidad Total:** Los datos (tanto tu contexto de negocio como las preguntas que puedan hacer tus clientes) nunca salen de tu ordenador. No hay envíos de información confidencial a la nube de terceros (Google, OpenAI, Anthropic).
*   **Eliminación de Costes de API:** Todo el procesamiento ocurre en tu máquina. Puedes hacer miles de consultas sin tener que preocuparte por facturas calculadas o "Tokens consumidos".
*   **Seguridad y Funcionamiento Offline:** El sistema es independiente y puede funcionar completamente aislado sin necesidad de conexión a internet una vez tengas el modelo en tu máquina.

## ⚙️ Requisitos para ejecutar este proyecto

1.  **Python 3.x** instalado.
2.  Tener instalado el software **Ollama** en tu sistema (se descarga desde [ollama.com](https://ollama.com)).
3.  Ejecutar el servidor local de modelos descargando tu LLM. Abre una terminal y corre: `ollama run llama3.2` (esto es un modelo de varios GBs, puede tardar un poco la primera vez).
4.  Tener configurado y activado tu entorno virtual de Python.
5.  Instalar la dependencia para comunicarse con Ollama desde Python: `pip install ollama`

Para ejecutar la prueba simplemente:
```bash
python rag_local.py
```
