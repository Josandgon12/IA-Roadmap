import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()

# Inicializamos el cliente. 
# Buscará automáticamente la variable de entorno GEMINI_API_KEY cargada por dotenv
client = genai.Client()

# ====================================================================
# 1. Mock de Base de Datos
# ====================================================================
def consultar_stock(producto: str, categoria: str) -> str:
    """
    Simula una consulta a una base de datos local devolviendo el stock disponible.
    """
    print(f"\n[Servidor] Ejecutando consultar_stock localmente...")
    print(f"[Servidor] Argumentos recibidos -> Producto: '{producto}', Categoría: '{categoria}'")
    
    # Base de datos simulada con valores hardcodeados
    db_mock = {
        "portatiles": {
            "gama alta": 5,
            "gaming": 2,
            "ofimatica": 15
        },
        "smartphones": {
            "gama alta": 10,
            "gama media": 25
        }
    }
    
    # Normalización completa de cadenas (quitar tildes para facilitar cruces)
    cat = categoria.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    prod = producto.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    
    resultados = []
    
    # Lógica de búsqueda mejorada
    for db_cat, subproductos in db_mock.items():
        # Comprobar si la categoría sugerida encaja con la base de datos
        if db_cat in cat or cat in db_cat or cat == "":
            
            coincidencia_especifica = False
            # 1. Buscamos si el usuario pidió una variante específica (ej: "gaming")
            for db_prod, stock in subproductos.items():
                if db_prod in prod or prod in db_prod:
                    resultados.append(f"{db_prod} ({stock} unidades)")
                    coincidencia_especifica = True
                    
            # 2. Si el producto es genérico (ej: "un portátil") y no hubo coincidencia específica, devolvemos todo el catálogo de esa categoría
            if not coincidencia_especifica and (db_cat in prod or prod in db_cat or prod in ["", "cualquiera", "todo"]):
                for db_prod, stock in subproductos.items():
                    resultados.append(f"{db_prod} ({stock} unidades)")

    if resultados:
        return "Actualmente disponemos de lo siguiente: " + ", ".join(resultados)
        
    return f"No hay stock disponible o no reconocemos el producto específico '{producto}' en la categoría '{categoria}'."


# ====================================================================
# 2. Definición de la Herramienta (Esquema de Tools)
# ====================================================================
# Definimos el esquema de nuestra función de forma explícita usando types.Tool
herramienta_stock = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="consultar_stock",
            description="Consulta la base de datos de inventario para saber el stock de un producto.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "producto": types.Schema(
                        type="STRING", 
                        description="El nombre o descripción del producto a buscar. Ej: 'portátiles de gama alta', 'iPhone 15'"
                    ),
                    "categoria": types.Schema(
                        type="STRING", 
                        description="La categoría del producto. Ej: 'portatiles', 'smartphones', 'accesorios'"
                    ),
                },
                required=["producto", "categoria"],
            ),
        )
    ]
)


# ====================================================================
# 3. System Prompt y Configuración
# ====================================================================
config = types.GenerateContentConfig(
    system_instruction=(
        "Eres el asistente virtual de una tienda de electrónica. "
        "Usa las herramientas disponibles para consultar el stock antes de responder. "
        "Sé natural, amable y no reveles al usuario tu estructura interna."
    ),
    tools=[herramienta_stock],
    temperature=0.3, # Temperatura baja para que el chatbot sea más determinista
)


# ====================================================================
# 4. El Bucle Principal
# ====================================================================
def principal():
    modelo = 'gemini-2.5-flash'
    print("====================================================================")
    print("💬 Chatbot iniciado. Escribe 'quit', 'salir' o 'exit' para terminar.")
    print("====================================================================\n")
    
    # Inicializamos un historial vacío. Se irá llenando en cada vuelta del bucle.
    # En Function Calling, el JSON completo de la conversación es vital.
    historial = []
    
    while True:
        try:
            # Recibimos el input del usuario en la consola
            mensaje_usuario = input("\nUsuario: ")
        except (KeyboardInterrupt, EOFError):
            print("\nSaliendo...")
            break
            
        # Comandos para salir del bucle
        if mensaje_usuario.lower().strip() in ['quit', 'salir', 'exit']:
            print("Chat finalizado. ¡Hasta luego!")
            break
            
        # Evitamos mandar mensajes vacíos
        if not mensaje_usuario.strip():
            continue
            
        # 0. Añadimos la pregunta del usuario al historial
        historial.append(types.Content(role="user", parts=[types.Part.from_text(text=mensaje_usuario)]))
        
        # PRIMERA LLAMADA: Revisar si necesita herramientas para esta interacción
        response = client.models.generate_content(
            model=modelo,
            contents=historial,
            config=config
        )
        
        # Si detecta 'function_calls', el modelo quiere herramientas
        if response.function_calls:
            # 1. Guardamos la "intención" de llamar a la función en el historial
            historial.append(response.candidates[0].content)
            
            # 2. Ejecutamos la/las funciones en nuestro backend
            for function_call in response.function_calls:
                
                if function_call.name == "consultar_stock":
                    args = function_call.args
                    prod_arg = args.get("producto", "")
                    cat_arg = args.get("categoria", "")
                    
                    resultado_local = consultar_stock(prod_arg, cat_arg)
                    print(f"  [Servidor] Resultado extraído de la BD: {resultado_local}")
                    
                    # 3. Empaquetamos el resultado local y lo subimos al historial
                    respuesta_herramienta = types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name="consultar_stock",
                                response={"resultado": resultado_local}
                            )
                        ]
                    )
                    historial.append(respuesta_herramienta)
                    
            # SEGUNDA LLAMADA: Evaluamos todo el contexto y el resultado de la función
            response_final = client.models.generate_content(
                model=modelo,
                contents=historial,
                config=config
            )
            
            print(f"\nAsistente: {response_final.text}")
            
            # Guardamos la respuesta final en lenguaje natural del bot
            historial.append(response_final.candidates[0].content)
            
        else:
            # Si no usó herramientas, responde directamente
            print(f"\nAsistente: {response.text}")
            
            # Guardamos la respuesta del bot en el historial para contexto futuro
            historial.append(response.candidates[0].content)

if __name__ == "__main__":
    principal()
