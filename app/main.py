from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.routes.ChatBotRoutes import router as farmer_route  
from app.routes.YeildPrediction import router as yeidlPrediction
from app.database.chatbot_database import init_db
from app.index.chatbot_index import run_conversation_stream
from app.routes.CropPrediction import router as CropPrediction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(farmer_route)
app.include_router(yeidlPrediction)
app.include_router(CropPrediction)

@app.websocket("/ws/{user_id}/{session_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, session_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await run_conversation_stream(user_id, session_id, data, websocket)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for {user_id}-{session_id}")
