from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
import pandas as pd
import os
from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import select, distinct, func, join

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

    contract_id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.String, db.ForeignKey("period.period_id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"))
    product_id = db.Column(db.String, db.ForeignKey("products.product_id"))
    contract_number = db.Column(db.Integer)
    contract_situation = db.Column(db.String)
    pay_method_id = db.Column(db.String)



    def __str__(self):
        return f'契約ID:{self.contract_id}周期ID:{self.period_id}顧客ID{self.customer_id}商品ID:{self.product_id}契約数:{self.contract_number}契約状況:{self.contract_situation}支払方法{self.pay_method_id}'


class Period(db.Model):
    
    __tablename__ = "period"

    period_id = db.Column(db.String, primary_key=True)

    #主リレーション
    contracts = db.relationship("Contract", backref = "period")

  
    def __str__(self):
        return f'{self.period_id}'


class Customer(db.Model):
    
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String)
    telephon_number = db.Column(db.Integer)

    #主リレーション
    contracts = db.relationship("Contract", backref="customers")

    def __str__(self):
        return f'顧客ID:{self.customer_id}顧客名:{self.customer_name}電話番号:{self.telephon_number}'


class Product(db.Model):
    
    __tablename__ = "products"

    product_id = db.Column(db.String, primary_key=True)
    product_name = db.Column(db.String)
    product_price = db.Column(db.Integer)

    #主リレーション
    contracts = db.relationship("Contract", backref="products")

    def __str__(self):
        return f'商品ID:{self.product_id}商品名:{self.product_name}商品価格:{self.product_price}'


@app.route("/")
def index():
    customer_total = Customer.query.count()
        
    
    money_total = Contract.query.with_entities(func.sum(Contract.contract_number * Product.product_price)).join(Product).filter(Contract.contract_situation == "契約済").all()


    Period_lists = Period.query.all()


    return render_template("index.html", customer_total=customer_total,money_total=money_total ,Period_lists=Period_lists)


@app.route("/create_contract", methods = ["GET","POST"])
def create_contract():
    # POST
    if request.method == 'POST':
        # 入力値取得
        contract_id = request.form.get('contract_id')
        period_id = request.form.get('period_id')
        customer_id = request.form.get('customer_id')
        product_id = request.form.get('product_id')
        contract_number = request.form.get('contract_number')
        contract_situation = request.form.get('contract_situation')
        # インスタンス生成
        contract = Contract(contract_id=contract_id, period_id=period_id, customer_id=customer_id, product_id=product_id, contract_number=contract_number, contract_situation=contract_situation)
        # 登録
        db.session.add(contract)
        db.session.commit()
        # 一覧へ
        return redirect("/")
    # GET
    customer_lists = Customer.query.all()
    product_lists = Product.query.all()
    return render_template('create_contract.html',customer_lists=customer_lists,product_lists=product_lists)


@app.route("/create_customer", methods = ["GET","POST"])
def create_customer():
    # POST
    if request.method == 'POST':
        # 入力値取得
        customer_id = request.form.get('customer_id')
        customer_name = request.form.get('customer_name')
        telephon_number = request.form.get('telephon_number')

        # インスタンス生成
        customer = Customer(customer_id=customer_id,customer_name=customer_name,telephon_number=telephon_number)
        # 登録
        db.session.add(customer)
        db.session.commit()
        # 一覧へ
        return redirect("/")
    # GET
    return render_template('create_customer.html')


@app.route("/create_product", methods = ["GET","POST"])
def create_product():
    # POST
    if request.method == 'POST':
        # 入力値取得
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        propduct_price = request.form.get('product_price')

        # インスタンス生成
        product_data = Product(product_id=product_id,product_name=product_name,propduct_price=propduct_price)
        # 登録
        db.session.add(product_data)
        db.session.commit()
        # 一覧へ
        return redirect("/")
    # GET
    return render_template('create_product.html')

@app.route("/period_contract/<period_id>")
def list(period_id):

    join_query = db.session.query(Contract, Period, Customer, Product). \
        join(Period, Contract.period_id == Period.period_id). \
        join(Customer, Contract.customer_id == Customer.customer_id). \
        join(Product, Contract.product_id == Product.product_id)
        

    subtotal = Contract.contract_number * Product.product_price


    period = Period.query.filter(Period.period_id == period_id).all()


    period_by_contract_list = join_query.filter(Contract.contract_situation == "契約済", Contract.period_id == period_id).all()
    
    groupby_customer_money = join_query.group_by(Contract.customer_id).with_entities(Contract.customer_id,func.sum(subtotal),Customer.customer_name,Customer.telephon_number).filter(Contract.contract_situation == "契約済", Contract.period_id == period_id)
    

    period_customer_total = Contract.query.group_by(Contract.customer_id).with_entities(Contract.contract_id).filter(Contract.contract_situation == "契約済", Contract.period_id == period_id).count()

    period_money_total = Contract.query.with_entities(func.sum(subtotal)).join(Product).filter(Contract.contract_situation == "契約済", Contract.period_id == period_id).all()

    return render_template("period_contract_list.html", period_by_contract_list=period_by_contract_list,period=period
                           ,groupby_customer_money=groupby_customer_money,period_customer_total=period_customer_total
                           ,period_money_total=period_money_total)


@app.route("/product")
def product():
    product_lists = Product.query.all()

    return render_template("product.html", product_lists=product_lists)


@app.route("/product/<product_id>")
def product_by_contract(product_id):

    join_query = db.session.query(Contract, Period, Customer, Product). \
        join(Period, Contract.period_id == Period.period_id). \
        join(Customer, Contract.customer_id == Customer.customer_id). \
        join(Product, Contract.product_id == Product.product_id)

    select_product = Product.query.filter(Product.product_name == product_id).all()
    product_by_contract_lists = join_query.filter(Contract.product_id == product_id,Contract.contract_situation == "契約済").all()
    return render_template("product_by_contract.html", product_by_contract_lists=product_by_contract_lists,select_product=select_product)

if __name__ == '__main__':
    app.run(debug=True)