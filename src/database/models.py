import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum, String, DateTime, func
from src.database.connection import Base
from src.schemas.gift import GiftSchema
from src.schemas.platform import PlatfromSchema
from src.schemas.settings import GlobalSettingsSchema
from src.schemas.levels import LevelSchema
from src.schemas.rating import RatingSchema
from src.schemas.subscription import SubscriptionSchema
from src.schemas.users import UserSchema


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str] = mapped_column(unique=True)
    hearts: Mapped[int] = mapped_column(default=0)
    clue: Mapped[int] = mapped_column(default=0)
    level_id: Mapped[int] = mapped_column(ForeignKey('levels.id'), default=1)
    id_platform: Mapped[int] = mapped_column(ForeignKey("platform.id"))

    platform: Mapped["PlatformModel"] = relationship('PlatformModel', uselist=False, lazy="joined")
    rating_forever: Mapped["RatingModelForever"] = relationship('RatingModelForever', back_populates='user',
                                                                uselist=False, lazy="joined")
    rating_week: Mapped["RatingModelWeek"] = relationship('RatingModelWeek', back_populates='user', uselist=False, lazy="joined")
    rating_month: Mapped["RatingModelMonth"] = relationship('RatingModelMonth', back_populates='user', uselist=False, lazy="joined")
    subscriptions: Mapped["SubscriptionModel"] = relationship('SubscriptionModel', back_populates='user', uselist=False, lazy="joined")
    level_rel: Mapped["LevelModel"] = relationship('LevelModel', back_populates='user', uselist=False, lazy="joined")

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            id_platform=self.id_platform,
            identifier=self.identifier,
            hearts=self.hearts,
            clue=self.clue,
            level_id=self.level_id
        )


class RatingModelMonth(Base):
    __tablename__ = 'rating-month'

    id: Mapped[int] = mapped_column(primary_key=True)
    reputation: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="rating_month", uselist=False, lazy="joined")

    def to_read_model(self) -> RatingSchema:
        return RatingSchema(
            id=self.id,
            reputation=self.reputation,
            user_id=self.user_id,
        )


class RatingModelWeek(Base):
    __tablename__ = 'rating-week'

    id: Mapped[int] = mapped_column(primary_key=True)
    reputation: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="rating_week", uselist=False, lazy="joined")

    def to_read_model(self) -> RatingSchema:
        return RatingSchema(
            id=self.id,
            reputation=self.reputation,
            user_id=self.user_id,
        )


class RatingModelForever(Base):
    __tablename__ = 'rating-forever'

    id: Mapped[int] = mapped_column(primary_key=True)
    reputation: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="rating_forever", uselist=False, lazy="joined")

    def to_read_model(self) -> RatingSchema:
        return RatingSchema(
            id=self.id,
            reputation=self.reputation,
            user_id=self.user_id,
        )


class PlatformModel(Base):
    __tablename__ = 'platform'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    def to_read_model(self) -> PlatfromSchema:
        return PlatfromSchema(
            id=self.id,
            name=self.name
        )


class GiftModel(Base):
    __tablename__ = 'gifts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hearts: Mapped[int] = mapped_column(default=0)
    clue: Mapped[int] = mapped_column(default=0)

    subscriptions: Mapped["SubscriptionModel"] = relationship('SubscriptionModel', back_populates='gift', uselist=False, lazy="joined")

    def to_read_model(self) -> GiftSchema:
        return GiftSchema(
            id=self.id,
            name=self.name,
            hearts=self.hearts,
            clue=self.clue,
        )


class SubscriptionModel(Base):
    __tablename__ = 'subscription'

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    gift_id: Mapped[int] = mapped_column(ForeignKey("gifts.id"), primary_key=True)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["UserModel"] = relationship('UserModel', back_populates='subscriptions', uselist=False, lazy="joined")
    gift: Mapped["GiftModel"] = relationship('GiftModel', back_populates='subscriptions', uselist=False, lazy="joined")

    def to_read_model(self) -> SubscriptionSchema:
        return SubscriptionSchema(
            user_id=self.user_id,
            gift_id=self.gift_id,
            updated_at=self.updated_at
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


class LevelModel(Base):
    __tablename__ = 'levels'

    id: Mapped[int] = mapped_column(primary_key=True)
    code_length: Mapped[int] = mapped_column()
    attempts: Mapped[int] = mapped_column()
    degree_hint: Mapped[int] = mapped_column()

    user: Mapped["UserModel"] = relationship('UserModel', back_populates='level_rel', uselist=False, lazy="joined")

    def to_read_model(self) -> LevelSchema:
        return LevelSchema(
            id=self.id,
            code_length=self.code_length,
            attempts=self.attempts,
            degree_hint=self.degree_hint,
        )
