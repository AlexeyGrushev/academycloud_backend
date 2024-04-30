from app.database.dbms import DataBaseHelper
from app.database.models.file_type import FileType


class FileTypeDAO(DataBaseHelper):
    model = FileType
