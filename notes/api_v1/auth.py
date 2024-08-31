import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


security = HTTPBasic()

USERS = {
    'admin': 'admin',
    'usser': 'qwerty',
}

def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Basic'}
    )

    correct_password = USERS.get(credentials.username)
    if not correct_password:
        raise unauthed_exc

    if not secrets.compare_digest(
        credentials.password.encode('utf-8'),
        correct_password.encode('utf-8')
    ):
        raise unauthed_exc

    return credentials.username
