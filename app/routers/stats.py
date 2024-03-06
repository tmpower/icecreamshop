from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.services.stats import get_stats
from app.schemas.stats import StatsResponse


router = APIRouter()


@router.get('/stats', response_model=List[StatsResponse])
async def get_stats_endpoint(session: AsyncSession = Depends(get_async_session)):
    stats_list = await get_stats(session)
    return stats_list
