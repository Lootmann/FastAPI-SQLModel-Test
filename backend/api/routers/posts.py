from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from api.cruds import posts as post_api
from api.db import get_session
from api.models import posts as post_model

router = APIRouter()


@router.get(
    "/posts",
    response_model=List[post_model.PostRead],
    status_code=status.HTTP_200_OK,
)
def read_all_posts(*, db: Session = Depends(get_session)):
    return post_api.get_all_posts(db)


@router.get(
    "/posts/{post_id}",
    response_model=post_model.PostRead,
    status_code=status.HTTP_200_OK,
)
def find_by_id(*, db: Session = Depends(get_session), post_id: int):
    found = post_api.find_by_id(db, post_id)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id}: Not Found",
        )
    return found


@router.post(
    "/posts",
    response_model=post_model.PostRead,
    status_code=status.HTTP_201_CREATED,
)
def create_post(*, db: Session = Depends(get_session), post: post_model.PostCreate):
    return post_api.create_post(db, post)


@router.patch(
    "/posts/{post_id}",
    response_model=post_model.PostRead,
    status_code=status.HTTP_200_OK,
)
def updated_post(
    *, db: Session = Depends(get_session), post: post_model.PostCreate, post_id: int
):
    original = post_api.find_by_id(db, post_id)
    if not original:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id}: Not Found",
        )

    if original.user_id != post.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Post {post_id}: Not Authenticated",
        )

    return post_api.update_post(db, original, post)
