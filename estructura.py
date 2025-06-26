from pathlib import Path

def listar_directorio(path, prefijo="", nivel=0, max_nivel=2):
    if nivel > max_nivel:
        return
    for item in sorted(path.iterdir()):
        if item.name in ["__pycache__", "env", ".git", "node_modules", ".vscode"]:
            continue
        print(f"{prefijo}|-- {item.name}")
        if item.is_dir():
            listar_directorio(item, prefijo + "|   ", nivel + 1, max_nivel)

if __name__ == "__main__":
    print("gestor-tareas-python-2")
    listar_directorio(Path("."), max_nivel=2)
