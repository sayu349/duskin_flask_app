from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import pandas as pd
import os
from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from sqlalchemy import select, distinct, func, join, where

app =Flask(__name__)

#DBファイル設定
base_dir = os.path.dirname(__file__)
database = "sqlite:///" + os.path.join(base_dir, 'data.sqlite')

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = False


#基本クラス作成
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app)

Migrate(app, db)
#モデル宣言
#サブクラス作成
class Contract(db.Model):
    
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    period_id: Mapped[int] = mapped_column(ForeignKey("Period.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("Customer.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("Product.id"))
    contract_number: Mapped[int]
    contract_situationm: Mapped[str]

    period : Mapped[list["Period"]] = relationship(
        back_populates="contracts", cascade="all, delete-orphan"
    )

    customer : Mapped[list["Customer"]] = relationship(
        back_populates="contracts", cascade="all, delete-orphan"
    )

    product : Mapped[list["Product"]] = relationship(
        back_populates="contracts", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f'契約ID:{self.id}周期ID:{self.period_id}顧客ID{self.customer_id}商品ID:{self.product_id}契約数:{self.contract_number}契約状況:{self.contract_situationm}'


class Period(db.Model):
    
    __tablename__ = "period"

    id: Mapped[int] = mapped_column(primary_key=True)
    week : Mapped[str] = mapped_column(ForeignKey("weeks.week"))
    week_days : Mapped[str] = mapped_column(ForeignKey("week_days.week_day"))

    contracts: Mapped[list["Contract"]] = relationship(back_populates="period")
    
    weeks : Mapped[list["Week"]] = relationship(
        back_populates="period", cascade="all, delete-orphan"
    )

    week_days : Mapped[list["Week_day"]] = relationship(
        back_populates="period", cascade="all, delete-orphan"
    )
    def __str__(self):
        return f'周期ID:{self.id}週:{self.weeks}曜日:{self.week_days}'


class Week(db.Model):
   
    __tablename__ = "weeks"

    week: Mapped[str] = mapped_column(primary_key=True)

    period : Mapped[list["Period"]] = relationship(back_populates="weeks")

    def __str__(self):
        return f'週{self.week}'


class Week_day(db.Model):

    __tablename__ = "week_days"
    
    week_day: Mapped[str] = mapped_column(primary_key=True)

    period : Mapped[list["Period"]] = relationship(back_populates="week_days")

    def __str__(self):
        return f'曜日:{self.week_day}'


class Customer(db.Model):
    
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str]
    telephon_number: Mapped[int]

    contracts : Mapped["Contract"] = relationship(back_populates="customer")

    def __str__(self):
        return f'顧客ID:{self.id}顧客名:{self.customer_name}電話番号:{self.telephon_number}'


class Product(db.Model):
    
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str]
    product_price:Mapped[int]

    contracts : Mapped[list[Contract]] = relationship(back_populates="product")

    def __str__(self):
        return f'商品ID:{id}商品名:{self.product_name}商品価格:{self.product_price}'


class Pay(db.Model):
    
    __tablename__ = "pays"

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

    def __str__(self):
        return f'支払ID:{self.id}顧客ID:{self.customer_id}契約ID:{self.contract_id}支払方法ID:{self.pay_methood_id}'


class Pay_methood(db.Model):
    
    __tablename__ = "pay_methood"

    id: Mapped[int] = mapped_column(primary_key=True)
    pay_methood_name: Mapped[str]

    pay : Mapped[list["Pay"]] = relationship(back_populates="pay_methood")

    def __str__(self):
        return f'支払方法ID:{self.id}支払方法:{self.pay_methood_name}'


@app.route("/")
def index():
        
    money_customer_total = db.session.execute(db
        .select(Contract.contract_number)*(Product.product_price)
        .join(Product)
        .where(Contract.contract_situationm == "解約済み")
        )

    return render_template("index.html", money_customer_total=money_customer_total)


@app.route("/period_contract/<int:period>", methoods=['POST'])
def period():
    period_by_contract_list = db.session.execute(db
        .select(Contract)
        .where(Contract.contract_situationm == "解約済み")
        .where(Contract.period_id == request.form(period))
        .order_by(Contract.customer_id)
        )
    
    customer_by_contract_cutomer_total = db.session.execute(db
        .select(sum(Product.product_price * Contract.contract_number), Customer)
        .join(Product)
        .join(Customer)
        .where(Contract.contract_situationm == "解約済み")
        .where(Contract.period_id == request.form(period))
        .group_by(Contract.customer_id)
        )
    
    period_by_contract_cutomer_total = db.session.execute(db
        .select(sum(Product.product_price * Contract.contract_number)), func.count(distinct(Contract.customer_id))
        .join(Product)
        .join(Customer)
        .where(Contract.contract_situationm == "解約済み")
        .where(Contract.period_id == request.form(period))
        )


    return render_template("period_contract_list.html", period_by_contract_list=period_by_contract_list ,
                            customer_by_contract_cutomer_total=customer_by_contract_cutomer_total ,
                            period_by_contract_cutomer_total=period_by_contract_cutomer_total)


if __name__ == '__main__':
    app.run()