from typing import Optional
from pydantic import EmailStr
from pydantic import BaseModel


class SRegisterUser(BaseModel):
    email: EmailStr
    phone_number: Optional[int] = None
    login: str
    password: str
