from pydantic import EmailStr
from pydantic import BaseModel


class User(BaseModel):
    email: EmailStr
    phone_number: int
    login: str
    password: str
