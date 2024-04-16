from fastapi import APIRouter

from src.api.endpoints.auth import router as auth_router
from src.api.endpoints.deploy import router as deploy_router


api_router = APIRouter()

api_router.include_router(auth_router, prefix="/user", tags=["auth"])
api_router.include_router(deploy_router, prefix="/deploy", tags=["deploy"])
