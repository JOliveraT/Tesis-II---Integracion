from pydantic import BaseModel, Field, field_validator
import re

EMAIL_REGEX = re.compile(r"^[\w.-]+@[\w.-]+\.\w+$")
NAME_REGEX = re.compile(r"^[A-Za-zÀ-ÿ\s]+$")
PHONE_REGEX = re.compile(r"^\d+$")


class SignUpRequest(BaseModel):
    nickname: str = Field(min_length=3, max_length=50)
    first_name: str = Field(min_length=2, max_length=80)
    last_name: str = Field(min_length=2, max_length=80)
    middle_name: str = Field(min_length=2, max_length=80)
    email: str
    country: str = Field(min_length=2, max_length=80)
    phone: str
    birth_date: str | None = None
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str) -> str:
      if not EMAIL_REGEX.match(value):
        raise ValueError('Formato de correo inválido')
      return value.lower().strip()

    @field_validator('first_name', 'last_name', 'middle_name')
    @classmethod
    def validate_name(cls, value: str) -> str:
      if not NAME_REGEX.match(value):
        raise ValueError('Nombre y apellidos solo deben contener letras y espacios')
      return value.strip()

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value: str) -> str:
      cleaned = value.strip().replace('+', '')
      if not PHONE_REGEX.match(cleaned):
        raise ValueError('El teléfono debe contener solo números')
      if len(cleaned) < 8 or len(cleaned) > 15:
        raise ValueError('El teléfono debe tener entre 8 y 15 dígitos')
      return cleaned


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthUser(BaseModel):
    id: str
    email: str
    display_name: str
    created_at: str | None = None


class AuthResponse(BaseModel):
    user: AuthUser
    token: str
