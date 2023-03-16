from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from api.models import posts as post_model
from api.models import tags as tag_model
from api.models import users as user_model
from tests.factory import PostFactory, TagFactory, UserFactory, random_string


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


class TestPostTag:
    def test_add_tag_post(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        post = PostFactory.create_post(
            session, post_model.PostCreate(content="first post", user_id=user.id)
        )
        tag = TagFactory.create_tag(session, tag_model.TagCreate(name="new tag"))

        resp = client.post(f"/posts/{post.id}/tags/{tag.id}")
        data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert data["id"] == post.id
        assert data["content"] == "first post"

    def test_add_many_tags_to_post(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        post = PostFactory.create_post(
            session, post_model.PostCreate(content="first post", user_id=user.id)
        )

        for _ in range(5):
            tag = TagFactory.create_tag(
                session, tag_model.TagCreate(name=random_string())
            )
            client.post(f"/posts/{post.id}/tags/{tag.id}")

        resp = client.get(f"/posts/{post.id}")
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data["id"] == post.id
        assert data["user_id"] == user.id
        assert data["content"] == post.content
        assert len(data["tags"]) == 5

    def test_add_tag_post_with_wrong_post_id(self, client: TestClient):
        resp = client.post("/posts/1000/tags/1")
        data = resp.json()

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "Post 1000: Not Found"}

    def test_add_tag_post_with_wrong_tag_id(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        post = PostFactory.create_post(
            session, post_model.PostCreate(content="first post", user_id=user.id)
        )

        resp = client.post(f"/posts/{post.id}/tags/100")
        data = resp.json()

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "Tag 100: Not Found"}


class TestPostFactory:
    def test_create_post_factory(self, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        post = PostFactory.create_post(
            session, post_model.PostCreate(content="first post", user_id=user.id)
        )

        assert post.content == "first post"
        assert post.user_id == user.id


class TestPatchPost:
    def test_update_post(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        post = PostFactory.create_post(
            session, post_model.PostCreate(content="first post", user_id=user.id)
        )

        resp = client.patch(
            f"/posts/{post.id}", json={"user_id": user.id, "content": "updated :^)"}
        )
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data["content"] == post.content
        assert data["content"] == "updated :^)"

    def test_update_post_with_wrong_post_id(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))

        resp = client.patch(
            f"/posts/123",
            json={"user_id": user.id, "content": "updated :^)"},
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_update_post_with_wrong_user_id(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        post = PostFactory.create_post(
            session, post_model.PostCreate(content="first post", user_id=user.id)
        )

        resp = client.patch(
            f"/posts/{post.id}",
            json={"user_id": user.id + 100, "content": "updated :^)"},
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


class TestDeletePost:
    def test_delete_post(self, client: TestClient, session: Session):
        user = UserFactory.create_user(session, user_model.UserCreate(name="hoge"))
        post = PostFactory.create_post(
            session, post_model.PostCreate(content="first post", user_id=user.id)
        )

        resp = client.delete(f"/posts/{post.id}")
        data = resp.json()
        assert data == None

    def test_delete_post_with_wrong_id(self, client: TestClient, session: Session):
        resp = client.delete("/posts/123")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
