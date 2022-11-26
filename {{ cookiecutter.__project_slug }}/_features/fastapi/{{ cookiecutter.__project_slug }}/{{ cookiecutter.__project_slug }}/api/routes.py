from fastapi import APIRouter
from {{cookiecutter.__project_slug}}.api.schemas import SomeSchema

router = APIRouter(
    prefix="/api",
)


@router.get("/something")
def get_something() -> SomeSchema():
    return SomeSchema()
