from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import re



@dataclass(frozen=True) # Inmutable para asegurar que el estado compartido no cambie

# Flyweight: representa un token de código con su estilo visual.
class TokenEstilo:
    """
    Flyweight: define el estilo visual de un tipo de token.
    Es inmutable y compartido entre todas las instancias del mismo tipo.
    """
    tipo: str        # "keyword", "string", "comment", "number", "default"
    color: str       # color hex para el frontend
    negrita: bool = False

    def __repr__(self):
        return f"TokenEstilo({self.tipo}, {self.color})"
    
# Flyweight Factory: administra la creación y el almacenamiento de los estilos de token.
# se asegura de que solo exista un objeto TokenEstilo por tipo, compartiéndolo entre todos los tokens del mismo tipo.

class TokenEstiloFactory:
    """
    Fábrica de Flyweights.
    Garantiza que solo exista UN objeto por tipo de token.
    """
    _estilos: Dict[str, TokenEstilo] = {}

    # Estilos predefinidos por tipo
    _ESTILOS_DEFAULT = {
        "keyword":  TokenEstilo("keyword",  "#569CD6", negrita=True),
        "string":   TokenEstilo("string",   "#CE9178"),
        "comment":  TokenEstilo("comment",  "#6A9955"),
        "number":   TokenEstilo("number",   "#B5CEA8"),
        "default":  TokenEstilo("default",  "#D4D4D4"),
        "builtin":  TokenEstilo("builtin",  "#4EC9B0"),
    }

    @classmethod
    def obtener(cls, tipo: str) -> TokenEstilo:
        """Retorna el Flyweight existente o lo crea si no existe."""
        if tipo not in cls._estilos:
            cls._estilos[tipo] = cls._ESTILOS_DEFAULT.get(
                tipo, cls._ESTILOS_DEFAULT["default"]
            )
        return cls._estilos[tipo]

    @classmethod
    def total_estilos_en_memoria(cls) -> int:
        return len(cls._estilos)