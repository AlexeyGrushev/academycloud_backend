from fastapi.routing import APIRouter

from app.equations.quadratic_equations.get_equation import QuadraticEquations
from app.equations.quadratic_equations.schemas import SEquation


router = APIRouter(
    prefix="/v1/equations/quadratic",
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
