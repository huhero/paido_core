from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from paido_core.core.security import (
    create_access_token,
    get_current_user,
    verify_password,
)
from paido_core.db.session import get_session
from paido_core.models.user import User
from paido_core.schemas.auth import Token

router = APIRouter(prefix='/auth', tags=['auth'])
T_Session = Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


@router.post('/token', response_model=Token)
def login_for_access_token(
    session: T_Session,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    db_user = session.scalar(
        select(User).where((User.email == form_data.username) & (User.active))
    )

    if not db_user or not verify_password(
        form_data.password, db_user.password
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': db_user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(current_user: T_User):
    new_access_token = create_access_token(data={'sub': current_user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
