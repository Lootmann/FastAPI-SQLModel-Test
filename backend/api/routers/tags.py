from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from api.cruds import tags as tag_api
from api.db import get_session
from api.models import tags as tag_model

router = APIRouter(tags=["tags"])


@router.get(
    "/tags",
    response_model=List[tag_model.TagRead],
    status_code=status.HTTP_200_OK,
)
def read_all_tags(*, db: Session = Depends(get_session)):
    return tag_api.get_all_tags(db)


@router.post(
    "/tags",
    response_model=tag_model.TagRead,
    status_code=status.HTTP_201_CREATED,
)
def create_tag(*, db: Session = Depends(get_session), tag: tag_model.TagCreate):
    return tag_api.create_tag(db, tag)
