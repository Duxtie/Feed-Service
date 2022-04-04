from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):

    async def create_feed_item(self, db: Session, *, data):
        db_obj = self.model(**data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def w_create_feed_item(self, db: Session, *, data):
        db_obj = self.model(**data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def get_by_feed(
        self, db: Session, *, feed_id: int, id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (db.query(self.model)
                .filter(Item.id == id)
                .filter(Item.feed_id == feed_id)
                .offset(skip)
                .limit(limit)
                .all())

    async def get_multi_by_feed(
        self, db: Session, *, feed_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (db.query(self.model)
                .filter(Item.feed_id == feed_id)
                .offset(skip)
                .limit(limit)
                .all())


item = CRUDItem(Item)
