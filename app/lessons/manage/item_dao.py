from app.database.dbms import DataBaseHelper
from app.database.models import Item


class ItemDAO(DataBaseHelper):
    model = Item
