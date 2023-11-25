from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
import pandas as pd
import os
from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import select, distinct, func

app = Flask(__name__)

#DBファイル設定
app.config['SECRET_KEY'] = os.urandom(24)
base_dir = os.path.dirname(__file__)
database = "sqlite:///" + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#基本クラス作成
class Base(DeclarativeBase):
    pass



Migrate(app, db)
#モデル宣言
#サブクラス作成
class Contract(db.Model):
    
    __tablename__ = "contracts"

    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.Integer, db.ForeignKey("period.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    contract_number = db.Column(db.Integer)
    contract_situationm = db.Column(db.String)

    #主リレーション
    pay = db.relationship("Pay", back_populates = "contracts", lazy=True)

    #外部リレーション
    period = db.relationship("Period", back_populates = "contracts")
    customers = db.relationship("Customer", back_populates = "contracts")
    products = db.relationship("Product", back_populates = "contracts")

    def __str__(self):
        return f'契約ID:{self.id}周期ID:{self.period_id}顧客ID{self.customer_id}商品ID:{self.product_id}契約数:{self.contract_number}契約状況:{self.contract_situationm}'


class Period(db.Model):
    
    __tablename__ = "period"

    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.String, db.ForeignKey("weeks.week"))
    week_day = db.Column(db.String,db.ForeignKey("week_days.week_day"))

    #主リレーション
    contracts = db.relationship("Contract", back_populates="period", lazy=True)

    #外部リレーション
    weeks = db.relationship("Week", back_populates = "period")
    week_days = db.relationship("Week_day", back_populates = "week_days")
  
    def __str__(self):
        return f'周期ID:{self.id}週:{self.weeks}曜日:{self.week_days}'


class Week(db.Model):
   
    __tablename__ = "weeks"

    week= db.Column(db.String, primary_key=True)

    #主リレーション
    period = db.relationship("Period",back_populates="weeks", lazy=True)

    def __str__(self):
        return f'週{self.week}'


class Week_day(db.Model):

    __tablename__ = "week_days"
    
    week_day= db.Column(db.String, primary_key=True)

    #主リレーション
    period = db.relationship("Period",back_populates="week_days", lazy=True)

    def __str__(self):
        return f'曜日:{self.week_day}'


class Customer(db.Model):
    
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String)
    telephon_number = db.Column(db.Integer)

    #主リレーション
    contracts = db.relationship("Contract", back_populates="customer", lazy=True)
    pay = db.relationship("Pay", back_populates = "customers", lazy=True)

    def __str__(self):
        return f'顧客ID:{self.id}顧客名:{self.customer_name}電話番号:{self.telephon_number}'


class Product(db.Model):
    
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    product_price = db.Column(db.Integer)

    #主リレーション
    contracts = db.relationship("contracts", back_populates="product", lazy=True)

    def __str__(self):
        return f'商品ID:{id}商品名:{self.product_name}商品価格:{self.product_price}'


class Pay(db.Model):
    
    __tablename__ = "pays"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))#この行はいらないかも？
    contract_id  = db.Column(db.Integer, db.ForeignKey("contracts.id"))
    pay_method_id  = db.Column(db.Integer, db.ForeignKey("pay_method.id"))
    #pay_total消した
    #外部リレーション
    customers = db.relationship("Customer", back_populates = "pay")
    contracts = db.relationship("Contract", back_populates = "pay")
    pay_method = db.relationship("Pay_method", back_populates = "pay")


    def __str__(self):
        return f'支払ID:{self.id}顧客ID:{self.customer_id}契約ID:{self.contract_id}支払方法ID:{self.pay_method_id}'


class Pay_method(db.Model):
    
    __tablename__ = "pay_method"

    id = db.Column(db.Integer, primary_key=True)
    pay_method_name = db.Column(db.String)

    #外部リレーション
    pay = db.relationship("Pay",back_populates="pay_method", lazy=True)

    def __str__(self):
        return f'支払方法ID:{self.id}支払方法:{self.pay_method_name}'


@app.route("/")
def index():
        
    money_customer_total = (
        db.session.query(db.func.count(distinct(Contract.customer_id)).label("customer_total") , db.func.sum(Contract.contract_number * Product.product_price).label("money_total"))
        .filter(Contract.product_id == Product.id)
    )


    Period_lists = (
        db.session.query(Period)
    )

    return render_template("index.html", money_customer_total=money_customer_total, Period_lists=Period_lists)


@app.route("/create_contract", methods = ["GET","POST"])
def create_contract():
    # POST
    if request.method == 'POST':
        # 入力値取得
        id = request.form['id']
        period_id = request.form['period_id']
        product_id = request.form['product_id']
        contract_number = request.form['contract_number']
        contract_situation = request.form['contract_situation']
        # インスタンス生成
        contract = Contract(id=id, period_id=period_id,product_id=product_id,contract_number=contract_number,contract_situation=contract_situation)
        # 登録
        db.session.add(contract)
        db.session.commit()
        # 一覧へ
        return redirect(url_for('index'))
    # GET
    return render_template('create_contract.html')


@app.route("/period_contract/<int:period_id>", methods = ["POST"])
def list(period_id):
    period_by_contract_list =db.select(Contract).where(Contract.contract_situationm != "解約済み").where(Contract.period_id == period_id).order_by(Contract.customer_id)
        
    customer_by_contract_cutomer_total = db.select(sum(Product.product_price * Contract.contract_number)).db.select(Customer).join(Product).join(Customer).where(Contract.contract_situationm != "解約済み").where(Contract.period_id == period_id).group_by(Contract.customer_id)
    
        
    period_by_contract_cutomer_total = db.select(sum(Product.product_price * Contract.contract_number)), func.count(distinct(Contract.customer_id)).join(Product).join(Customer).where(Contract.contract_situationm != "解約済み").where(Contract.period_id == period_id)


    return render_template("period_contract_list.html", period_by_contract_list=period_by_contract_list ,
                                customer_by_contract_cutomer_total=customer_by_contract_cutomer_total ,
                                period_by_contract_cutomer_total=period_by_contract_cutomer_total)


@app.route("/product")
def product():
    prouduct_lists =db.select(Product).order_by(Product.id)

    return render_template("product.html", prouduct_lists=prouduct_lists)


@app.route("/product/<int:product_id>", methods = ["POST"])
def product_by_contract(product_id):
    product_by_contract_lists = db.select(Contract.period_id,Customer.customer_name,Customer.telephon_number) .join(Customer).where(Contract.product_id == product_id).where(Contract.contract_situationm != "解約済み").order_by(Contract.customer_id)
    
    return render_template("product_by_contract.html", product_by_contract_lists=product_by_contract_lists)

if __name__ == '__main__':
    app.run()