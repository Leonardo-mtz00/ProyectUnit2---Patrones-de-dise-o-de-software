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