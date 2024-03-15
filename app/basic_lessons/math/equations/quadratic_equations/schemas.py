from pydantic import BaseModel


class SEquation(BaseModel):
    equation: str
    root_count: int
    data: tuple
