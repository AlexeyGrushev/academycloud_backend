from app.database.dbms import DataBaseHelper
from app.database.models import LessonType


class LessonTypeDAO(DataBaseHelper):
    model = LessonType
