from pydantic import BaseModel

from paido_core.models.school import SchoolType


class SchoolSchema(BaseModel):
    name: str
    address: str
    phone: str
    school_type: SchoolType


class SchoolPublic(SchoolSchema):
    id: int


class SchoolUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    phone: str | None = None
