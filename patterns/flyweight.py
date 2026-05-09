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

# Cliente: representa un token específico en el documento, con su valor y posición.
# Cada Token tiene una referencia a un TokenEstilo compartido, evitando la duplicación de estilos en memoria.    
@dataclass
class Token:
    """
    Representa un token en el código.
    - valor y posición: estado extrínseco (único por token)
    - estilo: Flyweight compartido
    """
    valor: str
    linea: int
    col_inicio: int
    estilo: TokenEstilo   # referencia compartida, NO se duplica

    def __repr__(self):
        return (f"Token({self.valor!r}, "
                f"l={self.linea}, c={self.col_inicio}, "
                f"tipo={self.estilo.tipo})")
    
# Cliente: el tokenizador que recorre el código y genera Tokens usando los estilos compartidos de la fábrica.
# El tokenizador se encarga de identificar el tipo de cada fragmento de código (palabra clave, string, comentario, número, etc.) y asignarle el estilo correspondiente sin crear objetos de estilo duplicados.
#  

class TokenizadorPython:
    """
    Recorre el código y genera Tokens usando Flyweights para los estilos.
    """

    KEYWORDS = {
        "def", "class", "return", "if", "else", "elif", "for",
        "while", "import", "from", "as", "with", "try", "except",
        "finally", "pass", "break", "continue", "lambda", "yield",
        "True", "False", "None", "and", "or", "not", "in", "is"
    }

    BUILTINS = {
        "print", "len", "range", "type", "int", "str", "float",
        "list", "dict", "set", "tuple", "input", "open", "sum",
        "min", "max", "enumerate", "zip", "map", "filter"
    }

    # Patrones ordenados por prioridad
    PATRONES: List[Tuple[str, str]] = [
        ("comment",  r"#.*"),
        ("string",   r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|".*?"|\'.*?\''),
        ("number",   r"\b\d+(\.\d+)?\b"),
        ("word",     r"\b[a-zA-Z_]\w*\b"),
        ("default",  r"\S+"),
    ]

    def tokenizar(self, codigo: str) -> List[Token]:
        tokens: List[Token] = []
        fabrica = TokenEstiloFactory

        for num_linea, linea in enumerate(codigo.splitlines(), start=1):
            col = 0
            texto_restante = linea

            while texto_restante:
                # Saltar espacios
                espacio = re.match(r"\s+", texto_restante)
                if espacio:
                    col += espacio.end()
                    texto_restante = texto_restante[espacio.end():]
                    continue

                matched = False
                for tipo_patron, patron in self.PATRONES:
                    m = re.match(patron, texto_restante)
                    if m:
                        valor = m.group()

                        # Clasificar palabras como keyword, builtin o default
                        if tipo_patron == "word":
                            if valor in self.KEYWORDS:
                                tipo_final = "keyword"
                            elif valor in self.BUILTINS:
                                tipo_final = "builtin"
                            else:
                                tipo_final = "default"
                        else:
                            tipo_final = tipo_patron

                        estilo = fabrica.obtener(tipo_final)  # Flyweight
                        tokens.append(Token(valor, num_linea, col, estilo))

                        col += m.end()
                        texto_restante = texto_restante[m.end():]
                        matched = True
                        break

                if not matched:
                    col += 1
                    texto_restante = texto_restante[1:]

        return tokens