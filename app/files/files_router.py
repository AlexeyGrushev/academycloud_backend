from fastapi import Depends, File, UploadFile, Form
from fastapi.routing import APIRouter

from app.auth.dependencies import get_current_user
from app.database.models.user import User
from app.files.utils import upload_file_on_server


router = APIRouter(
    prefix="/file",
    tags=["Управление файлами"]
)


@router.post("/upload_file")
async def upload_file(
    file_type: int = Form(...),
    user: User = Depends(get_current_user),
    file: UploadFile = File(...),
):
    file_id = await upload_file_on_server(
        file_type,
        file,
        user[0].id
    )
    return {
        "status": "success",
        "file_id": file_id
    }
