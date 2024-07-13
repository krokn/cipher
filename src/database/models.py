from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connection import Base
from sqlalchemy import ForeignKey, Enum
from src.schemas.settings import GlobalSettingsSchema
from src.schemas.levels import LevelSchema
from src.schemas.rating import RatingSchema
from src.schemas.users import UserSchema


class ModelUser(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(unique=True)
    subscription_status: Mapped[bool] = mapped_column(default=False)
    hearts: Mapped[int] = mapped_column(default=5)
    clue: Mapped[int] = mapped_column(default=1)

    rating = relationship("ModelRating", uselist=False, back_populates="user")

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            phone=self.phone,
            subscription_status=self.subscription_status,
            hearts=self.hearts,
            clue=self.clue,
        )


class ModelRating(Base):
    __tablename__ = 'rating'

    id: Mapped[int] = mapped_column(primary_key=True)
    current_level: Mapped[int] = mapped_column()
    reputation: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship("ModelUser", back_populates="rating")

    def to_read_model(self) -> RatingSchema:
        return RatingSchema(
            id=self.id,
            current_level=self.current_level,
            reputation=self.reputation,
            user_id=self.user_id,
        )


class GlobalSettings(Base):
    __tablename__ = 'settings'

    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column()

    def to_read_model(self) -> GlobalSettingsSchema:
        return GlobalSettingsSchema(
            key=self.key,
            value=self.value,
        )


class ModelLevel(Base):
    __tablename__ = 'levels'

    id: Mapped[int] = mapped_column(primary_key=True)
    code_length: Mapped[int] = mapped_column()
    hint: Mapped[int] = mapped_column()
    degree_hint: Mapped[int] = mapped_column()

    def to_read_model(self) -> LevelSchema:
        return LevelSchema(
            id=self.id,
            code_length=self.code_length,
            hint=self.hint,
            degree_hint=self.degree_hint,
        )


# class ModelPlatform(Base):
#     __tablename__ = 'platform'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(Enum("RuStore", "Билайн", "Tele2", name="platform_name"), unique=True)

