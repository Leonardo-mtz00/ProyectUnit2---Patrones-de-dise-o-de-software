from abc import ABC, abstractmethod
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Interfaz base del Asistente
# ---------------------------------------------------------------------------

class AsistenteIA(ABC):
    """Interfaz base que todos los Decorators respetan."""
    @abstractmethod
    def analizar(self, codigo: str) -> str:
        pass


# ---------------------------------------------------------------------------
# Asistente concreto base — hace la llamada real a la API
# ---------------------------------------------------------------------------

class AsistenteClaudeBase(AsistenteIA):
    """
    Componente base: llama a la API de Anthropic.
    No sabe nada de code smells, tests, ni arquitectura.
    Solo manda el código y recibe respuesta.
    """
    def __init__(self):
        self._cliente = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self._modelo = "claude-sonnet-4-20250514"

    def analizar(self, codigo: str) -> str:
        mensaje = self._cliente.messages.create(
            model=self._modelo,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"Analiza este código Python:\n\n{codigo}"
            }]
        )
        return mensaje.content[0].text