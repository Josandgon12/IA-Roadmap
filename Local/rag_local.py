import ollama

# 1. Tu "Base de Datos" (En un RAG real, esto se extraería de un PDF con ChromaDB)
contexto_privado = """
Políticas de la tienda AutoParts:
- Horario: Lunes a Viernes de 09:00 a 18:00. Sábados cerrado.
- Devoluciones: Se aceptan hasta 15 días después de la compra presentando el ticket original.
- Stock actual destacado: Baterías de litio (Agotado), Escobillas limpiaparabrisas (12 unidades).
"""

# 2. La pregunta del usuario
pregunta_usuario = "Hola, compré unas escobillas ayer pero no me valen. ¿Puedo devolverlas hoy si es sábado? Y por cierto, ¿os quedan baterías?"

# 3. Construcción del Prompt RAG (Retrieval-Augmented Generation)
# Le decimos al modelo que actúe estrictamente basándose en el contexto.
prompt_enriquecido = f"""
Eres un asistente de atención al cliente. Responde a la pregunta del usuario utilizando ÚNICAMENTE la siguiente información de contexto. Si la respuesta no está en el contexto, di que no lo sabes.

Contexto:
{contexto_privado}

Pregunta del usuario: {pregunta_usuario}
"""

print("Procesando en local con tu CPU (Llama 3.2)...\n")

# 4. Llamada a la API local de Ollama
respuesta = ollama.chat(
    model='llama3.2',
    messages=[
        {'role': 'user', 'content': prompt_enriquecido}
    ]
)

# 5. Imprimir el resultado
print("🤖 Respuesta de la IA:")
print(respuesta['message']['content'])