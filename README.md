# IA-Roadmap: Ecosistema de Agentes y Automatización con Inteligencia Artificial

Este repositorio centraliza proyectos de vanguardia relacionados con Agentes GenAI, Function Calling, RAG y Model Context Protocol (MCP). Está diseñado para ser una guía práctica y modular para desarrolladores que buscan implementar soluciones basadas en los últimos modelos de lenguaje (LLMs).

---

## Proyectos Incluidos

| Proyecto | Estado | Tecnología Principal | Descripción |
| :--- | :---: | :--- | :--- |
| **[Agente](./Agente)** | OK | CrewAI + Gemini | Orquestación de una Agencia de Software Virtual con roles especializados. |
| **[Chatbot](./Chatbot)** | OK | Gemini SDK | Chatbot E-commerce con capacidad de ejecución de funciones locales (Function Calling). |
| **[Local](./Local)** | OK | Ollama + Llama 3.2 | Implementación de RAG optimizada para ejecución 100% privada y local. |
| **[MCP](./MCP)** | Pendiente | Model Context Protocol | Implementación de cliente y servidor para el nuevo estándar de Anthropic/Google. |
| **[RAG](./RAG)** | OK | LangChain + ChromaDB | Sistema robusto de Retrieval-Augmented Generation con persistencia vectorial. |

---

## Requisitos Previos

Para ejecutar los proyectos de este repositorio, necesitarás:

1.  **Python 3.10+**: [Descargar aquí](https://www.python.org/downloads/)
2.  **Git**: [Descargar aquí](https://git-scm.com/)
3.  **API Keys**: Para la mayoría de los proyectos, necesitarás una clave de Google AI Studio ([Consíguela gratis aquí](https://aistudio.google.com/app/apikey)).
4.  **Ollama** (Opcional): Necesario solo para el proyecto `Local`. [Instalar Ollama](https://ollama.com/).

---

## Guía de Inicio Rápido (Recomendado)

Hemos incluido un script de automatización (`install_all.py`) que configura todos los proyectos, crea los entornos virtuales y prepara los archivos de configuración por ti. 

> [!IMPORTANT]
> Ejecuta este script desde la raíz del repositorio para tener todo listo en segundos.

```bash
# 1. Clona el repositorio
git clone https://github.com/Josandgon12/IA-Roadmap.git
cd IA-Roadmap

# 2. Ejecuta el instalador automático
python install_all.py

# 3. Configura tus claves
# Edita los archivos .env que se han generado en cada carpeta con tu API KEY.
```

---

## Uso de los Proyectos

Cada carpeta es independiente y contiene su propio entorno virtual (`venv`). Sigue estos pasos para usar un proyecto específico (ej: Chatbot):

1.  **Entra en la carpeta**: `cd Chatbot`
2.  **Activa el entorno**:
    *   Windows: `.\venv\Scripts\activate`
    *   Mac/Linux: `source venv/bin/activate`
3.  **Ejecuta el programa**: `python app.py`

---

## Licencia

Este proyecto está bajo la licencia **MIT** - consulta el archivo [LICENSE](./LICENSE) para más detalles.

---

> [!TIP]
> Desarrollado para la comunidad de IA por [Josandgon12](https://github.com/Josandgon12).
