from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, PositiveInt


class Flavor(str, Enum):
    chocolate = 'chocolate'
    vanilla = 'vanilla'
    strawberry = 'strawberry'


class Item(BaseModel):
    flavor: Flavor
    amount: PositiveInt


class OrderCreateIcecream(BaseModel):
    address: str
    items: List[Item]

    class Config:
        orm_mode = True

    def to_dict(self) -> Dict:
        return self.model_dump(by_alias=True, exclude_unset=True)

    def to_json(self) -> str:
        return self.model_dump_json(by_alias=True, exclude_unset=True)

class OrderResponseIceCream(BaseModel):
    id: int
    status: str
