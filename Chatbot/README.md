# Chatbot con Function Calling (Llamada a Funciones)

Este proyecto implementa una Prueba de Concepto (PoC) de un chatbot de comercio electrónico capaz de interactuar con sistemas externos mediante el uso de "Llamada a Funciones" (Function Calling) gracias a la API de Gemini. El chatbot actúa como dependiente de una tienda de electrónica y puede consultar disponibilidad de stock basándose en el inventario simulado.

## Tecnologías Empleadas

* **Python 3.x**: El lenguaje de programación utilizado para orquestar la lógica.
* **SDK `google-genai`**: Es el SDK oficial más moderno de Google para interactuar de forma segura con la API de Gemini.
* **`python-dotenv`**: Librería para cargar variables de entorno (como la API Key de Gemini) desde un archivo `.env` sin exponerlas en el código fuente.
* **Modelo Gemini 2.5 Flash**: Elegido como el motor lógico del programa (`gemini-2.5-flash`) por su bajo tiempo de respuesta y sus altas capacidades trabajando con esquemas de herramientas JSON.

## Funcionamiento del Programa

El flujo de ejecución del script principal (`app.py`) se divide en varios pasos lógicos:

1. **Inicialización y Configuración**: 
   Se cargan las credenciales desde el `.env`, se inicializa el cliente de Gemini y se declara el *System Prompt* (instrucciones de sistema) que configuran la personalidad y restricciones del bot.

2. **Bucle de Conversación (REPL)**: 
   El sistema entra en un ciclo infinito donde escucha los mensajes del usuario en la consola hasta que se interrumpe o se escribe un comando de salida.

3. **Mantenimiento del Historial**:
   Para que el chatbot tenga memoria en la misma sesión, se guarda todo el diálogo (preguntas, respuestas y resultados de base de datos) de forma secuencial en una lista llamada `historial`. Toda esta lista se envía completa al LLM en cada interacción.

4. **Flujo de Peticiones y Ejecución de Herramientas**:
   El Function Calling sigue un ciclo de "Dos Pasos" bien diferenciado:
   * **Petición Inicial**: Se manda el mensaje del usuario al modelo Gemini. El modelo analiza el texto y decide si necesita información externa. En lugar de generar texto natural, devuelve de manera estructurada una intención de uso de herramienta (`function_calls`), con los parámetros extraídos.
   * **Ejecución Local**: Nuestro código de Python detecta esta solicitud del LLM. Llama a nuestra función real `consultar_stock` ejecutándola en la máquina local usando los argumentos provistos por la IA.
   * **Segunda Petición**: El código recoge los resultados devueltos por la "base de datos" de Python, los añade al `historial` atribuyéndoselos al rol de la herramienta (`role="tool"`), y le devuelve esto a Gemini. Gemini analiza la nueva respuesta y genera el mensaje final, fluido y en lenguaje natural.

## Conceptos Clave Empleados

* **Function Calling (Tools)**: La capacidad de potenciar a un modelo de lenguaje permitiéndole delegar acciones (conseguir datos, hacer cálculos, afectar al sistema físico) al propio programa en el que está anidado. Evita las alucinaciones al depender de la información verificable que el código provee.
* **Esquema Tipado (Schema)**: La definición rigurosa que le enseñamos al modelo sobre cómo interactuar con nuestra función (`types.Schema`, `types.Tool`). Describe no solo los nombres de variables sino sus propósitos precisos (`producto` y `categoria`).
* **Roles de Conversación Diferenciados**: En lugar de solo cruzar texto, el programa maneja objetos y roles estructurales explícitos: `user` (el humano), `model` (la IA general y sus intenciones) y `tool` (la máquina que retorna información dura sin interpretar).
* **Mock Context** (Base de datos Mockeada): El uso de un entorno aislado (un simple diccionario en Python) para actuar como una pasarela o gemelo digital de lo que en un entorno de producción real sería una base de datos SQL conectada mediante SQLAlchemy o una consulta externa a pasarelas de inventario.
