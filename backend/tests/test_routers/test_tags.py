from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from api.models import tags as tag_model
from tests.factory import TagFactory


class TestGetTag:
    def test_get_all_tags(self, client: TestClient, session: Session):
        resp = client.get("/tags")
        data = resp.json()
        assert resp.status_code == status.HTTP_200_OK
        assert len(data) == 0

    def test_get_one_tag(self, client: TestClient, session: Session):
        tag = TagFactory.create_tag(session, tag_model.TagCreate(name="hoge"))

        resp = client.get(f"/tags/{tag.id}")
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data["name"] == "hoge"

    def test_get_one_tag_with_wrong_id(self, client: TestClient, session: Session):
        resp = client.get("/tags/123")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestPostTag:
    def test_create_tag(self, client: TestClient, session: Session):
        resp = client.post("/tags", json={"name": "ttt"})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = client.get("/tags")
        data = resp.json()
        assert resp.status_code == status.HTTP_200_OK
        assert len(data) == 1
