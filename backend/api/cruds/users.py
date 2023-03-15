from typing import List

from sqlmodel import Session, select

from api.models.users import User, UserCreate, UserRead


def get_all_users(db: Session) -> List[UserRead]:
    return db.exec(select(User)).all()


def create_user(db: Session, user: UserCreate) -> UserRead:
    """
    Then we create a new Hero (this is the actual table model
    that saves things to the database) using Hero.from_orm().

    The method .from_orm() reads data from another object with attributes
    and creates a new instance of this class, in this case Hero.
    """
    db_user = User.from_orm(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
