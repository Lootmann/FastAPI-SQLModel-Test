from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from api.cruds import users as user_api
from api.db import get_session
from api.models import users as user_model

router = APIRouter(tags=["users"])


@router.get(
    "/users",
    response_model=List[user_model.UserRead],
    status_code=status.HTTP_200_OK,
)
def read_all_users(*, db: Session = Depends(get_session)):
    return user_api.get_all_users(db)


@router.get(
    "/users/{user_id}",
    response_model=user_model.UserRead,
    status_code=status.HTTP_200_OK,
)
def get_user(*, db: Session = Depends(get_session), user_id: int):
    found = user_api.find_by_id(db, user_id)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id}: Not Found",
        )
    return found


@router.post(
    "/users",
    response_model=user_model.UserRead,
    status_code=status.HTTP_201_CREATED,
)
def create_user(*, db: Session = Depends(get_session), user: user_model.UserCreate):
    found = user_api.find_by_name(db, user.name)
    if found:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user.name}: Duplicate name",
        )
    return user_api.create_user(db, user)


@router.patch(
    "/users/{user_id}",
    response_model=user_model.UserRead,
    status_code=status.HTTP_200_OK,
)
def update_user(
    *,
    db: Session = Depends(get_session),
    user_id: int,
    user: user_model.UserUpdate,
):
    origin = user_api.find_by_id(db, user_id)
    if not origin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id}: Not Found",
        )
    return user_api.update_user(db, origin, user)


@router.delete("/users/{user_id}", response_model=None, status_code=status.HTTP_200_OK)
def delete_user(*, db: Session = Depends(get_session), user_id: int):
    origin = user_api.find_by_id(db, user_id)
    if not origin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id}: Not Found",
        )
    return user_api.delete_user(db, origin)
