from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from api.models.posts_tags import PostTagLink

if TYPE_CHECKING:
    from api.models.posts import Post


class TagBase(SQLModel):
    name: str = Field(index=True)


class Tag(TagBase, table=True):
    """
    Many Tags have Many Post
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    posts: List["Post"] = Relationship(back_populates="tags", link_model=PostTagLink)


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int


class TagUpdate(TagBase):
    pass
