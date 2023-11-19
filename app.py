from sqlalchemy import create_engine,Column, Integer, String, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class base(declarative_base):
    pass
#DB---Contract
class Contract:
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    period_id: Mapped[int] = mapped_column(ForeignKey("period.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    contract_number: Mapped[int]
    contract_situationm: Mapped[str] = mapped_column(str(30))

    period : Mapped[list["Period"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )

    customer : Mapped[list["Customer"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )


class Period:
    __tablename__ = "period"

    id: Mapped[int] = mapped_column(primary_key=True)
    week : Mapped[str] = mapped_column(ForeignKey("weeks.week"))
    week_days : Mapped[str] = mapped_column(ForeignKey("week_days.week_day"))

    contract: Mapped["Contract"] = relationship(back_populates="period")
    week : Mapped[list["Week"]] = relationship(
        back_populates="period", cascade="all, delete-orphan"
    )
    week_days : Mapped[list["Week_day"]] = relationship(
        back_populates="period", cascade="all, delete-orphan"
    )

class Week:
    __tablemame__ = "weeks"

    week: Mapped[str] = mapped_column(primary_key=True)

    period : Mapped[list["Period"]] = relationship(back_populates="weeks")

class Week_day:
    __tablename__ = "week_days"

    week_day: Mapped[str] = mapped_column(primary_key=True)

    period : Mapped[list["Period"]] = relationship(back_populates="week_days")

class Customer:
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(str(15))
    telephon_number: Mapped[int] = mapped_column(int(12))

    contract : Mapped[Contract] = relationship(back_populates="customer")

