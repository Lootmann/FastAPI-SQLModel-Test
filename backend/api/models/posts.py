from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from api.models.posts_tags import PostTagLink
from api.models.tags import Tag

if TYPE_CHECKING:
    from api.models.tags import Tag
    from api.models.users import User


class PostBase(SQLModel):
    content: str = Field(index=True)
    user_id: Optional[int] = Field(foreign_key="user.id")


class Post(PostBase, table=True):
    """
    A Post has A User
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    user: Optional["User"] = Relationship(back_populates="posts")
    tags: List["Tag"] = Relationship(back_populates="posts", link_model=PostTagLink)


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    tags: List["Tag"] = Field(default=None)


class PostUpdate(PostBase):
    pass
