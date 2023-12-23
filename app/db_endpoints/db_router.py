from fastapi.routing import APIRouter


router = APIRouter(
    prefix="/db",
    tags=["Взаимодействия с базой данных"]
)
