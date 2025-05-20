from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import table_registry


@table_registry.mapped_as_dataclass
class Course:
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    school_id: Mapped[int] = mapped_column(ForeignKey('schools.id'))
    active: Mapped[bool] = mapped_column(init=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint('school_id', 'name', name='uq_school_course_name'),
    )
