from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass

class User_Model(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

class Admin_Model(Base):
    __tablename__ = "admins"
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

class transaction_model(Base):
    __tablename__ = "transactions"  
    id: Mapped[int] = mapped_column(primary_key=True)
    sender: Mapped[int] = mapped_column(nullable=False)
    recipient: Mapped[int] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)