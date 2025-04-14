from pydantic import BaseModel, EmailStr, ConfigDict, Field


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'


class RegisterUserSchema(BaseModel):
    """
    Схема для регистрации пользователя
    """

    model_config = ConfigDict(strict=True)
 
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(...)
    name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
 
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True