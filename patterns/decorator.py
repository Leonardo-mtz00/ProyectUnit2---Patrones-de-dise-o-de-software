from abc import abstractmethod
from ai.assistant import AsistenteIA


# ---------------------------------------------------------------------------
# Decorator base
# ---------------------------------------------------------------------------

class DecoratorAsistente(AsistenteIA):
    """
    Decorator base: envuelve cualquier AsistenteIA
    y delega la llamada agregando comportamiento extra.
    """
    def __init__(self, asistente: AsistenteIA):
        self._asistente = asistente

    @abstractmethod
    def analizar(self, codigo: str) -> str:
        pass


# ---------------------------------------------------------------------------
# Decorator 1: Detección de Code Smells
# ---------------------------------------------------------------------------

class DecoratorCodeSmells(DecoratorAsistente):
    """
    Agrega al prompt instrucciones para detectar malos olores de código.
    """
    def analizar(self, codigo: str) -> str:
        print("🔍 [Decorator] Analizando code smells...")
        prompt = f"""Eres un experto en calidad de software.
Analiza el siguiente código Python y detecta CODE SMELLS.
Para cada problema encontrado indica:
- Tipo de smell (ej: función muy larga, nombre poco descriptivo, etc.)
- Línea aproximada
- Cómo corregirlo

Código:
{codigo}

Responde en español, de forma clara y concisa."""

        # Llama al asistente envuelto con el prompt enriquecido
        from ai.assistant import AsistenteClaudeBase
        from anthropic import Anthropic
        import os
        from dotenv import load_dotenv
        load_dotenv()

        cliente = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        respuesta = cliente.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return f"[CODE SMELLS]\n{respuesta.content[0].text}"


# ---------------------------------------------------------------------------
# Decorator 2: Generación de Pruebas Unitarias
# ---------------------------------------------------------------------------

class DecoratorGenerarTests(DecoratorAsistente):
    """
    Agrega al análisis la generación de pruebas unitarias.
    """
    def analizar(self, codigo: str) -> str:
        # Primero ejecuta el decorator anterior
        resultado_previo = self._asistente.analizar(codigo)

        print("🧪 [Decorator] Generando pruebas unitarias...")
        from anthropic import Anthropic
        import os
        from dotenv import load_dotenv
        load_dotenv()

        prompt = f"""Eres un experto en testing de software.
Genera pruebas unitarias con unittest para el siguiente código Python.
Incluye casos de prueba para:
- Casos normales
- Casos extremos (edge cases)
- Casos de error

Código:
{codigo}

Responde solo con el código de las pruebas, listo para ejecutarse."""

        cliente = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        respuesta = cliente.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        tests = respuesta.content[0].text
        return f"{resultado_previo}\n\n[PRUEBAS UNITARIAS]\n{tests}"


# ---------------------------------------------------------------------------
# Decorator 3: Coherencia Arquitectónica
# ---------------------------------------------------------------------------

class DecoratorCoherencia(DecoratorAsistente):
    """
    Verifica que el código sea coherente con la arquitectura general.
    """
    def __init__(self, asistente: AsistenteIA, contexto_proyecto: str = ""):
        super().__init__(asistente)
        self._contexto = contexto_proyecto

    def analizar(self, codigo: str) -> str:
        resultado_previo = self._asistente.analizar(codigo)

        print("🏗️  [Decorator] Verificando coherencia arquitectónica...")
        from anthropic import Anthropic
        import os
        from dotenv import load_dotenv
        load_dotenv()

        prompt = f"""Eres un arquitecto de software experto.
Contexto del proyecto: {self._contexto or 'Editor colaborativo de código en Python usando patrones de diseño.'}

Revisa si el siguiente código es coherente con ese contexto arquitectónico:
- ¿Respeta la separación de responsabilidades?
- ¿Hay dependencias incorrectas?
- ¿Sugiere algún patrón de diseño que debería aplicarse?

Código:
{codigo}

Responde en español con observaciones puntuales."""

        cliente = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        respuesta = cliente.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        coherencia = respuesta.content[0].text
        return f"{resultado_previo}\n\n[COHERENCIA ARQUITECTÓNICA]\n{coherencia}"