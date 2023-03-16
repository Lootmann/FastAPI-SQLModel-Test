from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from api.models.users import User


class PostBase(SQLModel):
    content: str = Field(index=True)
    # NOTE: All PostBase has user_id: int
    user_id: Optional[int] = Field(foreign_key="user.id")


class Post(PostBase, table=True):
    """
    A Post has A User
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    # NOTE: Only Table should have the relation !
    user: Optional["User"] = Relationship(back_populates="posts")


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int


class PostUpdate(PostBase):
    pass
