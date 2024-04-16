from fastapi import APIRouter, HTTPException

from src.api.dependencies import DeployServiceDependency

router = APIRouter()


@router.get("/")
async def deploy(
        token: str,
        deploy_service: DeployServiceDependency

):
    try:
        deploy_service.rebuilding_the_project(token)
    except Exception:
        raise HTTPException(status_code=403)
