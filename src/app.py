import uvicorn
from fastapi import FastAPI

from package import get_package  # fix: fix import path
from settings import SERVICE_HOST, SERVICE_LOG_LEVEL, SERVICE_PORT  # fix: fix import path

app = FastAPI()


# idea: add new endpoints for /, /health, /version, /package, to make this easier to use

@app.get("/package/{name}/{version}", tags=["package"])
async def get_package_view(name: str, version: str):
    return await get_package(name, version)


@app.get("/package/{name}", tags=["package"])
async def get_latest_package_view(name: str):
    return await get_package(name)


if __name__ == "__main__":
    uvicorn.run("app:app", host=SERVICE_HOST, port=SERVICE_PORT, log_level=SERVICE_LOG_LEVEL)
