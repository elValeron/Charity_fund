from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt
    invested_amount: int = 0

    class Config:
        schema_extra = {
            'example': {
                'name': 'Cat food for kitten',
                'description': 'Special food for kittens up to 6 months',
                'full_amount': 1000
            }
        }


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    create_date: datetime

    class Config:
        orm_mode = True
