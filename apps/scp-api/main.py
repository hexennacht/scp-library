from routes.routes import api
from fastapi import FastAPI
from core.configuration import settings
import uvicorn


def app() -> FastAPI:
    app = FastAPI(title=settings.app.name, version=settings.app.version)
    app.include_router(api)
    return app

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app.host, port=settings.app.port, reload=True)