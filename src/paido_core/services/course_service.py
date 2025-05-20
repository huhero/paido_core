from sqlalchemy import select
from sqlalchemy.orm import Session

from paido_core.models.course import Course
from paido_core.schemas.course import CourseSchema


class CourseService:
    def __init__(self, session: Session):
        self.session = session

    def create_course(self, school: CourseSchema, school_id: int) -> Course:
        db_course = Course(
            name=school.name,
            description=school.description,
            school_id=school_id,
        )
        self.session.add(db_course)
        self.session.commit()
        self.session.refresh(db_course)
        return db_course

    def get_course_by_name(self, name: str, school_id: int) -> Course | None:
        return self.session.scalar(
            select(Course).where(
                Course.name == name,
                Course.school_id == school_id,
                Course.active,
            )
        )
