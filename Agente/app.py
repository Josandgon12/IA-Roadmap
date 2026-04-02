import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

# ==========================================
# Configuración del LLM
# ==========================================
# CrewAI utiliza por defecto las variables de entorno para configurar el LLM a través de LiteLLM.
# Para usar Gemini, asegúrate de tener configurada la variable de entorno GEMINI_API_KEY.
# Ejemplo en terminal: export GEMINI_API_KEY="tu_api_key"
# Si utilizas otro proveedor, ajusta las variables de entorno o configura el parámetro `llm` en cada Agente.

# ==========================================
# 1. Definición de Agentes
# ==========================================

investigador = Agent(
    role='Investigador de Tecnología',
    goal='Investigar las herramientas más modernas y eficientes para cumplir la solicitud de: {topic}',
    backstory=(
        'Eres un analista de tecnología vanguardista experto en automatización y web scraping. '
        'Conoces las últimas tendencias del mundo del desarrollo en 2026 y puedes recomendar la '
        'arquitectura más robusta (ej. decidir entre BeautifulSoup, Playwright, Scrapy).'
    ),
    verbose=True,
    allow_delegation=False,
    llm='gemini/gemini-2.5-flash'
)

programador = Agent(
    role='Programador Senior Python',
    goal='Transformar planes de arquitectura en código Python funcional, modular y limpio.',
    backstory=(
        'Un ingeniero de software veterano, reconocido por escribir código Python impecable, '
        'seguro y fácil de mantener. Sigues las mejores prácticas y principios SOLID.'
    ),
    verbose=True,
    allow_delegation=False,
    llm='gemini/gemini-2.5-flash'
)

qa = Agent(
    role='Ingeniero QA',
    goal='Auditar código, buscar bugs o casos límite (edge cases), y crear la versión final perfecta.',
    backstory=(
        'Un detallista auditor de código y analista de calidad. Tienes vista de águila para '
        'detectar vulnerabilidades, ineficiencias o errores lógicos. No apruebas nada que no sea perfecto.'
    ),
    verbose=True,
    allow_delegation=False,
    llm='gemini/gemini-2.5-flash'
)

# ==========================================
# 2. Definición de Tareas (Tasks)
# ==========================================

tarea_investigacion = Task(
    description=(
        'Analizar cuál es la mejor forma de hacer web scraping a una página de noticias '
        'basado en la siguiente solicitud: "{topic}". '
        'Determina si usar peticiones síncronas/asíncronas, qué librerías emplear (ej. BeautifulSoup o Playwright) '
        'para lidiar con posibles barreras anti-bot actuales en 2026. '
        'Escribe un plan de arquitectura paso a paso.'
    ),
    expected_output='Un documento de plan de arquitectura detallado con la estrategia y librerías recomendadas.',
    agent=investigador
)

tarea_programacion = Task(
    description=(
        'Lee el plan de arquitectura creado por el Investigador. '
        'Genera el código Python completo, funcional y modular que implemente exactamente dicho plan. '
        'Asegúrate de incluir manejo de errores (try/except) y tipado (type hinting).'
    ),
    expected_output='Código Python completo y documentado, directamente utilizable.',
    agent=programador
)

tarea_qa = Task(
    description=(
        'Revisa el código generado por el Programador Senior. '
        'Aplica correcciones si detectas fallos, mejora la seguridad y eficiencia. '
        'Genera la versión final del script aprobada y devuelve EXCLUSIVAMENTE el código.'
    ),
    expected_output='El código final en Python, revisado, optimizado y sin formato de explicación adicional (solo código o bloque de código).',
    agent=qa
)

# ==========================================
# 3. Orquestación del Equipo (Crew)
# ==========================================

# Configuramos el Crew con un proceso secuencial puro. 
# El Output de tarea_investigacion irá al workspace de tarea_programacion, y así sucesivamente.
agencia_software = Crew(
    agents=[investigador, programador, qa],
    tasks=[tarea_investigacion, tarea_programacion, tarea_qa],
    process=Process.sequential,
    verbose=True
)

# ==========================================
# Ejecución Principal
# ==========================================
if __name__ == '__main__':
    print("Iniciando la Agencia de Software Virtual...")
    
    # Kickoff del equipo pasándole el input inicial a través de la variable {topic}
    input_usuario = "Queremos extraer los titulares de una web de tecnología"
    
    resultado_final = agencia_software.kickoff(inputs={'topic': input_usuario})
    
    print("\n\n" + "="*50)
    print("RESULTADO FINAL APROBADO:")
    print("="*50)
    print(resultado_final)
