from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from api.cruds import posts as post_api
from api.cruds import tags as tag_api
from api.cruds import users as user_api
from api.db import get_session
from api.models import posts as post_model

router = APIRouter(tags=["posts"])


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
    # TODO: validation user_id
    if not user_api.find_by_id(db, post.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {post.user_id}: Not Found",
        )
    return post_api.create_post(db, post)


@router.post(
    "/posts/{post_id}/tags/{tag_id}",
    response_model=post_model.PostRead,
    status_code=status.HTTP_201_CREATED,
)
def add_tag(*, db: Session = Depends(get_session), post_id: int, tag_id: int):
    post = post_api.find_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id}: Not Found",
        )

    tag = tag_api.find_by_id(db, tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag {tag_id}: Not Found",
        )

    return post_api.add_tag(db, post, tag)


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


@router.delete("/posts/{post_id}", response_model=None, status_code=status.HTTP_200_OK)
def delete_post(*, db: Session = Depends(get_session), post_id: int):
    # TODO: get user id with authentications
    original = post_api.find_by_id(db, post_id)
    if not original:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id}: Not Found",
        )
    return post_api.delete_post(db, original)
