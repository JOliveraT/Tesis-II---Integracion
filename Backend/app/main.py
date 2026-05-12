from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import supabase

from app.routers import (
    raffles,
    participants,
    messages,
    scoring,
    winner,
    redemptions,
    twitch_auth,
    auth
)

app = FastAPI(
    title="Backend - Sorteos Twitch con IA",
    version="0.1.0",
)

# CORS: frontend local + subdominios temporales de ngrok
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https://.*\.ngrok-free\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "*"],
)

app.include_router(raffles.router)
app.include_router(participants.router)
app.include_router(messages.router)
app.include_router(scoring.router)
app.include_router(winner.router)
app.include_router(redemptions.router)
app.include_router(twitch_auth.router)
app.include_router(auth.router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend funcionando correctamente"
    }


@app.get("/db-test")
def db_test():
    response = supabase.table("raffles").select("*").limit(1).execute()
    return {
        "message": "Conexión con Supabase correcta",
        "data": response.data
    }
