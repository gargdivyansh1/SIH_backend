from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# from app.routes.ChatBotRoutes import router as farmer_route  

from app.routes.YieldPrediction import router as YeidlPrediction
from app.routes.authRoutes import router as AuthRouter
from app.routes.Feedbacks import router as FeedbackRouter
from app.routes.Notifications import router as NotificationRouter
from app.routes.user import router as UserRouter
# from app.database.chatbot_database import init_db
# from app.index.chatbot_index import run_conversation_stream
from app.routes.CropPrediction import router as CropPrediction
from app.routes.CropGuidance import router as CropGuidance

app = FastAPI(
    title="KisanMitra",
    description="Backend for KisanMitra",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# init_db()

# app.include_router(farmer_route)
app.include_router(YeidlPrediction)

app.include_router(CropPrediction)

app.include_router(AuthRouter)

app.include_router(NotificationRouter)

app.include_router(UserRouter)

app.include_router(FeedbackRouter)

app.include_router(CropGuidance)

# @app.websocket("/ws/{user_id}/{session_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: str, session_id: str):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await run_conversation_stream(user_id, session_id, data, websocket)
#     except WebSocketDisconnect:
#         print(f"WebSocket disconnected for {user_id}-{session_id}")
