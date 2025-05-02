from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from paido_core.core.security import (
    get_current_user,
    get_password_hash,
)
from paido_core.db.session import get_session
from paido_core.models.user import User
from paido_core.schemas.message import Message
from paido_core.schemas.user import UserList, UserPublic, UserSchema
from paido_core.services.user_service import UserService

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    user_service = UserService(session)
    db_user = user_service.get_user_by_email_or_username(
        email=user.email, username=user.username
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='User already registered',
        )

    db_user = user_service.create_user(user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(
    session: T_Session,
    skip: int = 0,
    limit: int = 10,
):
    # users = session.scalars(
    #     select(User).where(User.active).offset(skip).limit(limit)
    # ).all()
    user_service = UserService(session)
    return user_service.get_list_of_users(skip=skip, limit=limit)


@router.get('/{username}', response_model=UserPublic)
def read_user_username(username: str, session: T_Session):
    user_service = UserService(session)

    db_user = user_service.get_user_by_email_or_username(username=username)

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return db_user


@router.put('/{username}', response_model=UserPublic)
def update_user(
    username: str,
    user: UserSchema,
    session: T_Session,
    current_user: T_User,
):
    user_service = UserService(session)
    db_user = user_service.get_user_by_email_or_username(
        username=current_user.username
    )

    if db_user.username != username:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = get_password_hash(user.password)

    return user_service.update_user(db_user)


@router.delete('/{username}', response_model=Message)
def delete_user(
    username: str,
    session: T_Session,
    current_user: T_User,
):
    user_service = UserService(session)
    db_user = user_service.get_user_by_email_or_username(
        username=current_user.username
    )

    if db_user.username != username:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    user_service.delete_user(db_user)
    return {'message': 'User deleted'}
