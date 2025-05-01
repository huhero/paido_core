from sqlalchemy.orm import registry

# from .school import SchoolType

# from .user import User

table_registry = registry()

metadata = table_registry.metadata

# __all__ = [
#     'SchoolType',
# ]
