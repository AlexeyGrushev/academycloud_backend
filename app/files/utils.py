import os
import shutil
import logging

from fastapi import UploadFile

from app.exceptions.http_exceptions import (
    http_exc_400_long_file_name,
    http_exc_400_bad_file_type
)
from app.files.file_dao import FileDAO
from app.files.file_type_dao import FileTypeDAO
from app.tasks.tasks import resize_image


async def upload_profile_picture(
    file_type: int,
    file: UploadFile,
    user_id: int
):
    # Сохранение картинки профиля
    previous_profile_pic = await FileDAO.find_one_or_none(
        file_type=1,
        user_id=user_id
    )
    if previous_profile_pic is not None:
        try:
            os.remove(
                f"app/static/images/{previous_profile_pic[0].file_name}"
            )
        except Exception as ex_:
            logging.error(ex_)
            pass
        await FileDAO.delete_values(
            id=previous_profile_pic[0].id
        )

    file.filename = f"profile_pic_{user_id}.{
        file.filename.split(".")[-1]}"

    with open(
            f"app/static/images/profile_pic_{user_id}.{
                file.filename.split(".")[-1]}",
            "+wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_id = await FileDAO.insert_values(
        file_name=file.filename,
        file_type=file_type,
        user_id=user_id
    )

    resize_image.delay(
        input_image_path=f"app/static/images/{file.filename}",
        output_image_path=f"app/static/images/{file.filename}",
        size=(128, 128)
    )

    return file_id


async def upload_file_on_server(
    file_type: int,
    file: UploadFile,
    user_id: int
):
    if len(file.filename) > 150:
        raise http_exc_400_long_file_name

    file_type_check = await FileTypeDAO.find_one_or_none(id=file_type)

    if file_type_check is None:
        raise http_exc_400_bad_file_type

    if file_type == 1:
        file_id = await upload_profile_picture(file_type, file, user_id)
        return file_id
