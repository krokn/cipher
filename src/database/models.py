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


class ModelUser(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_platform: Mapped[int] = mapped_column(ForeignKey("platform.id"))
    identifier: Mapped[str] = mapped_column(unique=True)
    hearts: Mapped[int] = mapped_column(default=5)
    clue: Mapped[int] = mapped_column(default=1)

    rating = relationship('ModelRating', back_populates='user')
    subscriptions = relationship('ModelSubscription', back_populates='user')

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            id_platform=self.id_platform,
            identifier=self.identifier,
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


class ModelPlatform(Base):
    __tablename__ = 'platform'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    def to_read_model(self) -> PlatfromSchema:
        return PlatfromSchema(
            id=self.id,
            name=self.name
        )


class ModelGift(Base):
    __tablename__ = 'gifts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hearts: Mapped[int] = mapped_column(default=0)
    clue: Mapped[int] = mapped_column(default=0)

    def to_read_model(self) -> GiftSchema:
        return GiftSchema(
            id=self.id,
            name=self.name,
            hearts=self.hearts,
            clue=self.clue,
        )


class ModelSubscription(Base):
    __tablename__ = 'subscription'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    gift_id: Mapped[int] = mapped_column(ForeignKey("gifts.id"), primary_key=True)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    user = relationship('ModelUser', back_populates='subscriptions')

    def to_read_model(self) -> SubscriptionSchema:
        return SubscriptionSchema(
            id=self.id,
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
