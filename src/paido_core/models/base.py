from sqlalchemy.orm import registry

table_registry = registry()
metadata = table_registry.metadata
