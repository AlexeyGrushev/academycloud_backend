from datetime import datetime
from pydantic import BaseModel


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
    status: str | None
