from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    hcp_id = Column(
        Integer,
        ForeignKey("hcps.id"),
        nullable=False,
    )

    interaction_type = Column(String, nullable=False)

    interaction_date = Column(Date, nullable=False)

    notes = Column(Text, nullable=False)

    products_discussed = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    hcp = relationship(
        "HCP",
        back_populates="interactions",
    )

    followups = relationship(
        "FollowUpTask",
        back_populates="interaction",
        cascade="all, delete-orphan",
    )