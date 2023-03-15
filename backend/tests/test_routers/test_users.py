from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from api.models.users import UserCreate
from tests.factory import UserFactory


class TestPostUser:
    def test_create_user(self, client: TestClient):
        resp = client.post("/users", json={"name": "hoge", "secret_name": "hogege"})
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data["name"] == "hoge"
        assert data["id"] is not None


class TestGetUser:
    def test_get_all_user(self, client: TestClient, session: Session):
        UserFactory.create_user(session, UserCreate(name="hoge"))
        UserFactory.create_user(session, UserCreate(name="hage"))
        UserFactory.create_user(session, UserCreate(name="hige"))

        resp = client.get("/users")
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert len(data) == 3
