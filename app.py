from sqlalchemy import create_engine,Column, Integer, String, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

#基本クラス作成
class Base(declarative_base):
    pass

#モデル宣言
#サブクラス作成
class Contract(Base):
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

    product : Mapped[list["Product"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )


class Period(Base):
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


class Week(Base):
    __tablemame__ = "weeks"

    week: Mapped[str] = mapped_column(primary_key=True)

    period : Mapped[list["Period"]] = relationship(back_populates="weeks")


class Week_day(Base):
    __tablename__ = "week_days"

    week_day: Mapped[str] = mapped_column(primary_key=True)

    period : Mapped[list["Period"]] = relationship(back_populates="week_days")


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(str(15))
    telephon_number: Mapped[int] = mapped_column(int(12))

    contract : Mapped["Contract"] = relationship(back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(str(40))
    product_price:Mapped[int] = mapped_column(int(5))

    contract : Mapped[list[Contract]] = relationship(back_populates="product")


class Pay(Base):
    __tablename__ = "pay"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))#この行はいらないかも？
    contract_id : Mapped[int] = mapped_column(ForeignKey("contracts.id"))
    pay_methood_id : Mapped[int] = mapped_column(ForeignKey("pay_methood.id"))
    #pay_total消した

    customer : Mapped[list[Customer]] = relationship(
        back_populates="pay", cascade="all, delete-orphan"
    )

    contract : Mapped[list[Contract]] = relationship(
        back_populates="pay", cascade="all, delete-orphan"
    )

    pay_methood : Mapped[list["Pay_methood"]] = relationship(
        back_populates = "pay", cascade="all, delete-orphan"
    )


class Pay_methood(Base):
    __tablename__ = "pay_methood"

    id: Mapped[int] = mapped_column(primary_key=True)
    pay_methood_name: Mapped[str]

    pay : Mapped[list["Pay"]] = relationship(back_populates="pay_methood")