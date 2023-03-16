from typing import List

from sqlmodel import Session, select

from api.models import tags as tag_model


def get_all_tags(db: Session) -> List[tag_model.TagRead]:
    return db.exec(select(tag_model.Tag)).all()


def find_by_id(db: Session, tag_id) -> tag_model.TagRead | None:
    stmt = select(tag_model.Tag).where(tag_model.Tag.id == tag_id)
    return db.exec(stmt).first()


def create_tag(db: Session, tag: tag_model.TagCreate) -> tag_model.TagRead:
    db_tag = tag_model.Tag.from_orm(tag)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag: tag_model.TagRead) -> None:
    db.delete(tag)
    db.commit()
    return
