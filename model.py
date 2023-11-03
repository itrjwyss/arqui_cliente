from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Double, Integer, Date, Boolean
from database import Base


class Customer(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    frequent = Column(Boolean)
    points = Column(Double)


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20))
    day = Column(Date)
    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship("Customer")
