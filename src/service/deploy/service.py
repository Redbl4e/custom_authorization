import subprocess

from src.core.config import BASE_DIR
from src.service.auth.jwt import decode_jwt


class DeployService:
    def __init__(self):
        self.PATH_DEPLOY_SCRIPTS = BASE_DIR.parent / "scripts.sh"

    def rebuilding_the_project(self, token: str):
        if self.decode_jwt_token(token) is None:
            raise
        subprocess.run([str(self.PATH_DEPLOY_SCRIPTS)])

    @staticmethod
    def decode_jwt_token(token: str):
        try:
            return decode_jwt(token)
        except Exception:
            return None


async def get_deploy_service() -> DeployService:
    yield DeployService()

print(BASE_DIR.parent)