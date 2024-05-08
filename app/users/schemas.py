from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class SProfile(BaseModel):
    first_name: str
    last_name: str
    status: str | None


class SUserProfile(BaseModel):
    id: int
    email: str
    register_date: datetime
    login: str
    role: int
    is_verified: bool

    first_name: str | None
    last_name: str | None
    profile_pic: str | None
    points: int | None
    status: str | None


class SUserActivationManager(BaseModel):
    id: int
    is_active: bool


class SUserLoginData(BaseModel):
    login_data: str


class SUserUpdate(BaseModel):
    email: EmailStr | None
    login: str | None
    password: str | None = Field(min_length=8)
