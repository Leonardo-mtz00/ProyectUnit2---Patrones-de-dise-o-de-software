## Proyecto Unidad 2 ##

# Integrantes:
# Francisco Alejandro Gaona Romero
# Leonardo Martinez Gomez 

# -----------------------------------------------------------------------------------------------------------

import json
from core.orchestrator import Orchestrator   # Importa la clase Orchestrator


# Función para cargar el workflow desde un archivo JSON
def cargar_workflow(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def main():
    # 1. Cargar el workflow desde archivo
    workflow_data = cargar_workflow("workflow/backup_diario.json")

    # 2. Crear instancia del Orchestrator
    orchestrator = Orchestrator(workflow_data)

    # 3. Ejecutar el workflow
    orchestrator.run()


if __name__ == "__main__":
    main()
