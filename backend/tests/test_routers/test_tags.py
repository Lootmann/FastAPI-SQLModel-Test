from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from api.models import tags as tag_model


class TestGetTag:
    def test_get_all_tags(self, client: TestClient, session: Session):
        resp = client.get("/tags")
        data = resp.json()
        assert resp.status_code == status.HTTP_200_OK
        assert len(data) == 0


class TestPostTag:
    def test_create_tag(self, client: TestClient, session: Session):
        resp = client.post("/tags", json={"name": "ttt"})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.get("/tags")
        data = resp.json()
        assert resp.status_code == status.HTTP_200_OK
        assert len(data) == 1
