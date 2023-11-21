from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import pandas as pd
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app =Flask(__name__)

#DBファイル作成
base_dir = os.path.dirname(__file__)
database = "sqlite:///" + os.path.join(base_dir, 'data.sqlite')

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = False


#基本クラス作成
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

#モデル宣言
#サブクラス作成
class Contract(db.Model):
    
    id: Mapped[int] = mapped_column(primary_key=True)
    period_id: Mapped[int] = mapped_column(ForeignKey("Period.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("Customer.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    contract_number: Mapped[int]
    contract_situationm: Mapped[str]

    period : Mapped[list["Period"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )

    customer : Mapped[list["Customer"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )

    product : Mapped[list["Product"]] = relationship(
        back_populates="contract", cascade="all, delete-orphan"
    )


class Period(db.Model):
    

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


class Week(db.Model):
   

    week: Mapped[str] = mapped_column(primary_key=True)

    period : Mapped[list["Period"]] = relationship(back_populates="weeks")


class Week_day(db.Model):
    

    week_day: Mapped[str] = mapped_column(primary_key=True)

    period : Mapped[list["Period"]] = relationship(back_populates="week_days")


class Customer(db.Model):
    

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str]
    telephon_number: Mapped[int]

    contract : Mapped["Contract"] = relationship(back_populates="customer")


class Product(db.Model):
    

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str]
    product_price:Mapped[int]

    contract : Mapped[list[Contract]] = relationship(back_populates="product")


class Pay(db.Model):
    

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


class Pay_methood(db.Model):
    

    id: Mapped[int] = mapped_column(primary_key=True)
    pay_methood_name: Mapped[str]

    pay : Mapped[list["Pay"]] = relationship(back_populates="pay_methood")

with app.app_context():
    db.create_all()
