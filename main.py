from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router
from core.config import settings

# FastAPI instance creation
app = FastAPI(
    title="Pheidippides API",
    summary="An interval integration designed for telex",
    version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #Only telex
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {
        "author": "Ayodeji Oni",
        "integration name": "pheiddipides",
        "description": "An integration that suggests books to read based on any selected genre.",
        "version": "0.1.0",
    }
