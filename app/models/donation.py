from sqlalchemy import Column, Integer, ForeignKey, Text

from .base import CharityDonationBaseModel


class Donation(CharityDonationBaseModel):

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return (
            f'{super().__repr__()},\n'
            f'user_id: {self.user_id},\n'
            f'comment: {self.comment}.'
        )
