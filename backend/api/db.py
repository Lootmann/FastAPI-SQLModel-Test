from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "dev.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
