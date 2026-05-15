from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import os

import jwt
from fastapi import Header, HTTPException

from app.config import settings
from app.database import supabase
from app.schemas.auth_schema import SignUpRequest

JWT_ALGORITHM = "HS256"
TOKEN_TTL_HOURS = 24
USERS_TABLE = "users"
PROFILES_TABLE = "user_profiles"


def _jwt_secret() -> str:
    secret = settings.supabase_service_role_key
    if not secret:
        raise HTTPException(status_code=500, detail="JWT secret no configurado")
    return secret


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return base64.b64encode(salt + key).decode('utf-8')


def _verify_password(password: str, password_hash: str) -> bool:
    raw = base64.b64decode(password_hash.encode('utf-8'))
    salt, stored = raw[:16], raw[16:]
    check = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return hmac.compare_digest(check, stored)


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


def signup(*, data: SignUpRequest) -> dict:
    if data.password != data.password_confirmation:
        raise HTTPException(status_code=409, detail='Las contraseñas no coinciden')

    for field, value, msg in [
      ('email', data.email, 'El correo ya está registrado'),
      ('nickname', data.nickname, 'El nickname ya está en uso'),
      ('phone', data.phone, 'El teléfono ya está registrado')
    ]:
      table = USERS_TABLE if field == 'email' else PROFILES_TABLE
      result = supabase.table(table).select('id' if table == USERS_TABLE else 'user_id').eq(field, value).limit(1).execute()
      if result.data:
        raise HTTPException(status_code=409, detail=msg)

    display_name = data.nickname
    user_created = supabase.table(USERS_TABLE).insert({
      'email': data.email,
      'display_name': display_name,
      'password_hash': _hash_password(data.password)
    }).execute()

    if not user_created.data:
      raise HTTPException(status_code=500, detail='No se pudo crear el usuario')

    user = user_created.data[0]
    supabase.table(PROFILES_TABLE).insert({
      'user_id': user['id'],
      'nickname': data.nickname,
      'first_name': data.first_name,
      'last_name': data.last_name,
      'middle_name': data.middle_name,
      'birth_date': data.birth_date,
      'country': data.country,
      'phone': data.phone,
    }).execute()

    return {'user': _to_user_payload(user), 'token': _create_token(user)}


def login(*, email: str, password: str) -> dict:
    result = supabase.table(USERS_TABLE).select('id,email,display_name,created_at,password_hash').eq('email', email.lower().strip()).limit(1).execute()
    if not result.data:
      raise HTTPException(status_code=401, detail='Credenciales inválidas')

    user = result.data[0]
    if not user.get('password_hash') or not _verify_password(password, user['password_hash']):
      raise HTTPException(status_code=401, detail='Credenciales inválidas')

    return {'user': _to_user_payload(user), 'token': _create_token(user)}


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

    result = supabase.table(USERS_TABLE).select("id,email,display_name,created_at").eq("id", user_id).limit(1).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return _to_user_payload(result.data[0])
