from pydantic import BaseModel


class SItem(BaseModel):
    name: str


class SLesson(BaseModel):
    id: int


class SLessonAnswer(SLesson):
    answer: list
