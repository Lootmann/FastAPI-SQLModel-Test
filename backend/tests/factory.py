from sqlmodel import Session

from api.models import posts as post_model
from api.models import users as user_model


class UserFactory:
    @staticmethod
    def create_user(db: Session, user: user_model.UserCreate) -> user_model.UserRead:
        """
        NOTE: Consider whether the arguments of this function should be UserCreate or name="hoge"
        """
        db_user = user_model.User.from_orm(user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


class PostFactory:
    @staticmethod
    def create_post(db: Session, post: post_model.PostCreate) -> post_model.PostRead:
        db_post = post_model.Post.from_orm(post)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
