from patterns.mediator import (
    EditorColaborativoMediator, Usuario
)

# Crear mediator y usuarios
mediator = EditorColaborativoMediator()

ana   = Usuario("u1", "Ana")
carlos = Usuario("u2", "Carlos")
luis  = Usuario("u3", "Luis")

# Conectar usuarios
mediator.conectar_usuario(ana)
mediator.conectar_usuario(carlos)
mediator.conectar_usuario(luis)

print("\n--- Ana edita ---")
ana.editar("def suma(a, b):\n    return a + b", linea=1)

print("\n--- Carlos edita ---")
carlos.editar("def suma(a, b):\n    return a + b + 0", linea=2)

print("\n--- Luis pide análisis de IA ---")
luis.solicitar_analisis_ia()

print("\n--- Carlos se desconecta ---")
mediator.desconectar_usuario("u2")


# Probando flyweight

from patterns.flyweight import TokenizadorPython, TokenEstiloFactory

codigo = """\
def suma(a, b):
    # Suma dos números
    return a + b

class Calculadora:
    def __init__(self):
        self.historial = []

    def operar(self, a, b):
        resultado = suma(a, b)
        print(resultado)
        return resultado
"""

tokenizador = TokenizadorPython()
tokens = tokenizador.tokenizar(codigo)

print(f"Total de tokens: {len(tokens)}")
print(f"Estilos únicos en memoria (Flyweights): "
      f"{TokenEstiloFactory.total_estilos_en_memoria()}\n")

# Mostrar algunos tokens
for t in tokens[:20]:
    print(t)

# Demostrar que los Flyweights se comparten (misma referencia)
print("\n--- Verificando que los Flyweights se comparten ---")
t1 = next(t for t in tokens if t.estilo.tipo == "keyword")
t2 = next(t for t in reversed(tokens) if t.estilo.tipo == "keyword")
print(f"Token 1: {t1.valor!r} → estilo id: {id(t1.estilo)}")
print(f"Token 2: {t2.valor!r} → estilo id: {id(t2.estilo)}")
print(f"¿Mismo objeto en memoria? {t1.estilo is t2.estilo}")


# Prueba de Decorators

from ai.assistant import AsistenteClaudeBase
from patterns.decorator import (
    DecoratorCodeSmells,
    DecoratorGenerarTests,
    DecoratorCoherencia
)

# Código de ejemplo a analizar
codigo_prueba = """\
def c(a,b):
    x = a+b
    y = a-b
    z = a*b
    w = a/b
    print(x)
    print(y)
    print(z)
    print(w)
    return x
"""

print("=" * 60)
print("Construyendo el stack de Decorators...")
print("=" * 60)

# Así se apilan los Decorators, de adentro hacia afuera:
asistente = AsistenteClaudeBase()
asistente = DecoratorCodeSmells(asistente)
asistente = DecoratorGenerarTests(asistente)
asistente = DecoratorCoherencia(asistente, contexto_proyecto="Editor colaborativo de código")

print("\n🚀 Ejecutando análisis completo...\n")
resultado = asistente.analizar(codigo_prueba)

print("\n" + "=" * 60)
print(resultado)