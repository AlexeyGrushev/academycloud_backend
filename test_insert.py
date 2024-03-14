import asyncio
from app.database.dbms import DataBaseHelper
from app.database import models as mdl


class PartOfSpeech(DataBaseHelper):
    model = mdl.Part_of_speech


async def insert_part_of_speech():
    p_o_s = PartOfSpeech()

    await p_o_s.insert_values(
        part="Существительное"
    )


if __name__ == "__main__":
    asyncio.run(insert_part_of_speech())
