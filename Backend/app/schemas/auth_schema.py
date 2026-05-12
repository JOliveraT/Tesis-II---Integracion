from pydantic import BaseModel, EmailStr


class SignUpRequest(BaseModel):
    email: EmailStr
    display_name: str


class LoginRequest(BaseModel):
    email: EmailStr


class AuthUser(BaseModel):
    id: str
    email: EmailStr
    display_name: str
    created_at: str | None = None


class AuthResponse(BaseModel):
    user: AuthUser
    token: str
