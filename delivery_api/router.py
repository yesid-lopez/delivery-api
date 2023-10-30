import os

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthcheck")
def read_root():
    return {"message": "The healthcheck was successful."}


def run():
    host = os.getenv("HOST", "127.0.0.1")
    uvicorn.run("delivery_api.router:app", host=host, reload=True)
