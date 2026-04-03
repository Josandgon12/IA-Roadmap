# Sistema RAG con Gemini Flash

> **Retrieval-Augmented Generation** — Un sistema de preguntas y respuestas que utiliza tus propios documentos como base de conocimiento.

---

## ¿Qué es RAG?

**RAG (Retrieval-Augmented Generation)** es un patrón de arquitectura de IA que combina dos capacidades:

1. **Retrieval (Recuperación):** Buscar en una base de conocimiento los fragmentos de texto más relevantes para una pregunta.
2. **Generation (Generación):** Usar un modelo de lenguaje (LLM) para generar una respuesta basada *únicamente* en esos fragmentos recuperados.

### ¿Por qué RAG y no solo un LLM?

| Aspecto | Solo LLM | LLM + RAG |
|---|---|---|
| **Fuente de conocimiento** | Solo lo que aprendió en su entrenamiento | Tus documentos específicos |
| **Alucinaciones** | Puede inventar información | Responde solo con lo que encuentra en tus docs |
| **Actualización** | Requiere re-entrenamiento | Solo añade/actualiza archivos `.txt` |
| **Privacidad** | Tus datos no se procesan localmente | Los documentos se procesan y almacenan en local |

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                        SISTEMA RAG                              │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌────────────┐                 │
│  │  📄 Docs │───▶│ ✂️ Chunks│───▶│ 🧠 Embeddings│               │
│  │  (.txt)  │    │ (1000c)  │    │ (vectores) │                 │
│  └──────────┘    └──────────┘    └─────┬──────┘                 │
│                                        │                        │
│                                        ▼                        │
│                                 ┌──────────────┐                │
│                                 │  💾 ChromaDB  │                │
│                                 │ (base vectorial)│              │
│                                 └──────┬───────┘                │
│                                        │                        │
│  ┌──────────┐                          │                        │
│  │ 🤔 Pregunta│─── búsqueda ──────────▶│                        │
│  │ del usuario │    semántica           │                        │
│  └──────────┘                          │                        │
│        │                               ▼                        │
│        │                    ┌───────────────────┐               │
│        │                    │ 📋 Top 3 fragmentos│              │
│        │                    │   más relevantes   │              │
│        │                    └─────────┬─────────┘               │
│        │                              │                         │
│        ▼                              ▼                         │
│  ┌─────────────────────────────────────────┐                    │
│  │          ⚡ Gemini 2.5 Flash            │                    │
│  │  Prompt: "Usa SOLO este contexto para   │                    │
│  │           responder la pregunta"        │                    │
│  └───────────────────┬─────────────────────┘                    │
│                      │                                          │
│                      ▼                                          │
│              ┌──────────────┐                                   │
│              │ 🤖 Respuesta │                                   │
│              │  generada    │                                   │
│              └──────────────┘                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Tecnologías Utilizadas

### LangChain (v1.x) — *Framework de orquestación*
LangChain es el framework que conecta todos los componentes. En este proyecto se usan los siguientes subpaquetes:

| Paquete | Uso |
|---|---|
| `langchain-core` | Primitivas LCEL (`RunnablePassthrough`, `StrOutputParser`, `ChatPromptTemplate`) |
| `langchain-community` | `DirectoryLoader` y `TextLoader` para cargar documentos |
| `langchain-text-splitters` | `RecursiveCharacterTextSplitter` para dividir documentos en chunks |
| `langchain-chroma` | Integración con la base de datos vectorial ChromaDB |
| `langchain-google-genai` | Integración con los modelos de Google (Gemini) |

> **Nota:** Este proyecto usa la API moderna **LCEL** (LangChain Expression Language) con el operador pipe (`|`), que reemplaza las antiguas funciones `create_retrieval_chain` y `create_stuff_documents_chain` eliminadas en LangChain 1.x.

### Google Gemini — *Modelos de IA*
Se utilizan **dos modelos** de Google:

