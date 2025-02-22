from fastapi import APIRouter

from api.routes import integration

api_router = APIRouter()
api_router.include_router(integration.router)
