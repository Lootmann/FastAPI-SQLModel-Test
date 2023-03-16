from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from api.models import posts as post_model
from api.models import users as user_model
from tests.factory import PostFactory, UserFactory


class TestPostPost:
    def test_create_post(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        resp = client.post("/posts", json={"content": "first post", "user_id": user.id})
        data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert data["user_id"] == user.id
        assert data["content"] == "first post"


class TestGetPost:
    def test_get_all_posts_with_no_posts(self, client: TestClient, session: Session):
        resp = client.get("/posts")
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data == []

    def test_get_all_posts(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        PostFactory.create_post(
            session, post_model.PostCreate(content="first post", user_id=user.id)
        )
        PostFactory.create_post(
            session, post_model.PostCreate(content="second post", user_id=user.id)
        )
        PostFactory.create_post(
            session, post_model.PostCreate(content="third post", user_id=user.id)
        )

        resp = client.get("/posts")
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(data) == 3

    def test_get_one_post(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        post = PostFactory.create_post(
            session, post_model.PostCreate(content="first post", user_id=user.id)
        )

        resp = client.get(f"/posts/{post.id}")
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data["id"] == post.id
        assert data["content"] == "first post"
        assert data["user_id"] == user.id

    def test_get_one_post_with_wrong_id(self, client: TestClient):
        resp = client.get("/posts/123")
        data = resp.json()

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "Post 123: Not Found"}


class TestPostFactory:
    def test_create_post_factory(self, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        post = PostFactory.create_post(
            session, post_model.PostCreate(content="first post", user_id=user.id)
        )

        assert post.content == "first post"
        assert post.user_id == user.id
