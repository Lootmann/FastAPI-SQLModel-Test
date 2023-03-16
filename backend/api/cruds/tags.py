from typing import List

from sqlmodel import Session, select

from api.models import tags as tag_model


def get_all_tags(db: Session) -> List[tag_model.TagRead]:
    return db.exec(select(tag_model.Tag)).all()
