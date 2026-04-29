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



