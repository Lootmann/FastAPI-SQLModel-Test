from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from api.cruds import users as user_api
from api.db import get_session
from api.models.users import UserCreate, UserRead

router = APIRouter()


@router.get("/users", response_model=List[UserRead], status_code=status.HTTP_200_OK)
def read_all_users(*, db: Session = Depends(get_session)):
    return user_api.get_all_users(db)


@router.post("/users", response_model=UserRead, status_code=status.HTTP_200_OK)
def create_user(*, db: Session = Depends(get_session), user: UserCreate):
    return user_api.create_user(db, user)