| Modelo | Función | Descripción |
|---|---|---|
| `gemini-embedding-001` | **Embeddings** | Convierte texto en vectores numéricos de 3072 dimensiones para búsqueda semántica |
| `gemini-2.5-flash` | **Generación** | Modelo de lenguaje rápido y eficiente que genera las respuestas finales |

### ChromaDB — *Base de datos vectorial*
ChromaDB almacena los embeddings (vectores) de los fragmentos de texto en disco local (carpeta `./chroma_db`). Permite realizar búsquedas por **similitud semántica**: en lugar de buscar palabras exactas, encuentra los fragmentos cuyo *significado* es más cercano a la pregunta.

### python-dotenv — *Gestión de secrets*
Carga la API key de Google desde un archivo `.env` para no exponerla en el código fuente.

---

## 🔄 Flujo de Funcionamiento Detallado

### Fase 1: Inicialización (se ejecuta una vez al arrancar)

#### Paso 1 — Lectura de Documentos
```python
loader = DirectoryLoader('./docs', glob="**/*.txt", loader_cls=TextLoader)
documentos = loader.load()
```
- Escanea la carpeta `./docs` buscando todos los archivos `.txt`
- Cada archivo se convierte en un objeto `Document` con su contenido y metadatos (ruta del archivo)
- **Resultado:** Lista de documentos cargados en memoria

#### Paso 2 — División en Chunks (Fragmentación)
```python
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documentos)
```
- Divide cada documento en fragmentos de **1000 caracteres**
- Aplica un **solapamiento de 200 caracteres** entre chunks consecutivos
- El solapamiento asegura que no se pierda contexto en los bordes de cada fragmento

**Ejemplo visual:**
```
Documento original (2200 caracteres):
[=====================================================]

Chunk 1 (1000 chars):  [=========================]
Chunk 2 (1000 chars):            [=========================]    ← 200 chars de overlap
Chunk 3 (400 chars):                       [========]
```

#### Paso 3 — Creación de Embeddings y Almacenamiento Vectorial
```python
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="./chroma_db")
```
- Cada chunk de texto se envía a la API de Google, que devuelve un **vector de 3072 números decimales**. Este vector representa el *significado semántico* del texto
- Los vectores se almacenan en ChromaDB junto con el texto original
- Se persisten en disco (`./chroma_db`) para no tener que recalcularlos cada vez

> **¿Qué es un embedding?** Es una representación numérica del significado de un texto. Textos con significados similares tendrán vectores cercanos entre sí en el espacio de 3072 dimensiones.

#### Paso 4 — Configuración de la Cadena RAG (LCEL)
```python
rag_chain = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

Esta cadena LCEL define el pipeline completo usando el operador `|`:

1. **`retriever | format_docs`** → Busca los 3 chunks más relevantes y los concatena como texto
2. **`RunnablePassthrough()`** → Pasa la pregunta del usuario tal cual
3. **`prompt`** → Inyecta el contexto y la pregunta en el template del prompt
4. **`llm`** → Envía todo a Gemini 2.5 Flash
5. **`StrOutputParser()`** → Extrae la respuesta como texto plano

### Fase 2: Bucle de Preguntas (interactivo)

```
Usuario escribe pregunta
        │
        ▼
¿Es "salir"/"exit"/"quit"?  ──Sí──▶  Fin del programa
        │ No
        ▼
rag_chain.invoke(pregunta)
        │
        ├── 1. Retriever busca los 3 chunks más similares semánticamente
        ├── 2. format_docs los concatena como texto plano
        ├── 3. El prompt inyecta: contexto + pregunta
        ├── 4. Gemini Flash genera la respuesta
        └── 5. Se imprime la respuesta
        │
        ▼
