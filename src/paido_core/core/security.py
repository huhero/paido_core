from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import Select
from sqlalchemy.orm import Session

from paido_core.core.settings import Settings
from paido_core.db.session import get_session
from paido_core.models.user import User

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')
settings = Settings()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode,
        settings.SECRET_JWT_KEY,
        algorithm=settings.ALGORITHM_JWT,
    )
    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token,
            settings.SECRET_JWT_KEY,
            algorithms=[settings.ALGORITHM_JWT],
        )
        username = payload.get('sub')

        if not username:
            raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    except PyJWTError:
        raise credentials_exception

    db_user = session.scalar(
        Select(User).where((User.email == username) & (User.active))
    )

    if not db_user:
        raise credentials_exception

    return db_user
