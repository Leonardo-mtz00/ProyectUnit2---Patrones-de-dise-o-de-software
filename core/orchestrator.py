class Orchestrator:
    def __init__(self, workflow_data):
        self.workflow_data = workflow_data

    def run(self):
        print("Ejecutando workflow:", self.workflow_data.get("name", "Sin nombre"))
