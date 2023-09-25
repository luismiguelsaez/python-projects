from fastapi import FastAPI, Response
from os import environ

CACHE_CONTROL = environ.get("CACHE_CONTROL", "max-age=3600, public")

# Create the FastAPI instance
app = FastAPI()

# Create a path operation decorator
@app.get("/") # Decorator
async def root(response: Response):
    return {"message": "Root path without cache control"}

@app.get("/v2")
async def v2_root(response: Response):
    response.headers["Cache-Control"] = "{}".format(CACHE_CONTROL)
    response.status_code = 403
    return {"message": "Root path with cache control"}
