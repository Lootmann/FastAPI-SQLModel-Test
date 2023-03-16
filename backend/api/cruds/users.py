from typing import List

from sqlmodel import Session, select

from api.models import users as user_model


def get_all_users(db: Session) -> List[user_model.UserRead]:
    return db.exec(select(user_model.UserTable)).all()


def find_by_id(db: Session, user_id: int) -> user_model.UserRead | None:
    stmt = select(user_model.UserTable).where(user_model.UserTable.id == user_id)
    return db.exec(stmt).first()


def create_user(db: Session, user: user_model.UserCreate) -> user_model.UserRead:
    """
    Then we create a new Hero (this is the actual table model
    that saves things to the database) using Hero.from_orm().

    The method .from_orm() reads data from another object with attributes
    and creates a new instance of this class, in this case Hero.
    """
    db_user = user_model.UserTable.from_orm(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session, origin: user_model.UserTable, user: user_model.UserUpdate
) -> user_model.UserRead:
    if user.name != "":
        origin.name = user.name

    db.add(origin)
    db.commit()
    db.refresh(origin)
    return origin


def delete_user(db: Session, origin: user_model.UserTable) -> None:
    db.delete(origin)
    db.commit()
    return
