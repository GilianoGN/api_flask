import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from .basemodel import db

class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'))
    created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"