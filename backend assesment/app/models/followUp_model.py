from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class FollowUpTask(Base):
    __tablename__ = "follow_up_tasks"

    id = Column(Integer, primary_key=True, index=True)

    interaction_id = Column(
        Integer,
        ForeignKey("interactions.id"),
        nullable=False,
    )

    task = Column(String, nullable=False)

    due_date = Column(Date)

    status = Column(
        String,
        default="Pending",
    )

    created_at = Column(
        DateTime,
        default=datetime.now()
    )

    interaction = relationship(
        "Interaction",
        back_populates="followups",
    )