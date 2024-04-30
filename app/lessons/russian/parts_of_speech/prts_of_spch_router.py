from fastapi.routing import APIRouter


router = APIRouter(
    prefix="/v1/russian/",
    tags=["Логика заданий по русскому языку"]
)


@router.get("/get_part_of_speech")
async def generate_equation():
    # data = QuadraticEquations().get_equation()
    # return SEquation(
    #     equation=data[0],
    #     root_count=data[1],
    #     data=data[2]
    # )
    return "Заглушка"
