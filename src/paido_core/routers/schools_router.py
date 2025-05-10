from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from paido_core.core.security import get_current_user
from paido_core.db.session import get_session
from paido_core.models.user import User
from paido_core.schemas.message import Message
from paido_core.schemas.school import (
    SchoolPublic,
    SchoolSchema,
    SchoolUpdate,
)
from paido_core.services.school_service import SchoolService

router = APIRouter(prefix='/schools', tags=['schools'])
T_Session = Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=SchoolPublic)
def create_school(school: SchoolSchema, session: T_Session, user: T_User):
    school_service = SchoolService(session)
    db_school = school_service.get_school_by_name(name=school.name)

    if db_school:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='School already registered',
        )

    db_school = school_service.create_school(school, user.id)

    return db_school


@router.get('/', response_model=List[SchoolPublic])
def get_schools(
    session: T_Session,
    name: str | None = None,
    skip: int = 0,
    limit: int = 10,
):
    school_service = SchoolService(session)
    db_schools = school_service.get_schools(skip=skip, limit=limit, name=name)

    return db_schools


@router.delete('/{school_name}', response_model=Message)
def delete_school(school_name: str, session: T_Session, user: T_User):
    school_service = SchoolService(session)

    db_school = school_service.get_user_school(
        user_id=user.id, name=school_name
    )

    if not db_school:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='School not found.'
        )

    db_school.active = False

    school_service.update_school(db_school)

    return {'message': 'School has been deleted successfully.'}


@router.patch('/{school_name}', response_model=SchoolPublic)
def patch_school(
    school_name: str, session: T_Session, user: T_User, school: SchoolUpdate
):
    school_service = SchoolService(session)
    db_school = school_service.get_user_school(
        user_id=user.id, name=school_name
    )

    if not db_school:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='School not found.'
        )

    for key, value in school.model_dump(exclude_unset=True).items():
        setattr(db_school, key, value)

    school_service.update_school(db_school)

    return db_school
