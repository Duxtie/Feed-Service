from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
async def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve items.
    """
    items = await crud.item.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Item)
async def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
) -> Any:
    """
    Create new item.
    """
    item = await crud.item.create(db=db, obj_in=item_in)
    return item


@router.put("/{id}", response_model=schemas.Item)
async def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.ItemUpdate,
) -> Any:
    """
    Update an item.
    """
    item = await crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = await crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.Item)
async def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get item by ID.
    """
    item = await crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{id}", response_model=schemas.Item)
async def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an item.
    """
    item = await crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = await crud.item.remove(db=db, id=id)
    return item
