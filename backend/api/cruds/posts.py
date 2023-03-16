from typing import List

from sqlmodel import Session, select

from api.models import posts as post_model
from api.models import tags as tag_model


def get_all_posts(db: Session) -> List[post_model.PostRead]:
    return db.exec(select(post_model.Post)).all()


def find_by_id(db: Session, post_id: int) -> post_model.PostRead | None:
    stmt = select(post_model.Post).where(post_model.Post.id == post_id)
    return db.exec(stmt).first()


def create_post(db: Session, post: post_model.PostCreate) -> post_model.PostRead:
    db_post = post_model.Post.from_orm(post)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def add_tag(db: Session, post: post_model.Post, tag: tag_model.Tag) -> post_model.Post:
    post.tags.append(tag)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(
    db: Session, original: post_model.Post, post: post_model.PostUpdate
) -> post_model.PostRead:
    original.content = post.content
    db.add(original)
    db.commit()
    db.refresh(original)
    return original


def delete_post(db: Session, post: post_model.Post) -> None:
    db.delete(post)
    db.commit()
    return
