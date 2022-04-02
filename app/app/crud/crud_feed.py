from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.feed import Feed
from app.schemas.feed import FeedCreate, FeedUpdate


class CRUDFeed(CRUDBase[Feed, FeedCreate, FeedUpdate]):

    def create(self, db: Session, *, data):
        db_obj = self.model(**data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


feed = CRUDFeed(Feed)
