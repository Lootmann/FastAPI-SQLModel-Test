from typing import Optional

from sqlmodel import Field, SQLModel


class PostTagLink(SQLModel, table=True):
    """
    PostTabLink : JOIN Table

    Post : Tag = N : N
    """

    post_id: Optional[int] = Field(
        default=None,
        foreign_key="post.id",
        primary_key=True,
    )

    tag_id: Optional[int] = Field(
        default=None,
        foreign_key="tag.id",
        primary_key=True,
    )
