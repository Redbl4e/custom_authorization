from fastapi import Depends
from typing_extensions import Annotated

from src.core.types import UP
from src.service.auth.config import authenticator
from src.service.auth.service import UserService, get_user_service
from src.service.deploy.service import DeployService, get_deploy_service

get_current_active_user = authenticator.current_user(
    active=True
)

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
CurrentActiveUserDependency = Annotated[UP, Depends(get_current_active_user)]
DeployServiceDependency = Annotated[DeployService, Depends(get_deploy_service)]