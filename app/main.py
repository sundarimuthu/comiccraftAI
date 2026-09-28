from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import (
    APP_NAME,
    BASE_DIR
)

from app.routes import router


app = FastAPI(
    title=APP_NAME
)


templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "templates"
    )
)


app.state.templates = templates


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            BASE_DIR / "static"
        )
    ),
    name="static"
)


app.include_router(
    router
)


@app.get("/health")
def health():

    return {
        "status": "ok",
        "app": APP_NAME
    }