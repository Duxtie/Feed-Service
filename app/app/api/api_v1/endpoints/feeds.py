import json
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from xmltodict import parse

from app import crud, schemas
from app.api import deps
from app.core.celery_app import celery_app

router = APIRouter()


@router.get("/", response_model=List[schemas.Feed])
def read_feeds(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve feeds.
    """
    feeds = crud.feed.get_multi(db, skip=skip, limit=limit)
    return feeds


@router.post("/")
async def create_feed(
        *,
        db: Session = Depends(deps.get_db),
        file: UploadFile = File(...)) -> Any:
    """
    Create new feed.
    """
    content = json.loads(json.dumps(parse(await file.read())))
    content = content["channel"]

    feed_data = {
        "title": content["title"],
        "description": content["description"],
        "status": "processing"
    }

    new_feed = crud.feed.create(db=db, data=feed_data)

    new_feed = jsonable_encoder(new_feed)
    new_feed_id = int(new_feed["id"])
    items = content["item"]

    # crate items in the background
    args = [new_feed_id, items]
    # worker.feed_load.delay(*args)
    celery_app.send_task("app.worker.feed_load", args=args)

    return {"id": new_feed_id}


@router.get("/{id}")
def read_feed(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Get feed by ID.
    """
    feed = crud.feed.get(db=db, id=id)
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")

    feed = jsonable_encoder(feed)

    return {"status": feed["status"]}


@router.get("/{feed_id}/items", response_model=List[schemas.Item])
def read_feed_items(
        *,
        db: Session = Depends(deps.get_db),
        feed_id: int,
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve feeds.
    """
    feed_items = crud.item.get_multi_by_feed(db, feed_id=feed_id, skip=skip, limit=limit)
    return feed_items


@router.get("/{feed_id}/items/{item_id}")
def read_feed_item(
        *,
        db: Session = Depends(deps.get_db),
        feed_id: int,
        item_id: int,
) -> Any:
    """
    Get item by feed_id and item_id.
    """
    feed = crud.item.get_by_feed(db=db, id=item_id, feed_id=feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    return jsonable_encoder(feed)


@router.get("/{feed_id}/images")
def read_feed_images(
        *,
        db: Session = Depends(deps.get_db),
        feed_id: int,
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve feed images id.
    """
    # get all feed items
    feed_items = crud.item.get_multi_by_feed(db, feed_id=feed_id, skip=skip, limit=limit)
    feed_items = jsonable_encoder(feed_items)

    # get items id
    item_ids = []
    for item in feed_items:
        item_ids.append(item['id'])

    # get items images
    feed_items = crud.media.get_multi_by_items(db, item_ids=item_ids, skip=skip, limit=limit)
    feed_images = jsonable_encoder(feed_items)

    # get images id
    image_ids = []
    for image in feed_images:
        image_ids.append(image['id'])

    return image_ids


@router.get("/{feed_id}/images/{image_id}")
def read_feed_image(
        *,
        db: Session = Depends(deps.get_db),
        feed_id: int,
        image_id: int,
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve feed images id.
    """
    # get all feed items
    feed_items = crud.item.get_multi_by_feed(db, feed_id=feed_id, skip=skip, limit=limit)
    feed_items = jsonable_encoder(feed_items)

    # get items id
    item_ids = []
    for item in feed_items:
        item_ids.append(item['id'])

    # get items images
    feed_image = crud.media.get_by_item(db, media_id=image_id, item_ids=item_ids, skip=skip, limit=limit)
    feed_image = jsonable_encoder(feed_image)

    return feed_image


@router.delete("/{id}", response_model=schemas.Feed)
def delete_feed(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Delete an feed.
    """
    feed = crud.feed.get(db=db, id=id)
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    feed = crud.feed.remove(db=db, id=id)
    return feed
