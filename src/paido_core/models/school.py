from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

# table_registry = registry()
from . import table_registry


class SchoolType(str, Enum):
    school = 'school'
    academy = 'academy'
    league = 'league'
    none = 'none'


@table_registry.mapped_as_dataclass
class School:
    __tablename__ = 'schools'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str]
    phone: Mapped[str]
    school_type: Mapped[SchoolType]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    active: Mapped[bool] = mapped_column(init=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
