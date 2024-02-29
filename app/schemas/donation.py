from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBaseSchema(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBaseSchema):
    invested_amount: int = 0
    fully_invested: bool = False

    class Config:
        schema_extra = {
            'example': {
                'comment': 'this is not a required field',
                'full_amount': 1500,
                'invested_amount': 0
            }
        }


class DonationDB(DonationBaseSchema):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBLong(DonationDB):
    fully_invested: bool
    user_id: int
    invested_amount: int
