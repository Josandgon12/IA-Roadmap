import os
import sys
from dotenv import load_dotenv

# Dependencias de LangChain y Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 0. Cargar variables de entorno (como GOOGLE_API_KEY)
load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    print("❌ ERROR: No se encontró GOOGLE_API_KEY en el entorno. Por favor, añádela al archivo .env (y no a .env.example)")
    sys.exit(1)

def main():
    print("="*50)
    print("🤖 Iniciando Sistema RAG con Gemini Flash 🤖")
    print("="*50)
    
    # 1. LECTURA DE DOCUMENTOS
    print("\n📚 1. Cargando documentos desde la carpeta 'docs'...")
    # Buscamos todos los archivos .txt en la carpeta docs
    loader = DirectoryLoader('./docs', glob="**/*.txt", loader_cls=TextLoader)
    try:
        documentos = loader.load()
    except Exception as e:
        print(f"⚠️ Error al leer documentos: {e}")
        sys.exit(1)

    if not documentos:
        print("⚠️ No se encontraron documentos .txt en la carpeta 'docs'. ¡Añade algunos y vuelve a probar!")
        sys.exit(1)

    print(f"✅ Se cargaron {len(documentos)} documentos.")

    # 2. DIVISIÓN (CHUNKING)
    # Dividimos el texto en bloques de 1000 caracteres con 200 de solapamiento
    print("\n✂️ 2. Dividiendo el texto en fragmentos (chunks)...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documentos)
    print(f"✅ Los documentos se dividieron en {len(chunks)} fragmentos.")

    # 3. EMBEDDINGS Y BASE DE DATOS VECTORIAL
    print("\n🧠 3. Creando embeddings y guardándolos en ChromaDB...")
    # Usamos embeddings de Google (optimizados para integrarse con sus LLMs)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # Guardamos los fragmentos en ChromaDB localmente en la carpeta './chroma_db'
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="./chroma_db")
    
    # Configuramos el recuperador para que devuelva los 3 fragmentos más relevantes
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 4. PREPARAR EL MODELO (GEMINI FLASH)
    print("\n⚡ 4. Conectando con Gemini 2.5 Flash...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

    # Definimos las instrucciones (prompt) para la IA
    system_prompt = (
        "Eres un asistente útil que responde preguntas de forma clara y amable.\n"
        "Usa ÚNICAMENTE la siguiente información recuperada (contexto) para responder a la pregunta.\n"
        "Si la respuesta no está en el contexto, simplemente di que el documento no menciona nada al respecto, no inventes información.\n"
        "\nContexto:\n{context}"
    )

    # En caso de que quieras que el modelo use también su propio conocimiento
    # system_prompt = (
    # "Eres un asistente útil que responde preguntas de forma clara y amable.\n"
    # "Se te proporciona la siguiente información recuperada de documentos del usuario como contexto.\n"
    # "Si la pregunta está relacionada con el contexto, PRIORIZA esa información para responder.\n"
    # "Si la pregunta NO está relacionada con el contexto (por ejemplo, cálculos, preguntas generales, etc.), "
    # "responde usando tu propio conocimiento.\n"
    # "Cuando uses información del contexto, menciónalo. Cuando uses tu conocimiento general, indícalo también.\n"
    # "\nContexto:\n{context}"
    # )

    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # Función para formatear los documentos recuperados como texto
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Construimos la cadena (chain) de RAG con LCEL
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print("✅ Sistema RAG Listo.")

    # 5. BUCLE DE PREGUNTAS (CHAT)
    print("\n" + "="*50)
    print("🚀 ¡Ya puedes hacer preguntas sobre tus documentos! Escribe 'salir' para terminar.")
    print("="*50)

    while True:
        try:
            pregunta = input("\n🤔 Tu pregunta: ")
            if pregunta.lower() in ['salir', 'exit', 'quit']:
                print("\n¡Hasta luego!")
                break
                
            if not pregunta.strip():
                continue
                
            print("⏳ Buscando en los documentos y generando respuesta...")
            respuesta = rag_chain.invoke(pregunta)
            
            print("\n🤖 Respuesta de Gemini:")
            print(respuesta)
            
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break
        except Exception as e:
            print(f"\n❌ Ocurrió un error al procesar tu pregunta: {e}")

if __name__ == "__main__":
    main()
