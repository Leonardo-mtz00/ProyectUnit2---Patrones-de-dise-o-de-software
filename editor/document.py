from patterns.memento import DocumentMemento

class CodeDocument:
    """
    Originator en el patrón Memento.
    Representa el documento de código que se está editando.
    """
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._contenido = ""
        self._cursor_linea = 0
        self._cursor_col = 0

    def escribir(self, contenido: str, linea: int = 0, col: int = 0):
        self._contenido = contenido
        self._cursor_linea = linea
        self._cursor_col = col

    def obtener_contenido(self) -> str:
        return self._contenido

    # --- Memento ---
    def guardar_estado(self) -> DocumentMemento:
        """Crea un snapshot del estado actual."""
        return DocumentMemento(
            contenido=self._contenido,
            cursor_linea=self._cursor_linea,
            cursor_col=self._cursor_col
        )

    def restaurar_estado(self, memento: DocumentMemento):
        """Restaura un snapshot previo."""
        self._contenido = memento.contenido
        self._cursor_linea = memento.cursor_linea
        self._cursor_col = memento.cursor_col

    def __str__(self):
        return f"[{self.nombre}] línea {self._cursor_linea}: {self._contenido[:50]}..."