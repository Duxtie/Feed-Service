from typing import Optional

from pydantic import BaseModel


# Shared properties
class FeedBase(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class FeedCreate(FeedBase):
    title: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item update
class FeedUpdate(FeedBase):
    pass


# Properties shared by models stored in DB
class FeedInDBBase(FeedBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Feed(FeedInDBBase):
    pass


# Properties properties stored in DB
class FeedInDB(FeedInDBBase):
    pass
