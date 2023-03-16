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


@router.get(
    "/tags/{tag_id}",
    response_model=tag_model.TagRead,
    status_code=status.HTTP_200_OK,
)
def find_by_id(*, db: Session = Depends(get_session), tag_id: int):
    found = tag_api.find_by_id(db, tag_id)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag {tag_id}: Not Found",
        )
    return found


@router.post(
    "/tags",
    response_model=tag_model.TagRead,
    status_code=status.HTTP_201_CREATED,
)
def create_tag(*, db: Session = Depends(get_session), tag: tag_model.TagCreate):
    return tag_api.create_tag(db, tag)


@router.patch(
    "/tags/{tag_id}",
    response_model=tag_model.TagRead,
    status_code=status.HTTP_200_OK,
)
def update_tag(
    *, db: Session = Depends(get_session), tag_id: int, tag: tag_model.TagUpdate
):
    original = tag_api.find_by_id(db, tag_id)
    if not original:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag {tag_id}: Not Found",
        )

    if tag.name == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Tag: Should Not Empty",
        )

    return tag_api.update_tag(db, original, tag)


@router.delete("/tags/{tag_id}", response_model=None, status_code=status.HTTP_200_OK)
def delete_tag(*, db: Session = Depends(get_session), tag_id: int):
    found = tag_api.find_by_id(db, tag_id)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag {tag_id}: Not Found",
        )
    return tag_api.delete_tag(db, found)
