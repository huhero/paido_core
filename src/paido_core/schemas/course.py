from pydantic import BaseModel


class CourseSchema(BaseModel):
    name: str
    description: str


class CoursePublic(CourseSchema):
    id: int
