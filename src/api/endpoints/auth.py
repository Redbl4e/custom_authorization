from fastapi import HTTPException, Depends

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.api.dependencies import UserServiceDependency, CurrentActiveUserDependency
from src.api.error_code import AuthErrorCode
from src.api.responses.auth import REGISTER_POST_RESPONSES, LOGIN_POST_RESPONSES
from src.core.types import UP
from src.schemas.user import UserReadSchema, UserCreateSchema
from src.service.auth.config import bearer_jwt_backend
from src.service.auth.exceptions import UserAlreadyExists, InvalidPassword, UserNotExists, InvalidCredentials
from src.service.auth.strategy.base import StrategyABC

router = APIRouter()

backend = bearer_jwt_backend


@router.post(
    "/register",
    response_model=UserReadSchema,
    summary="Регистрация пользователя",
    operation_id="auth:register_user",
    responses=REGISTER_POST_RESPONSES
)
async def register_user(
        user_data: UserCreateSchema,
        user_service: UserServiceDependency
):
    try:
        user = await user_service.create(user_data)
    except InvalidPassword as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "reason": e.reason,
                "code": AuthErrorCode.INVALID_PASSWORD,
                "error_fields": ["password"]
            }
        )

    except UserAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "reason": e.reason,
                "code": AuthErrorCode.USER_ALREADY_EXISTS,
                "error_fields": e.error_fields
            }
        )

    return user


@router.post(
    "/login",
    summary="Вход пользователя",
    operation_id="auth:login_user",
    responses=LOGIN_POST_RESPONSES
)
async def login(
        user_service: UserServiceDependency,
        credentials: OAuth2PasswordRequestForm = Depends(),
        strategy: StrategyABC[UP] = Depends(backend.strategy)
):
    try:
        user = await user_service.authenticate(credentials)
    except InvalidCredentials as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "reason": e.reason,
                "code": AuthErrorCode.BAD_CREDENTIALS
            }
        )
    response = await backend.login(strategy, user)
    return response


@router.get(
    "/me",
    response_model=UserReadSchema,
    summary="Информация о пользователе",
    operation_id="auth:get_current_user",
)
async def get_user(user: CurrentActiveUserDependency):
    return user
