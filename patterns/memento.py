from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class DocumentMemento:
    """
    Memento: guarda un snapshot inmutable del documento.
    Solo el Originator (CodeDocument) debería crear/leer esto.
    """
    contenido: str
    cursor_linea: int
    cursor_col: int
    timestamp: datetime = field(default_factory=datetime.now)

    def __repr__(self):
        return (f"Memento(línea={self.cursor_linea}, "
                f"col={self.cursor_col}, "
                f"tiempo={self.timestamp.strftime('%H:%M:%S')})")


class HistorialDocumento:
    """
    Caretaker: administra los Mementos sin conocer su contenido interno.
    Maneja el undo/redo de un documento.
    """
    def __init__(self, max_estados: int = 50):
        self._historial: List[DocumentMemento] = []
        self._pos_actual: int = -1
        self._max_estados = max_estados

    def guardar(self, memento: DocumentMemento):
        """Guarda un nuevo estado, descartando el futuro si estamos en medio del historial."""
        # Si hicimos undo y luego escribimos, borramos el "futuro"
        if self._pos_actual < len(self._historial) - 1:
            self._historial = self._historial[:self._pos_actual + 1]

        self._historial.append(memento)

        # Limitar tamaño del historial
        if len(self._historial) > self._max_estados:
            self._historial.pop(0)

        self._pos_actual = len(self._historial) - 1

    def undo(self) -> DocumentMemento | None:
        """Regresa al estado anterior."""
        if self._pos_actual <= 0:
            print("No hay más estados para deshacer.")
            return None
        self._pos_actual -= 1
        return self._historial[self._pos_actual]

    def redo(self) -> DocumentMemento | None:
        """Avanza al estado siguiente."""
        if self._pos_actual >= len(self._historial) - 1:
            print("No hay más estados para rehacer.")
            return None
        self._pos_actual += 1
        return self._historial[self._pos_actual]

    def puede_undo(self) -> bool:
        return self._pos_actual > 0

    def puede_redo(self) -> bool:
        return self._pos_actual < len(self._historial) - 1

    def resumen(self):
        print(f"Historial: {len(self._historial)} estados, posición actual: {self._pos_actual}")
        for i, m in enumerate(self._historial):
            marcador = "◄ actual" if i == self._pos_actual else ""
            print(f"  [{i}] {m} {marcador}")