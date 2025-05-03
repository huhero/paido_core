from sqlalchemy.orm import Session

from paido_core.models.school import School
from paido_core.schemas.school import SchoolSchema


class SchoolService:
    def __init__(self, session: Session):
        self.session = session

    def create_school(self, school: SchoolSchema, user_id: int) -> School:
        db_school = School(
            name=school.name,
            address=school.address,
            phone=school.phone,
            school_type=school.school_type,
            user_id=user_id,
        )
        self.session.add(db_school)
        self.session.commit()
        self.session.refresh(db_school)
        return db_school
