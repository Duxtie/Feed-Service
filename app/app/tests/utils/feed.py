from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.feed import FeedCreate
from app.tests.utils.utils import random_lower_string


def create_random_feed(db: Session, *, owner_id: Optional[int] = None) -> models.Item:

    title = random_lower_string()
    description = random_lower_string()
    feed_in = FeedCreate(title=title, description=description, id=id, status="processing")
    return crud.feed.create_with_owner(db=db, obj_in=feed_in, owner_id=owner_id)
