from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.connection import Base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean

from src.schemas.levels import LevelSchema
from src.schemas.rating import RatingSchema
from src.schemas.users import UserSchema


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column()
    subscription_status: Mapped[bool] = mapped_column(default=False)
    hearts: Mapped[int] = mapped_column(default=0)
    clue: Mapped[int] = mapped_column(default=0)

    rating: Mapped["Rating"] = relationship("Rating", uselist=False, back_populates="user")

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            phone=self.phone,
            subscription_status=self.subscription_status,
            hearts=self.hearts,
            clue=self.clue,
        )


class Rating(Base):
    __tablename__ = 'rating'

    id: Mapped[int] = mapped_column(primary_key=True)
    current_level: Mapped[int] = mapped_column()
    reputation: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="rating")

    def to_read_model(self) -> RatingSchema:
        return RatingSchema(
            id=self.id,
            current_level=self.current_level,
            reputation=self.reputation,
            user_id=self.user_id,
        )


class Level(Base):
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True)
    code_length = Column(Integer)
    hint = Column(Integer)
    degree_hint = Column(Integer)

    def to_read_model(self) -> LevelSchema:
        return LevelSchema(
            id=self.id,
            code_length=self.code_length,
            hint=self.hint,
            degree_hint=self.degree_hint,
        )