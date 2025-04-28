from pydantic import BaseModel, ConfigDict, EmailStr

from paido_core.models import SchoolType


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class SchoolSchema(BaseModel):
    name: str
    address: str
    phone: str
    school_type: SchoolType


class SchoolPublic(SchoolSchema):
    id: int


class SchoolList(BaseModel):
    schools: list[SchoolPublic]


class SchoolUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    phone: str | None = None
