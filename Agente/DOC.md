# Agencia de Software Virtual - Prueba de Concepto (PoC)

Este proyecto es una Prueba de Concepto (PoC) que implementa un equipo de trabajo autónomo utilizando Inteligencia Artificial para actuar como una **Agencia de Software Virtual**.

El objetivo es automatizar la investigación, el desarrollo y la auditoría de scripts en Python, enfocado inicialmente en tareas de **Web Scraping**.

---

## 🚀 Funcionalidad Principal

El programa crea tres agentes especializados que colaboran secuencialmente para cumplir con una petición del usuario. En este entorno de prueba, la petición establecida por defecto es:

> _"Queremos extraer los titulares de una web de tecnología"_

El flujo de ejecución (pipeline) sigue un **Proceso Secuencial**:

1. **Investigación**: Se evalúan las mejores librerías y enfoques para realizar el scraping.
2. **Programación**: Se toma el documento de arquitectura generado en el paso anterior y se escribe el código de Python funcional.
3. **Control de Calidad (QA)**: Se audita el código generado para corregir ineficiencias o errores, devolviendo el script final impecable listo para ejecutarse.

---

## 🤖 Los Agentes

El sistema cuenta con 3 roles o "personas" impulsadas por LLMs:

- 🕵🏼‍♂️ **Investigador de Tecnología**: Analiza los requerimientos y el estado del arte tecnológico (ej. decidir entre `BeautifulSoup`, `Playwright` o `Scrapy`) para crear un plan de arquitectura.
- 🧑🏻‍💻 **Programador Senior Python**: Se encarga de traducir el plan arquitectónico en un código de Python real, modular, comentando usos de tipado (`type hinting`) y manejo de errores (`try/except`).
- 🧐 **Ingeniero QA**: Funciona como un auditor crítico. Recibe el código del programador, detecta posibles bugs o casos límite (edge cases), asegura buenas prácticas y devuelve única y exclusivamente el código validado.

---

## 🛠 Tecnologías Utilizadas

- **[Python 3](https://www.python.org/)**: Lenguaje de programación principal del proyecto.
- **[CrewAI](https://www.crewai.com/)**: Un framework potente diseñado para la orquestación de agentes autónomos. Permite definir Agentes, Tareas y Procesos para simular el comportamiento humano dentro de un equipo de trabajo (Crew).
- **[LiteLLM](https://docs.litellm.ai/)**: Es la capa interna que emplea CrewAI para comunicarse con los modelos de inteligencia artificial bajo el capó, sirviendo como proxy multimodelo.
- **[Google Generative AI (Gemini)](https://ai.google.dev/)**: El cerebro ("LLM" o Large Language Model) que proporciona la inteligencia a los agentes. Específicamente, utilizamos la familia de modelos `gemini-2.5-flash` por su gran velocidad y capacidad de razonamiento con ventanas de contexto largas.
- **[python-dotenv](https://saurabh-kumar.com/python-dotenv/)**: Módulo empleado para cargar configuraciones secretas (como la variable `GEMINI_API_KEY`) desde un archivo `.env` para que el código quede libre de contraseñas y llaves expuestas.

---

## 🧠 Conceptos Técnicos Clave implementados

- **Agentic Frameworks**: Modelado de agentes impulsados por IA a los cuales se les otorga un rol, un contexto (`backstory`) y un objetivo (`goal`).
- **Task Delegation**: Separación del trabajo algorítmico en "Tareas" atómicas (`Tasks`). Cada tarea tiene una descripción minuciosa y un resultado esperado, asignándose al agente más apto para el trabajo.
- **Orquestación Secuencial**: Uso del sistema `Process.sequential` disponible en CrewAI. Esto asegura que la salida (output) del Trabajador A vaya directamente como alimentación (input) al marco de trabajo del Trabajador B, impidiendo saltos lógicos en la resolución de problemas de software.
- **LLM Abstraction**: Gracias a LiteLLM se evita usar el SDK directo de Google en el código para la inferencia, en cambio, la configuración se mantiene mediante la definición de `llm='gemini/gemini-1.5-flash'` inyectado en cada agente y configurado a través de variables de entorno.
