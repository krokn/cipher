import datetime

from pydantic import BaseModel


class SubscriptionSchema(BaseModel):
    id: int = 0
    user_id: int = 0
    gift_id: int = 1
    updated_at: datetime.datetime = '2024-07-16 16:18:38.782'
