from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    sec_id = Column(String, index=True)
    feed_id = Column(Integer, index=True)
    # feed_id = Column(Integer, ForeignKey("feed.id"))
    # feed = relationship("Feed", back_populates="feeds")
    title = Column(String, index=True)
    description = Column(Text)
    link = Column(String)
    image_link = Column(String)
    additional_image_link = Column(Text)
    price = Column(String)
    condition = Column(String)
    availability = Column(String)
    brand = Column(String)
    gtin = Column(String)
    item_group_id = Column(String)
    sale_price = Column(String)
