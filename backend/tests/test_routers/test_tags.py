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


class TestUpdateTag:
    def test_update_tag(self, client: TestClient, session: Session):
        tag = TagFactory.create_tag(session, tag_model.TagCreate(name="new tag"))

        resp = client.patch(f"/tags/{tag.id}", json={"name": "updated"})
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data["id"] == tag.id
        assert data["name"] != "new tag"
        assert data["name"] == "updated"

    def test_update_tag_with_wrong_id(self, client: TestClient, session: Session):
        TagFactory.create_tag(session, tag_model.TagCreate(name="new tag"))

        resp = client.patch("/tags/123", json={"name": "updated"})
        data = resp.json()

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "Tag 123: Not Found"}

    def test_update_tag_with_empty_name(self, client: TestClient, session: Session):
        tag = TagFactory.create_tag(session, tag_model.TagCreate(name="new tag"))

        resp = client.patch(f"/tags/{tag.id}", json={"name": ""})
        data = resp.json()

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert data == {"detail": "Tag: Should Not Empty"}


class TestDeleteTag:
    def test_delete_tag(self, client: TestClient, session: Session):
        tag = TagFactory.create_tag(session, tag_model.TagCreate(name="new tag"))

        resp = client.delete(f"/tags/{tag.id}")
        data = resp.json()
        assert resp.status_code == status.HTTP_200_OK
        assert data == None

    def test_delete_tag_with_wrong_id(self, client: TestClient, session: Session):
        resp = client.delete(f"/tags/123")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
