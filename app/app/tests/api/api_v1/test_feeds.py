import logging
import os, glob
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.tests.conftest import db

from app.core.config import settings
from app.core.helper import get_mime_type

from app.main import app

client = TestClient(app)


def test_create_feed():
    data = {"title": "Foo", "description": "Fighters"}

    # set file path
    file_path = "./assets/files/feed_upload_example_file.xml"

    # check if file exists
    assert os.path.isfile(file_path)

    # get file mime_type
    mime_type = get_mime_type(file_path)

    # check if file is xml
    assert mime_type == "text/xml"


    # print("Otel")
    # file_path2 = "../feed_upload_example_file.xml"
    # assert os.path.isfile(file_path2)

    with open(file_path, "r") as file:
        response = client.post(
            f"{settings.API_V1_STR}/feeds/",
            json=data,
            files={"file": ("filename", file, mime_type)}
        )

    return response

    # assert response.status_code == 200
    # content = response.json()
    # assert "id" in content
    # assert content["status"] == "processing" or "successful" or "failed"

# def test_read_feed(
#         client: TestClient, superuser_token_headers: dict, db: Session
# ) -> None:
#     feed = create_random_feed(db)
#     response = client.get(
#         f"{settings.API_V1_STR}/feeds/{feed.id}", headers=superuser_token_headers,
#     )
#     assert response.status_code == 200
#     content = response.json()
#     assert "status" in content
#     assert content["status"] == feed.status
