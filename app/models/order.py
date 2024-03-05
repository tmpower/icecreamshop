from enum import Enum as StEnum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import User


class OrderStatus(str, StEnum):
    pending = 'pending'
    paid = 'paid'
    shipped = 'shipped'
    failed = 'failed'


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    items = Column(String, nullable=False)  # storing items as JSON string
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='orders')
