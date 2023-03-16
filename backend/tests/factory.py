from random import randint, sample
from string import ascii_letters

from sqlmodel import Session

from api.models import posts as post_model
from api.models import tags as tag_model
from api.models import users as user_model


def random_string(min_: int = 5, max_: int = 10) -> str:
    s = ascii_letters
    while max_ > len(s):
        s += s
    return "".join(sample(s, randint(min_, max_)))


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


class TagFactory:
    @staticmethod
    def create_tag(db: Session, tag: tag_model.TagCreate) -> tag_model.TagRead:
        db_tag = tag_model.Tag.from_orm(tag)
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag
