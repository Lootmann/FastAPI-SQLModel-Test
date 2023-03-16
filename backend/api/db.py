from sqlmodel import Session, create_engine

from api.models.posts import Post
from api.models.users import User

sqlite_file_name = "dev.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    # TODO: SQLModel.metadata doesn't work D:
    User.metadata.drop_all(engine)
    User.metadata.create_all(engine)

    Post.metadata.drop_all(engine)
    Post.metadata.create_all(engine)
