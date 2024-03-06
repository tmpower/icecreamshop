from pydantic import BaseModel, PositiveInt

from app.schemas.order import Flavor


class StatsResponse(BaseModel):
    id: int
    flavor: Flavor
    count: PositiveInt
