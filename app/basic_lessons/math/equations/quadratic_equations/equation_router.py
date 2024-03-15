from fastapi.routing import APIRouter


from app.basic_lessons.math.equations.quadratic_equations.get_equation import QuadraticEquations # noqa
from app.basic_lessons.math.equations.quadratic_equations.schemas import SEquation # noqa


router = APIRouter(
    prefix="/v1/math/equations/quadratic",
    tags=["Логика квадратных уравнений"]
)


@router.get("/get_equation")
async def generate_equation():
    data = QuadraticEquations().get_equation()
    return SEquation(
        equation=data[0],
        root_count=data[1],
        data=data[2]
    )