Vuelve a pedir pregunta
```

---

## 📁 Estructura del Proyecto

```
RAG/
├── 📄 app.py              # Script principal del sistema RAG
├── 📄 requirements.txt    # Dependencias Python del proyecto
├── 📄 .env                # API key de Google (NO compartir)
├── 📁 docs/               # Carpeta con los documentos de conocimiento
│   ├── ejemplo1.txt       # Documento sobre el "Proyecto Fénix"
│   ├── ejemplo2.txt       # Documento sobre la "Selva de Cristal"
│   └── yo.txt             # Documento con información personal
├── 📁 chroma_db/          # Base de datos vectorial (se genera automáticamente)
└── 📁 venv/               # Entorno virtual Python
```

---

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
GOOGLE_API_KEY="TU_API_KEY_AQUÍ"
```

### 4. Preparar Documentos
Coloca tus archivos `.txt` en la carpeta `./docs/`.

### 5. Ejecución
```bash
python app.py
```

---

## Parámetros Configurables

Estos valores se pueden ajustar directamente en `app.py`:

| Parámetro | Valor actual | Descripción | Línea |
| :--- | :--- | :--- | :--- |
| `chunk_size` | `1000` | Tamaño máximo de cada fragmento (en caracteres) | 45 |
| `chunk_overlap` | `200` | Solapamiento entre chunks consecutivos | 45 |
| `search_kwargs["k"]` | `3` | Número de fragmentos recuperados por pregunta | 58 |
| `temperature` | `0.3` | Creatividad del modelo (0 = preciso, 1 = creativo) | 62 |
| `model` (LLM) | `gemini-2.5-flash` | Modelo de generación | 62 |
| `model` (Embeddings) | `gemini-embedding-001` | Modelo de embeddings | 52 |

### Recomendaciones de ajuste:
- **Documentos cortos** → Reducir `chunk_size` a 500
- **Respuestas imprecisas** → Aumentar `k` a 5 para dar más contexto al modelo
- **Respuestas demasiado creativas** → Bajar `temperature` a 0.1
- **Respuestas más detalladas** → Subir `temperature` a 0.5-0.7

---

## Dependencias

```txt
langchain>=0.3.0              # Framework de orquestación (core vacío en v1.x)
langchain-community>=0.3.0    # Loaders de documentos
langchain-chroma>=0.1.4       # Integración con ChromaDB
langchain-google-genai>=2.0.0 # Integración con Google Gemini
python-dotenv>=1.0.1          # Carga de variables de entorno
chromadb>=0.5.15              # Base de datos vectorial local
```

---

## Preguntas Frecuentes

### ¿Puedo usar otros tipos de archivos además de `.txt`?
Sí, LangChain soporta PDF, Word, CSV, y muchos más. Solo necesitas cambiar el `loader_cls` y el `glob` en la línea 29. Por ejemplo para PDFs:
```python
from langchain_community.document_loaders import PyPDFLoader
loader = DirectoryLoader('./docs', glob="**/*.pdf", loader_cls=PyPDFLoader)
```
*(Requiere instalar `pypdf`: `pip install pypdf`)*

### ¿Qué pasa si el modelo no encuentra la respuesta?
El prompt le indica explícitamente que diga *"el documento no menciona nada al respecto"* en lugar de inventar información. Esto evita las alucinaciones.

### ¿Necesito internet para ejecutarlo?
**Sí**, tanto para generar embeddings como para obtener respuestas de Gemini se necesita conexión, ya que ambos modelos se ejecutan en la nube de Google.

### ¿Tiene coste usar la API de Google?
La API de Gemini tiene un **nivel gratuito** generoso. Para un uso personal/aprendizaje es más que suficiente. Puedes consultar los límites en [Google AI Studio](https://aistudio.google.com/).

### ¿Cada vez que ejecuto el programa se recalculan los embeddings?
Sí, en la implementación actual se recalculan al inicio. Para optimizar esto, podrías cargar el vectorstore existente si la carpeta `chroma_db/` ya existe:
```python
if os.path.exists("./chroma_db"):
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
else:
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="./chroma_db")
```
