from typing import Optional

from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    feed_id: Optional[int] = None
    sec_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    image_link: Optional[str] = None
    additional_image_link: Optional[str] = None
    price: Optional[str] = None
    condition: Optional[str] = None
    availability: Optional[str] = None
    brand: Optional[str] = None
    gtin: Optional[str] = None
    item_group_id: Optional[str] = None
    sale_price: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    feed_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
