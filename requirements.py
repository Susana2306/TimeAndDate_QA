import subprocess
import sys
import importlib

# Lista de dependencias requeridas y sus nombres de importación para verificar si ya están instaladas.
# El formato es: {"nombre_pip": "nombre_importable"}
REQUIRED_PACKAGES = {
    "behave": "behave",
    "selenium": "selenium",
    "webdriver-manager": "webdriver_manager",
    "behave-html-formatter": "behave_html_formatter"
}

def check_and_install():
    print("=" * 60)
    print(" Verificando dependencias para timeanddate_escenarios...")
    print("=" * 60)
    
    missing_packages = []
    
    for pip_name, module_name in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(module_name)
            print(f"[OK] {pip_name} ya está instalado.")
        except ImportError:
            print(f"[X] {pip_name} no está instalado.")
            missing_packages.append(pip_name)
            
    if not missing_packages:
        print("\n¡Todas las dependencias están instaladas y listas para usar! 🎉")
        print("Puedes ejecutar los escenarios usando el comando: behave")
        print("=" * 60)
        return

    print(f"\nSe encontraron {len(missing_packages)} dependencias faltantes: {', '.join(missing_packages)}")
    print("Instalando dependencias automáticamente...\n")
    
    for package in missing_packages:
        print(f"Instalando {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"[OK] {package} se instaló correctamente.\n")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] No se pudo instalar {package}. Detalle: {e}")
            sys.exit(1)
            
    print("=" * 60)
    print("¡Todas las dependencias han sido instaladas con éxito! 🎉")
    print("Puedes ejecutar los escenarios usando el comando: behave")
    print("=" * 60)

if __name__ == "__main__":
    check_and_install()
