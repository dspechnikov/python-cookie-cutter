from fastapi import FastAPI
from {{cookiecutter.__project_slug}}.api.routes import router

app = FastAPI()

app.include_router(router)
