"""
Declarative base class — every SQLAlchemy model inherits from this.
"""
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass