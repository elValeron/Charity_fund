from datetime import datetime


from app.models import CharityDonationBaseModel


def invest(
        target: CharityDonationBaseModel,
        sources: list[CharityDonationBaseModel],
) -> list[CharityDonationBaseModel]:
    updated = []

    for source in sources:
        min_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for modified in (source, target):
            modified.invested_amount += min_amount
            if modified.full_amount == modified.invested_amount:
                modified.fully_invested = True
                modified.close_date = datetime.now()
        updated.append(source)
        if target.fully_invested:
            break
    return updated
