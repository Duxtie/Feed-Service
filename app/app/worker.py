from time import sleep
from typing import Any

from celery import current_task
from fastapi.encoders import jsonable_encoder

from app import crud
from app.core.celery_app import celery_app
from app.core.helper import __get, save_item_file
from app.db.session import SessionLocal

from app.api.deps import get_db

@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task(acks_late=True)
def test_celery2(word: str) -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(state='PROGRESS', meta={'process_percent': i * 10})
    return f"test task return {word}"


@celery_app.task()
def feed_load(new_feed_id, items) -> Any:
    # db = SessionLocal()
    db = next(get_db())

    # set item progress score
    progress_score = 0
    item_score = 100 / len(items)

    result = []
    for item in items:
        # save item
        new_item = crud.item.w_create_feed_item(db=db, data={
            "feed_id": new_feed_id,
            "sec_id": __get("g:id", item),
            "title": __get("title", item),
            "link": __get("link", item),
            "description": __get("description", item),
            "price": __get("g:price", item),
            "condition": __get("g:condition", item),
            "availability": __get("g:availability", item),
            "brand": __get("g:brand", item),
            "gtin": __get("g:gtin", item),
            "item_group_id": __get("g:item_group_id", item),
            "sale_price": __get("g:sale_price", item),
        })
        new_item = jsonable_encoder(new_item)

        # save primary image
        save_item_file(db, new_item['id'], __get("g:image_link", item))

        # save additional images
        additional_files = __get("g:additional_image_link", item)
        if additional_files:
            if isinstance(additional_files, list):
                for file in additional_files:
                    save_item_file(db, new_item['id'], file)
            else:
                save_item_file(db, new_item['id'], additional_files)

        result.append(new_item)

        # update task progress
        current_task.update_state(state='PROGRESS', meta={'process_percent': progress_score + item_score})

    # update feed status
    feed = crud.feed.w_get(db=db, id=new_feed_id)
    feed = crud.feed.w_update(db=db, db_obj=feed, obj_in={"status":"processed"})

    return result
