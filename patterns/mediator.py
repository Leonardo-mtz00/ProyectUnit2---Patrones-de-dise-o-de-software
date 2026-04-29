from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List
from datetime import datetime

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


class GestorHistorial(Componente): # aqui se apoya en Memento para guardar el historial de cambios
    """Escucha cambios y guarda snapshots (se apoya en Memento)."""
    def __init__(self):
        super().__init__()
        from patterns.memento import HistorialDocumento # Importamos aquí para evitar dependencias circulares
        from editor.document import CodeDocument # Importamos aquí para evitar dependencias circulares
        self._doc = CodeDocument("sesion_colaborativa") # Creamos un documento específico para esta sesión de colaboración
        self._historial = HistorialDocumento() # Creamos un historial específico para esta sesión de colaboración

    def registrar_cambio(self, contenido: str, linea: int, col: int):
        self._doc.escribir(contenido, linea, col)
        self._historial.guardar(self._doc.guardar_estado()) # Guardamos el estado actual del documento en el historial
        print(f"💾 Historial: {len(self._historial._historial)} estados guardados.") # Aqui se imprime el historial

    def undo(self):
        memento = self._historial.undo()
        if memento:
            self._doc.restaurar_estado(memento)
            return self._doc.obtener_contenido()
        return None

    def redo(self):
        memento = self._historial.redo()
        if memento:
            self._doc.restaurar_estado(memento)
            return self._doc.obtener_contenido()
        return None

# Clase Mediator concreto

class EditorColaborativoMediator(EditorMediator):

    def __init__(self):
        self._usuarios: Dict[str, Usuario] = {}
        self._gestor_doc = GestorDocumento()
        self._gestor_historial = GestorHistorial()
        self._asistente_ia = None  # Lo conectamos en el commit 4

        # Registrar componentes
        self._gestor_doc.set_mediator(self) # El GestorDocumento necesita notificar al Mediator cuando se actualice el documento
        self._gestor_historial.set_mediator(self) # El GestorHistorial necesita notificar al Mediator cuando se registre un cambio para que pueda notificar a los usuarios

    def conectar_usuario(self, usuario: Usuario):
        usuario.set_mediator(self)
        self._usuarios[usuario.user_id] = usuario
        print(f"🟢🟢🟢 {usuario.nombre} se conectó. "
              f"Usuarios activos: {len(self._usuarios)}")

    def desconectar_usuario(self, user_id: str):
        if user_id in self._usuarios:
            nombre = self._usuarios[user_id].nombre
            del self._usuarios[user_id]
            print(f"🔴🔴🔴 {nombre} se desconectó.")