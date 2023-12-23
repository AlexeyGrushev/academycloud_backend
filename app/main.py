from fastapi import FastAPI

from app.equations.quadratic_equations import equation_router


app = FastAPI(
    title="API для AcademyCloud",
    version="Alpha 1.0"
    )

app.include_router(equation_router.router)
