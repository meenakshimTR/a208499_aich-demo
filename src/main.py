from fastapi import Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from auth_bearer import JWTBearer
from ddtrace import patch

patch(fastapi=True)
app = FastAPI(docs_url="/demo/asp-python/docs", redoc_url="/demo/asp-python/redoc")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/actuator/health", description="Returns the health status of the API")
def health_check():
    data = {"status": "UP"}
    return JSONResponse(content=data)


@app.post(
    "/demo/v1/slug",
    dependencies=[Depends(JWTBearer())],
    description="Sample Python application in ASP CLI.",
)
async def agents():
    return {"Message": "welcome to Python world..!"}
