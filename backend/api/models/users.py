from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.models.posts import Post


class UserBase(SQLModel):
    name: str = Field(index=True)


class User(UserBase, table=True):
    """
    A User has Many Posts
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    posts: List["Post"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    posts: List["Post"] = Relationship(back_populates="User")


class UserUpdate(UserBase):
    pass
