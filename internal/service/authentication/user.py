from typing import Annotated
from uuid import UUID
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from internal.config.settings import settings

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.AUTHORIZATION_URL,
    tokenUrl=settings.TOKEN_URL,
    refreshUrl=settings.REFRESH_URL,
    scheme_name=settings.AUTH_SCHEME_NAME
)


def authorized_user_id(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        decoded = jwt.decode(token,
                             verify=False,
                             options={"verify_signature": False})
        return UUID(decoded['sub'])
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Not Authenticated')
