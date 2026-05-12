from fastapi import APIRouter, Depends

from app.schemas.auth_schema import AuthResponse, LoginRequest, SignUpRequest
from app.services.auth_service import get_current_user, login, signup

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=AuthResponse)
def auth_signup(data: SignUpRequest):
    return AuthResponse(**signup(email=data.email, display_name=data.display_name))


@router.post("/login", response_model=AuthResponse)
def auth_login(data: LoginRequest):
    return AuthResponse(**login(email=data.email))


@router.get("/me")
def auth_me(user=Depends(get_current_user)):
    return {"user": user}
