from datetime import datetime
from pydantic import BaseModel


class SProfile(BaseModel):
    first_name: str
    last_name: str
    profile_picture: str | None
    status: str | None


class SUserProfile(BaseModel):
    id: int
    email: str
    register_date: datetime
    login: str

    first_name: str | None
    last_name: str | None
    profile_picture: str | None
    status: str | None
