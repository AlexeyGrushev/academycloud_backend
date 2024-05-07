from app.database.dbms import DataBaseHelper
from app.database.models import Lesson


class LessonDAO(DataBaseHelper):
    model = Lesson
