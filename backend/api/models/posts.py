from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.models.users import User


class PostBase(SQLModel):
    content: str = Field(index=True)


class Post(PostBase, table=True):
    """
    A Post has A User
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="posts")


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    user: Optional["User"]


class PostUpdate(PostBase):
    pass
