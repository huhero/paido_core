from typing import List

from sqlalchemy import select
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

    def get_school_by_name(self, name: str) -> School | None:
        return self.session.scalar(
            select(School).where(School.name == name, School.active)
        )

    def get_school_by_id(self, id: int) -> School | None:
        return self.session.scalar(
            select(School).where(School.id == id, School.active)
        )

    def get_school_user_by_id(self, id: int, user_id: int) -> School | None:
        return self.session.scalar(
            select(School).where(
                School.id == id, School.user_id == user_id, School.active
            )
        )

    def get_user_school(self, user_id: int, name: str) -> School | None:
        return self.session.scalar(
            select(School).where(
                School.name == name, School.user_id == user_id, School.active
            )
        )

    def get_schools(
        self, skip: int, limit: int, name: str | None = None
    ) -> List[School] | None:
        query = select(School).where(School.active)

        if name:
            query = query.filter(School.name.contains(name))

        db_schools = self.session.scalars(
            query.offset(skip).limit(limit)
        ).all()

        return db_schools

    def update_school(self, school: School) -> School:
        self.session.commit()
        self.session.refresh(school)
        return school
