from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from patterns.mediator import EditorColaborativoMediator, Usuario
from patterns.decorator import (
    DecoratorCodeSmells,
    DecoratorGenerarTests,
    DecoratorCoherencia
)
from ai.assistant import AsistenteClaudeBase
import json

app = FastAPI(title="Editor Colaborativo")

# ---------------------------------------------------------------------------
# Estado global del servidor
# ---------------------------------------------------------------------------

mediator = EditorColaborativoMediator()
conexiones_activas: dict[str, WebSocket] = {}  # user_id → websocket


# ---------------------------------------------------------------------------
# WebSocket Manager — maneja conexiones y broadcast
# ---------------------------------------------------------------------------

class WebSocketManager:
    def __init__(self):
        self._conexiones: dict[str, WebSocket] = {}

    async def conectar(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self._conexiones[user_id] = websocket

    def desconectar(self, user_id: str):
        self._conexiones.pop(user_id, None)

    async def enviar_a(self, user_id: str, mensaje: dict):
        ws = self._conexiones.get(user_id)
        if ws:
            await ws.send_text(json.dumps(mensaje))

    async def broadcast(self, mensaje: dict, excluir: str = None):
        """Manda mensaje a todos menos al excluido."""
        for uid, ws in self._conexiones.items():
            if uid != excluir:
                await ws.send_text(json.dumps(mensaje))

    def total_conectados(self) -> int:
        return len(self._conexiones)


ws_manager = WebSocketManager()


# ---------------------------------------------------------------------------
# Rutas HTTP
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return {"mensaje": "Editor Colaborativo activo 🚀"}


@app.get("/status")
async def status():
    return {
        "usuarios_conectados": ws_manager.total_conectados(),
        "estado": "activo"
    }


# ---------------------------------------------------------------------------
# WebSocket — conexión principal del editor
# ---------------------------------------------------------------------------

@app.websocket("/ws/{user_id}")
async def websocket_editor(websocket: WebSocket, user_id: str):
    # Conectar usuario
    await ws_manager.conectar(user_id, websocket)

    usuario = Usuario(user_id, user_id)
    mediator.conectar_usuario(usuario)

    # Notificar a todos que alguien entró
    await ws_manager.broadcast({
        "tipo": "usuario_conectado",
        "usuario": user_id,
        "total": ws_manager.total_conectados()
    })

    try:
        while True:
            # Esperar mensajes del cliente
            data = await websocket.receive_text()
            mensaje = json.loads(data)
            tipo = mensaje.get("tipo")

            # --- El usuario editó código ---
            if tipo == "edicion":
                contenido = mensaje.get("contenido", "")
                linea = mensaje.get("linea", 0)

                # Broadcast a los demás usuarios
                await ws_manager.broadcast({
                    "tipo": "actualizacion",
                    "contenido": contenido,
                    "linea": linea,
                    "de": user_id
                }, excluir=user_id)

            # --- El usuario pide análisis de IA ---
            elif tipo == "analizar_ia":
                contenido = mensaje.get("contenido", "")

                # Armar stack de decorators
                asistente = AsistenteClaudeBase()
                asistente = DecoratorCodeSmells(asistente)
                asistente = DecoratorGenerarTests(asistente)
                asistente = DecoratorCoherencia(
                    asistente,
                    contexto_proyecto="Editor colaborativo de código en Python"
                )

                # Analizar y devolver resultado solo al que pidió
                resultado = asistente.analizar(contenido)
                await ws_manager.enviar_a(user_id, {
                    "tipo": "resultado_ia",
                    "resultado": resultado
                })

            # --- Undo ---
            elif tipo == "undo":
                contenido = mediator._gestor_historial.undo()
                if contenido:
                    await ws_manager.enviar_a(user_id, {
                        "tipo": "actualizacion",
                        "contenido": contenido,
                        "de": "historial"
                    })

            # --- Redo ---
            elif tipo == "redo":
                contenido = mediator._gestor_historial.redo()
                if contenido:
                    await ws_manager.enviar_a(user_id, {
                        "tipo": "actualizacion",
                        "contenido": contenido,
                        "de": "historial"
                    })

    except WebSocketDisconnect:
        ws_manager.desconectar(user_id)
        mediator.desconectar_usuario(user_id)
        await ws_manager.broadcast({
            "tipo": "usuario_desconectado",
            "usuario": user_id,
            "total": ws_manager.total_conectados()
        })

        # Al final del archivo, antes del último bloque
from fastapi.staticfiles import StaticFiles

app.mount("/editor", StaticFiles(directory="frontend", html=True), name="frontend")