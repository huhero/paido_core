from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from paido_core.core.security import get_current_user
from paido_core.db.session import get_session
from paido_core.models.user import User
from paido_core.schemas.course import CoursePublic, CourseSchema
from paido_core.services.course_service import CourseService
from paido_core.services.school_service import SchoolService

router = APIRouter(tags=['courses'])
T_Session = Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


@router.post(
    '/school/{school_id}/course',
    response_model=CoursePublic,
    status_code=HTTPStatus.CREATED,
)
def create_course(
    school_id: int, course: CourseSchema, session: T_Session, user: T_User
):
    school_service = SchoolService(session)
    db_school = school_service.get_school_by_id(school_id, user.id)
    if db_school is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='There is no school for this course.',
        )

    course_service = CourseService(session)
    db_course = course_service.get_course_by_name(
        name=course.name, school_id=db_school.id
    )

    if db_course:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Your school already exists',
        )

    db_course = course_service.create_course(course, school_id)

    return db_course
