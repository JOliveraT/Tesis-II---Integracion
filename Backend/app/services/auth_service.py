from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Header, HTTPException

from app.config import settings
from app.database import supabase

JWT_ALGORITHM = "HS256"
TOKEN_TTL_HOURS = 24
USERS_TABLE = "users"


def _jwt_secret() -> str:
    secret = settings.supabase_service_role_key
    if not secret:
        raise HTTPException(status_code=500, detail="JWT secret no configurado")
    return secret


def _create_token(user: dict) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user["id"]),
        "email": user["email"],
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=TOKEN_TTL_HOURS)).timestamp()),
    }
    return jwt.encode(payload, _jwt_secret(), algorithm=JWT_ALGORITHM)


def _to_user_payload(user: dict) -> dict:
    return {
        "id": str(user.get("id")),
        "email": user.get("email"),
        "display_name": user.get("display_name") or "",
        "created_at": user.get("created_at"),
    }


def signup(*, email: str, display_name: str) -> dict:
    existing = supabase.table(USERS_TABLE).select("id").eq("email", email).limit(1).execute()
    if existing.data:
        raise HTTPException(status_code=409, detail="El usuario ya existe")

    created = (
        supabase.table(USERS_TABLE)
        .insert({"email": email, "display_name": display_name})
        .execute()
    )
    if not created.data:
        raise HTTPException(status_code=500, detail="No se pudo crear el usuario")

    user = created.data[0]
    return {"user": _to_user_payload(user), "token": _create_token(user)}


def login(*, email: str) -> dict:
    result = (
        supabase.table(USERS_TABLE)
        .select("id,email,display_name,created_at")
        .eq("email", email)
        .limit(1)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    user = result.data[0]
    return {"user": _to_user_payload(user), "token": _create_token(user)}


def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Token faltante")

    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, _jwt_secret(), algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")

    result = (
        supabase.table(USERS_TABLE)
        .select("id,email,display_name,created_at")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return _to_user_payload(result.data[0])
