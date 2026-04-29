from __future__ import annotations
from abc import ABC, abstractmethod

class Componente(ABC):
    """Todo lo que se comunica a través del Mediator."""
    def __init__(self, mediator: EditorMediator = None):
        self._mediator = mediator

    def set_mediator(self, mediator: EditorMediator): # Permite cambiar el Mediator después de la creación del Componente
        self._mediator = mediator # Asigna el Mediator al Componente

class EditorMediator(ABC): 
    """Interfaz del Mediator."""
    @abstractmethod
    def notificar(self, emisor: Componente, evento: str, datos: dict): # Método para notificar al Mediator sobre un evento ocurrido en un Componente
        pass

# ahora ocupamos los componentes concretos y el Mediator concreto

class Usuario (Componente):
    """Representa a un desarrollador conectado al editor."""
    def __init__(self, user_id: str, nombre: str):
        super().__init__()
        self.user_id = user_id
        self.nombre = nombre

    def editar(self, contenido: str, linea: int = 0, col: int = 0):
        """El usuario hace un cambio en el documento."""
        print(f"✏️  [{self.nombre}] editando línea {linea}...")
        self._mediator.notificar(self, "edicion", {
            "contenido": contenido,
            "linea": linea,
            "col": col
        })

    def solicitar_analisis_ia(self):
        """El usuario pide sugerencias al asistente de IA."""
        print(f"🤖 [{self.nombre}] solicita análisis de IA...")
        self._mediator.notificar(self, "solicitar_ia", {})

    def recibir_actualizacion(self, contenido: str, de_usuario: str):
        """Recibe cambios de otro usuario."""
        print(f"📥 [{self.nombre}] recibe cambio de {de_usuario}: "
              f"'{contenido[:40]}...'")


class GestorDocumento(Componente):
    """Administra el estado actual del documento compartido."""
    def __init__(self):
        super().__init__()
        self._contenido = ""
        self._ultima_edicion: datetime = None
        self._editor_actual: str = None

    def actualizar(self, contenido: str, usuario: str, linea: int, col: int):
        self._contenido = contenido
        self._ultima_edicion = datetime.now()
        self._editor_actual = usuario
        # Notifica al mediator que el documento cambió
        self._mediator.notificar(self, "documento_actualizado", {
            "contenido": contenido,
            "usuario": usuario,
            "linea": linea,
            "col": col
        })

    def obtener_contenido(self) -> str:
        return self._contenido
