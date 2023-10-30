import os

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    """
    Returns a hello world message
    :return: dict with a hello world message
    """
    return {"Hello": "World"}


@app.get("/healthcheck")
def healthcheck() -> dict[str, str]:
    """
    Returns a healthcheck validation
    :return: dict with a successful healthcheck message
    """
    return {"message": "The healthcheck was successful."}


def run() -> None:
    """
    Bootstraps the delivery service
    """
    host = os.getenv("HOST", "127.0.0.1")
    reload = os.getenv("RELOAD", "False") == "True"
    uvicorn.run("delivery_api.router:app", host=host, reload=reload)
