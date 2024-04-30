from app.database.dbms import DataBaseHelper
from app.database.models.file_accounting import FileAccounting


class FileDAO(DataBaseHelper):
    model = FileAccounting
