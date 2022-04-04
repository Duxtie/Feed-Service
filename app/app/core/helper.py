import logging
import os, shutil, datetime, json, mimetypes
from xmltodict import parse
from pathlib import Path
from typing import Any, List, Optional

import urllib.request
import urllib.parse
import urllib.error

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


def __get(needle, haystack, default=""):
    return haystack[needle] if needle in haystack else ""


def save_item_file(db, item_id, url: str) -> Any:
    file_path = save_file(url)

    # get mime_type
    mime_type = get_mime_type(file_path)

    # save media
    return crud.media.create_item_media(db=db, data={
        "item_id": item_id,
        "path": save_file(url),
        "size": Path(file_path).stat().st_size,
        "ext": Path(file_path).suffix,
        "mime_type": mime_type
    })


def save_file(url: str, file_name: str = None) -> str:
    # set download path
    path = make_path("assets/downloads/img/")

    # create file path locally if it doesn't already exists
    if not file_name:
        file_name = str(Path(urllib.parse.urlparse(url).path).name)

    # set full file path (In some cases you may need to add a time stamp to the file name to make it unique)
    file_name = path + file_name

    try:
        file = urllib.request.urlretrieve(url, file_name)
        logging.info(file)
    except urllib.error.URLError as e:
        logging.debug(e)
    except Exception as e:
        logging.debug(e)

    return file_name


def make_path(path: str) -> str:
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def get_mime_type(file_path: str) -> str:
    mime_types = mimetypes.guess_type(file_path)
    mime_type = mime_types[0] if mime_types else None
    return mime_type
