from mcp.server.fastmcp import FastMCP

# Creamos nuestro propio servidor MCP
# FastMCP es un wrapper ligero que viene incluido en el SDK oficial
mcp = FastMCP("Gestor_de_Tareas")

# Un "estado" en memoria muy simple para guardar nuestras tareas
lista_tareas = []

# Exponemos funciones como herramientas usando el decorador @mcp.tool()
# El docstring ("""...""") es fundamental, ya que es la descripción que leerá la IA para entender qué hace.
@mcp.tool()
def add_task(description: str) -> str:
    """Añade una nueva tarea a la lista de tareas pendientes del usuario."""
    lista_tareas.append(description)
    return f"¡Hecho! Tarea añadida satisfactoriamente: '{description}'"

@mcp.tool()
def list_tasks() -> str:
    """Devuelve la lista actual en formato texto de todas las tareas pendientes."""
    if not lista_tareas:
        return "No hay ninguna tarea pendiente en el sistema."
    
    resultado = "Estas son las tareas pendientes actuales:\n"
    for idx, tarea in enumerate(lista_tareas, 1):
        resultado += f"{idx}. {tarea}\n"
    return resultado

if __name__ == "__main__":
    # Arrancamos el servidor usando la entrada/salida estándar (stdio)
    # Esta es la forma más común en que los clientes MCP se comunican localmente
    mcp.run(transport='stdio')
