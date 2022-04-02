from typing import Optional

from pydantic import BaseModel


# Shared properties
class MediaBase(BaseModel):
    item_id: Optional[int] = None
    path: Optional[str] = None
    mime_type: Optional[str] = None
    ext: Optional[str] = None


# Properties to receive on item creation
class MediaCreate(MediaBase):
    item_id: int
    path: str
    mime_type: str
    ext: str


# Properties to receive on item update
class MediaUpdate(MediaBase):
    pass


# Properties shared by models stored in DB
class MediaInDBBase(MediaBase):
    id: int
    title: str
    feed_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Media(MediaInDBBase):
    pass


# Properties properties stored in DB
class MediaInDB(MediaInDBBase):
    pass
