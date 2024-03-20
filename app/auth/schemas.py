from pydantic import EmailStr, Field
from pydantic import BaseModel


class SRegisterUser(BaseModel):
    email: EmailStr
    login: str
    password: str = Field(min_length=8)


class SLoginUser(BaseModel):
    login_data: str
    password: str = Field(min_length=8)
