from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Media])
def read_medias(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve medias.
    """
    medias = crud.media.get_multi(db, skip=skip, limit=limit)
    return medias


@router.post("/", response_model=schemas.Media)
def create_media(
    *,
    db: Session = Depends(deps.get_db),
    media_in: schemas.MediaCreate,
) -> Any:
    """
    Create new media.
    """
    media = crud.media.create(db=db, obj_in=media_in)
    return media


@router.put("/{id}", response_model=schemas.Media)
def update_media(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    media_in: schemas.MediaUpdate,
) -> Any:
    """
    Update an media.
    """
    media = crud.media.get(db=db, id=id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    media = crud.media.update(db=db, db_obj=media, obj_in=media_in)
    return media


@router.get("/{id}", response_model=schemas.Media)
def read_media(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get media by ID.
    """
    media = crud.media.get(db=db, id=id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media


@router.delete("/{id}", response_model=schemas.Media)
def delete_media(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an media.
    """
    media = crud.media.get(db=db, id=id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    media = crud.media.remove(db=db, id=id)
    return media
