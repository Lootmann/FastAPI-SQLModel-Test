from sqlmodel import Session

from api.models import users as user_model


class UserFactory:
    @staticmethod
    def create_user(db: Session, user: user_model.UserCreate) -> user_model.UserRead:
        """
        NOTE: Consider whether the arguments of this function should be UserCreate or name="hoge"
        """
        db_user = user_model.UserTable.from_orm(user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
