from .base import metadata, table_registry
from .course import Course
from .school import School
from .user import User

__all__ = [
    'User',
    'School',
    'Course',
    'table_registry',
    'metadata',
]
