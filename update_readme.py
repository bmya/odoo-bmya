import os
from ast import literal_eval


def get_modules_info(root_dir):
    """
    Recorre el directorio raíz y extrae información de los módulos desde los archivos __manifest__.py.
    """
    modules_info = {}
    for dirpath, _, filenames in os.walk(root_dir):
        if "__manifest__.py" in filenames:
            manifest_path = os.path.join(dirpath, "__manifest__.py")
            with open(manifest_path, "r", encoding="utf-8") as f:
                content = f.read()
                try:
                    manifest = literal_eval(content)
                    module_name = manifest.get("name_technical", os.path.basename(dirpath))
                    version = manifest.get("version", "N/A")
                    # Usar "summary" en lugar de "description"
                    summary = manifest.get("summary", "")
                    installable = manifest.get("installable", True)
                    if not installable:
                        version = "No Disponible"
                    modules_info[module_name] = {
                        "description": summary.strip(),  # Asignar summary a la clave "description"
                        "version": version
                    }
                except (SyntaxError, ValueError) as e:
                    print(f"Error parsing {manifest_path}: {e}")
    return modules_info

def update_readme(modules_info):
    """
    Actualiza la tabla en el README.md con la información de los módulos.
    Si encuentra la tabla existente, la reemplaza; si no, añade una nueva al final.
    """
    # Crear la tabla en Markdown
    header = "| Descripción | Nombre Técnico | Última Versión |\n|-------------|----------------|----------------|\n"
    rows = []
    for name, info in sorted(modules_info.items()):
        rows.append(f"| {info['description']} | {name} | {info['version']} |")

    table_content = header + "\n".join(rows)

    # Leer el contenido actual del README.md
    with open("README.md", "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Buscar la tabla existente usando el marcador
    start_marker = "| Descripción | Nombre Técnico | Última Versión |"
    if start_marker in readme_content:
        start_idx = readme_content.index(start_marker)
        end_idx = readme_content.find("\n\n", start_idx)
        if end_idx == -1:
            end_idx = len(readme_content)
        new_content = readme_content[:start_idx] + table_content + readme_content[end_idx:]
    else:
        new_content = readme_content + "\n\n" + table_content

    # Escribir el nuevo contenido en README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    root_dir = "."  # Directorio raíz del repositorio
    modules_info = get_modules_info(root_dir)
    update_readme(modules_info)
