from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=True)
    hospital = Column(String, nullable=True)
    city = Column(String, nullable=True)

    interactions = relationship(
        "Interaction",
        back_populates="hcp",
        cascade="all, delete-orphan",
    )

    