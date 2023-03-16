from typing import List

from sqlmodel import Session, select

from api.models import posts as post_model


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
