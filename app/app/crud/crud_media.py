from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.media import Media
from app.schemas.media import MediaCreate, MediaUpdate


class CRUDMedia(CRUDBase[Media, MediaCreate, MediaUpdate]):

    async def create_item_media(self, db: Session, *, data):
        db_obj = self.model(**data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def get_by_item(
        self, db: Session, *, item_id: int, id: int, skip: int = 0, limit: int = 100
    ) -> List[Media]:
        return (db.query(self.model)
                .filter(Media.id == id)
                .filter(Media.item_id == item_id)
                .offset(skip)
                .limit(limit)
                .all())

    async def get_multi_by_item(
        self, db: Session, *, item_id: int, skip: int = 0, limit: int = 100
    ) -> List[Media]:
        return (db.query(self.model)
                .filter(Media.item_id == item_id)
                .offset(skip)
                .limit(limit)
                .all())

    async def get_multi_by_items(
        self, db: Session, *, item_ids: List[int], skip: int = 0, limit: int = 100
    ) -> List[Media]:
        return (db.query(self.model)
                .filter(Media.item_id.in_(item_ids))
                .offset(skip)
                .limit(limit)
                .all())

    async def get_by_item(
        self, db: Session, *, media_id: int, item_ids: List[int], skip: int = 0, limit: int = 100
    ) -> List[Media]:
        return (db.query(self.model)
                .filter(Media.id == media_id)
                .filter(Media.item_id.in_(item_ids))
                .first())


media = CRUDMedia(Media)
