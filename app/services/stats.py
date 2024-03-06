from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stats import Stats


async def update_stats(items: List[dict], session: AsyncSession) -> None:
    for item in items:
        query_str = select(Stats).filter(Stats.flavor == item['flavor'])
        result = await session.execute(query_str)
        stats = result.scalars().first()

        if not stats:
            stats = Stats(flavor=item['flavor'], count=item['amount'])
            session.add(stats)
        else:
            stats.count += item['amount']

    await session.commit()
    await session.refresh(stats)


async def get_stats(session: AsyncSession) -> List[Stats]:
    query_str = select(Stats)
    result = await session.execute(query_str)
    return result.scalars().all()
