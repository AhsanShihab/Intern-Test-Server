from fastapi import Depends, Header, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from user import service as user_service
from user.schemas import UserInDB
from authentication.security_config import decode_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme.lower() == "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"msg": "Invalid authentication scheme."},
                )
            if not decode_token(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"msg": "Invalid or expired token."},
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"msg": "Invalid authorization code."},
            )


require_token = JWTBearer()

"""
# Simplified version of  `require_token`

async def require_token(
    Authorization: str = Header(example="Bearer my-access-token"),
) -> str:
    if (
        not Authorization
        or Authorization.split(" ")[0].lower() != "bearer"
        or not Authorization.split(" ")[1]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "Invalid header."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        decode_token(token)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "Invalid or expired token."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Authorization.split(" ")[1]
"""


async def get_current_user(token=Depends(require_token)) -> UserInDB:
    decoded_token = decode_token(token)
    user = await user_service.get_user_by_id(decoded_token["id"])
    return user
