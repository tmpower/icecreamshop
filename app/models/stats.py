from sqlalchemy import Column, Enum, Integer

from app.database import Base
from app.schemas.order import Flavor


class Stats(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True, index=True)
    flavor = Column(Enum(Flavor), unique=True, nullable=False)
    count = Column(Integer, default=0, nullable=False)
