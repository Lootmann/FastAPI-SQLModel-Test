from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from api.models import users as user_model
from tests.factory import UserFactory


class TestPostUser:
    def test_create_user(self, client: TestClient):
        resp = client.post("/users", json={"name": "hoge", "secret_name": "hogege"})
        data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert data["name"] == "hoge"
        assert data["id"] is not None


class TestGetUser:
    def test_get_all_user(self, client: TestClient, session: Session):
        UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        UserFactory.create_user(session, user_model.UserCreate(name="hage"))
        UserFactory.create_user(session, user_model.UserCreate(name="hige"))

        resp = client.get("/users")
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert len(data) == 3

    def test_get_one_user(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))

        resp = client.get(f"/users/{user.id}")
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data["id"] == user.id
        assert data["name"] == user.name

    def test_get_one_user_with_wrong_id(self, client: TestClient):
        resp = client.get("/users/123")
        data = resp.json()

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "User 123: Not Found"}


class TestPatchUser:
    def test_update_user(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))

        resp = client.patch(f"/users/{user.id}", json={"name": "updated :^)"})
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert data["id"] == user.id
        assert data["name"] == "updated :^)"

    def test_update_user_with_wrong_id(self, client: TestClient):
        resp = client.patch("/users/123", json={"name": "updated"})
        data = resp.json()

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "User 123: Not Found"}


class TestDeleteUser:
    def test_delete_user(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))

        resp = client.get("/users")
        data = resp.json()
        assert len(data) == 1

        resp = client.delete(f"/users/{user.id}")
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert data == None

        resp = client.get("/users")
        data = resp.json()
        assert len(data) == 0

    def test_delete_user_with_wrong_id(self, client: TestClient):
        resp = client.delete(f"/users/123")
        data = resp.json()
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "User 123: Not Found"}
