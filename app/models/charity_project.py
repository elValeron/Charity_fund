from sqlalchemy import Column, String

from .base import CharityDonationBaseModel


class CharityProject(CharityDonationBaseModel):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String, nullable=False)

    def __repr__(self) -> str:
        return (
            f'{super().__repr__()},\n'
            f'name: {self.name},\n'
            f'description: {self.description}.'
        )
