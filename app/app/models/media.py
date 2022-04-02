from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Media(Base):
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, index=True)
    # item_id = Column(Integer, ForeignKey("feed.id"))
    # item = relationship("Feed", back_populates="feeds")
    path = Column(String, index=True)
    size = Column(Integer)
    mime_type = Column(String)
    ext = Column(String)
