from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.equations.quadratic_equations import equation_router
from app.user import user_router


app = FastAPI(
    title="API для AcademyCloud",
    version="Alpha 1.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(equation_router.router)
app.include_router(user_router.router)