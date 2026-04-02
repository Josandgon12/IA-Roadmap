# Local RAG con Ollama

Este proyecto es una prueba de concepto (PoC) sencilla para demostrar cómo funciona el concepto de **RAG (Retrieval-Augmented Generation)** de forma completamente local, utilizando modelos de lenguaje de código abierto a través de **Ollama**.

## 🚀 Cómo funciona

El script `rag_local.py` simula un asistente de atención al cliente para una tienda ficticia llamada "AutoParts". El flujo de ejecución es el siguiente:

1.  **Definición del Contexto (La "Base de Datos"):** En lugar de conectarse a una base de datos vectorial o realizar búsquedas en tiempo real, el script define un bloque de texto duro (`contexto_privado`) con información específica del negocio (tiempos de devolución, horarios, stock). Este texto actúa como nuestra "fuente de conocimiento".
2.  **Captura de la Pregunta:** Se define una pregunta del usuario simulando una consulta real sobre devoluciones fuera de horario y verificación de stock.
3.  **Construcción del Prompt (Enriquecimiento):** Aquí ocurre la magia del RAG. El script toma la instrucción base (comportarse como un asistente de atención al cliente), le inyecta el `contexto_privado` (nuestra información) y le añade la `pregunta_usuario`. Se le da la instrucción estricta a la IA de responder *únicamente* basándose en ese contexto proporcionado.
4.  **Inferencia Local (Ollama):** El prompt enriquecido se envía al modelo `llama3.2` que se está ejecutando localmente en tu máquina a través de la API local que expone Ollama.
5.  **Respuesta:** El modelo analiza la pregunta en base al contexto dado, compila una respuesta coherente y la devuelve para ser impresa en la consola.

## 🛠️ Tecnologías Empleadas

*   **Python:** El lenguaje de programación utilizado para orquestar la lógica.
*   **Ollama:** Una herramienta que simplifica enormemente la ejecución de Large Language Models (LLMs) localmente en tu propio hardware (procesador o tarjeta gráfica).
*   **Llama 3.2:** El modelo de lenguaje específico de IA (desarrollado por Meta) descargado y ejecutado vía Ollama. Considerado excelente para tareas de razonamiento local.
*   **Librería `ollama` para Python:** El cliente oficial en Python usado para interactuar cómodamente con la API local que levanta Ollama en tu ordenador.

## 🧠 Conceptos Clave

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
