import sys
import os
import asyncio
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
from google.genai import types

load_dotenv()

async def run_client(prompt: str):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: Asegúrate de tener la variable de entorno GOOGLE_API_KEY configurada.")
        print("En PowerShell: $env:GOOGLE_API_KEY='TU_CLAVE'")
        sys.exit(1)

    print("---Iniciando cliente MCP---")
    # 1. Configurar los parámetros del servidor local
    # Vamos a invocar a nuestro propio servidor hecho en mcp_server.py
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=os.environ.copy()
    )

    print("Conectando con el servidor local Task Manager...")
    # 2. Conectarse al servidor abriendo un canal E/S (stdio)
    try:
        async with stdio_client(server_params) as (read, write):
            # 3. Inicializar la sesión MCP
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("🚀 Conexión MCP establecida exitosamente.\n")

                # 4. Leer las herramientas que el servidor ofrece al cliente LLM
                tools_response = await session.list_tools()
                
                # Convirtiendo estas herramientas al formato que espera Gemini (genai.types.FunctionDeclaration)
                gemini_tools = []
                
                print("Herramientas descubiertas desde el servidor MCP:")
                for t in tools_response.tools:
                    print(f" - [TOOL] {t.name}: {t.description}")
                    props = {}
                    for prop_name in t.inputSchema.get('properties', {}).keys():
                        props[prop_name] = types.Schema(type=types.Type.STRING)
                        
                    schema = types.Schema(
                        type=types.Type.OBJECT,
                        properties=props,
                        required=t.inputSchema.get('required', [])
                    )
                    
                    # Si no tiene propiedades ni requerimientos
                    if not props:
                        schema = None
                    
                    func_decl = types.FunctionDeclaration(
                        name=t.name,
                        description=t.description or "",
                        parameters=schema
                    )
                    gemini_tools.append(func_decl)

                gemini_tool_config = types.Tool(function_declarations=gemini_tools)

                print("\nIniciando comunicación con Gemini...")
                # 5. Configurar Gemini
                genai_client = genai.Client(api_key=api_key)
                
                # Usar chats.create para mantener el historial (importante para iterar herramientas)
                chat = genai_client.chats.create(
                    model='gemini-2.5-flash',
                    config=types.GenerateContentConfig(
                        tools=[gemini_tool_config] if gemini_tools else None,
                        temperature=0.0
                    )
                )

                print(f"\n> Usuario: {prompt}")
                
                # Mandamos la solicitud a Gemini
                response = chat.send_message(prompt)

                # 6. Bucle para que Gemini pueda consultar herramientas iterativamente
                while response.function_calls:
                    # Gemini decidió usar una o más herramientas
                    for fc in response.function_calls:
                        print(f"\n🧠 Gemini decidió usar la herramienta: '{fc.name}'")
                        print(f"📦 Argumentos enviados: {fc.args}")

                        # ¡Llamamos a nuestro servidor MCP para que ejecute la tarea en LOCAL!
                        # Nota: Convertimos fc.args (dict) desempaquetando sus valores, mcp requiere kwargs
                        result = await session.call_tool(fc.name, dict(fc.args))
                        
                        # Obtenemos el output del servidor (es un array de contenidos, cogemos el texto del 1º)
                        output_text = result.content[0].text if result.content else "Éxito sin contenido devuelto."
                        print(f"🖥️ Resultado del Servidor MCP: {output_text}")

                        # Embalamos la respuesta de la herramienta para que Gemini la entienda
                        func_res = types.Part.from_function_response(
                            name=fc.name,
                            response={"result": output_text}
                        )
                        
                        # Mandamos el resultado de la función de vuelta al modelo para seguir la conv.
                        print(f"Enviando resultados locales a Gemini...")
                        response = chat.send_message(func_res)

                # Imprimir la respuesta final consolidada
                print(f"\n✨ IA (Gemini): {response.text}")

    except Exception as e:
         print(f"Error al conectar con MCP Server: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ai_client.py \"Tu prompt aquí\"")
        print("Ejemplo: python ai_client.py \"Añade limpiar la casa a mis tareas y luego dime qué tareas tengo\"")
        sys.exit(1)
        
    # En Windows, asyncio usando subprocesos falla si no se pone esto
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(run_client(sys.argv[1]))
