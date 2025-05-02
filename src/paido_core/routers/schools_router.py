from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from paido_core.core.security import get_current_user
from paido_core.db.session import get_session
from paido_core.models.school import School
from paido_core.models.user import User
from paido_core.schemas.message import Message
from paido_core.schemas.school import (
    SchoolList,
    SchoolPublic,
    SchoolSchema,
    SchoolUpdate,
)

router = APIRouter(prefix='/schools', tags=['schools'])
T_Session = Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=SchoolPublic)
def create_school(school: SchoolSchema, session: T_Session, user: T_User):
    db_school = School(
        name=school.name,
        address=school.address,
        phone=school.phone,
        school_type=school.school_type,
        user_id=user.id,
    )

    session.add(db_school)
    session.commit()
    session.refresh(db_school)
    return db_school


@router.get('/', response_model=SchoolList)
def get_schools(
    session: T_Session,
    user: T_User,
    name: str | None = None,
    skip: int = 0,
    limit: int = 10,
):
    query = select(School).where(School.user_id == user.id)

    if name:
        query = query.filter(School.name.contains(name))

    db_schools = session.scalars(query.offset(skip).limit(limit)).all()
    return {'schools': db_schools}


@router.delete('/{school_id}', response_model=Message)
def delete_school(school_id: int, session: T_Session, user: T_User):
    db_school = session.scalar(
        select(School).where(
            School.user_id == user.id, School.id == school_id, School.active
        )
    )

    if not db_school:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='School not found.'
        )

    db_school.active = False
    session.commit()

    return {'message': 'School has been deleted successfully.'}


@router.patch('/{school_id}', response_model=SchoolPublic)
def patch_school(
    school_id: int, session: T_Session, user: T_User, school: SchoolUpdate
):
    db_school = session.scalar(
        select(School).where(
            School.user_id == user.id, School.id == school_id, School.active
        )
    )

    if not db_school:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='School not found.'
        )

    for key, value in school.model_dump(exclude_unset=True).items():
        setattr(db_school, key, value)

    session.add(db_school)
    session.commit()
    session.refresh(db_school)

    return db_school
