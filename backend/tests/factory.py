from sqlmodel import Session

from api.models.users import User, UserCreate, UserRead


class UserFactory:
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> UserRead:
        """
        NOTE: Consider whether the arguments of this function should be UserCreate or name="hoge"
        """
        db_user = User.from_orm(user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
