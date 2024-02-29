from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint
from sqlalchemy.sql import false

from app.core.db import Base


class CharityDonationBaseModel(Base):

    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('full_amount >= invested_amount > 0')
    )

    id = Column(Integer, primary_key=True,)
    full_amount = Column(Integer, default=0, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=false())
    create_date = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    close_date = Column(DateTime(timezone=True))

    def __repr__(self):
        return (
            f'Создан {type(self).__name__} со значениями полей:\n'
            f'id: {self.id},\n'
            f'full_amount: {self.full_amount},\n'
            f'invested_amount: {self.invested_amount}\n'
            f'create_date: {self.create_date}'
        )
