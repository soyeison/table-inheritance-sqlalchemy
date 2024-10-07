from typing import List
from typing import Optional
from sqlalchemy import (
    String,
    Column,
    Integer,
    Float,
    ForeignKey,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base, sessionmaker
from enum import Enum


Base = declarative_base()
engine = create_engine("sqlite:///./test_db.db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class AccountTypeEnum(Enum):
    SAVING = "saving"
    CURRENT = "current"
    DOLLARS = "dollars_account"


class Account(Base):
    __tablename__ = "account"

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(Integer, default=0)
    account_type = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "account",
        "polymorphic_on": account_type,
    }


class SavingAccount(Account):
    __tablename__ = "saving_account"

    account_id = Column(Integer, ForeignKey("account.account_id"), primary_key=True)
    interest_rate = Column(Float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "saving_account",
    }


class CurrentAccount(Account):
    __tablename__ = "current_account"

    account_id = Column(Integer, ForeignKey("account.account_id"), primary_key=True)
    overdraft_limit = Column(Float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "current_account",
    }


Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    db = SessionLocal()

    # Crear la cuenta de ahorros
    """ savings_account = SavingAccount(balance=1000, interest_rate=3.5)

    db.add(savings_account)
    db.commit()
    db.refresh(savings_account) """

    # Consultas polimorficas
    accounts = db.query(Account).all()

    for account in accounts:
        if isinstance(account, SavingAccount):
            print("Instanbcia de saving")
            print("account_type:", account.account_type)
            print("interest_rate:", account.interest_rate)
        elif isinstance(account, CurrentAccount):
            print("Instancia de current")

    db.close()
