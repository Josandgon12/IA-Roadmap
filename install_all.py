import os
import subprocess
import sys
import shutil
from pathlib import Path

def print_banner(text):
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def setup_project(project_path):
    project_name = project_path.name
    print_banner(f"Configurando Proyecto: {project_name}")
    
    # 1. Crear Entorno Virtual si no existe
    venv_path = project_path / "venv"
    if not venv_path.exists():
        print(f"[*] Creando entorno virtual en {venv_path}...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    else:
        print("[+] Entorno virtual ya existe.")

    # 2. Determinar ejecutable de pip
    if os.name == 'nt':  # Windows
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:  # Linux/Mac
        pip_exe = venv_path / "bin" / "pip"

    # 3. Instalar Requerimientos
    requirements_file = project_path / "requirements.txt"
    if requirements_file.exists():
        print(f"[*] Instalando dependencias desde {requirements_file.name}...")
        subprocess.run([str(pip_exe), "install", "-r", str(requirements_file)], check=True)
    else:
        print("[!] No se encontró requirements.txt, saltando instalación.")

    # 4. Configurar .env si existe .env.example
    env_example = project_path / ".env.example"
    env_file = project_path / ".env"
    if env_example.exists() and not env_file.exists():
        print(f"[*] Creando archivo .env a partir de .env.example...")
        shutil.copy(str(env_example), str(env_file))
        print(f"[!] RECUERDA: Edita {env_file} con tu propia API Key.")
    elif env_file.exists():
        print("[+] Archivo .env ya existe.")

def main():
    root_dir = Path(__file__).parent
    projects_found = 0

    print_banner("IA ROADMAP - INSTALADOR AUTOMÁTICO")
    print(f"Buscando subproyectos en: {root_dir}")

    # Lista de carpetas a ignorar
    ignore_dirs = {'.git', 'venv', '.venv', '__pycache__', 'Notebooks', 'chroma_db'}

    for item in root_dir.iterdir():
        if item.is_dir() and item.name not in ignore_dirs:
            # Si tiene un script python o un readme, lo tratamos como proyecto
            if any(item.glob("*.py")) or (item / "requirements.txt").exists():
                try:
                    setup_project(item)
                    projects_found += 1
                except Exception as e:
                    print(f"[ERROR] Error configurando {item.name}: {e}")

    print_banner("INSTALACIÓN FINALIZADA")
    if projects_found > 0:
        print(f"Se han configurado {projects_found} proyectos con éxito.")
        print("\nPróximos pasos:")
        print("1. Entra en la carpeta del proyecto que quieras usar.")
        print("2. Activa el entorno virtual (venv/Scripts/activate).")
        print("3. Asegúrate de poner tus API Keys en los archivos .env.")
    else:
        print("No se encontraron proyectos válidos para configurar.")

if __name__ == "__main__":
    main()
