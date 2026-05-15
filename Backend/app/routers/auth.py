from fastapi import APIRouter, Depends

from app.schemas.auth_schema import AuthResponse, LoginRequest, SignUpRequest
from app.services.auth_service import get_current_user, login, signup

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=AuthResponse)
def auth_signup(data: SignUpRequest):
    return AuthResponse(**signup(data=data))


@router.post("/login", response_model=AuthResponse)
def auth_login(data: LoginRequest):
    return AuthResponse(**login(email=data.email, password=data.password))


@router.get("/me")
def auth_me(user=Depends(get_current_user)):
    return {"user": user}
