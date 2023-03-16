from typing import List

from sqlmodel import Session, select

from api.models import tags as tag_model


def get_all_tags(db: Session) -> List[tag_model.TagRead]:
    return db.exec(select(tag_model.Tag)).all()


def create_tag(db: Session, tag: tag_model.TagCreate) -> tag_model.TagRead:
    db_tag = tag_model.Tag.from_orm(tag)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag
