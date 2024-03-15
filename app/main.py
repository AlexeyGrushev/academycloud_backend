from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.basic_lessons.math.equations.quadratic_equations import (
    equation_router
)
from app.auth import auth_router


app = FastAPI(
    title="API для AcademyCloud",
    version="Alpha 1.5"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(equation_router.router)
