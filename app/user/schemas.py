from pydantic import BaseModel, constr


class User(BaseModel):
    email: str
    phone_number: int
    login: constr(min_length=4, max_length=20)
    password: constr(min_length=8, max_length=50)
