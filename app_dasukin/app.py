from sqlalchemy.orm import DeclarativeBase
import os
from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func, desc


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

    contract_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    period_id = db.Column(db.String, db.ForeignKey("period.period_id"),nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"),nullable=False)
    product_id = db.Column(db.String, db.ForeignKey("products.product_id"),nullable=False)
    contract_number = db.Column(db.Integer,nullable=False)
    contract_situation = db.Column(db.String,nullable=False)
    pay_method_id = db.Column(db.String,nullable=False)



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
    customer_name = db.Column(db.String,nullable=False)
    telephon_number = db.Column(db.String,nullable=False)
    customer_situation = db.Column(db.String,nullable=False)
    #主リレーション
    contracts = db.relationship("Contract", backref="customers")

    def __str__(self):
        return f'顧客ID:{self.customer_id}顧客名:{self.customer_name}電話番号:{self.telephon_number}'


class Product(db.Model):
    
    __tablename__ = "products"

    product_id = db.Column(db.String, primary_key=True)
    product_name = db.Column(db.String,nullable=False)
    product_price = db.Column(db.Integer,nullable=False)

    #主リレーション
    contracts = db.relationship("Contract", backref="products")

    def __str__(self):
        return f'商品ID:{self.product_id}商品名:{self.product_name}商品価格:{self.product_price}'
#====================================================================================================
#トップページ
@app.route("/")
def index():

    subtotal = func.sum(Contract.contract_number * Product.product_price)

    customer_total = Customer.query.filter(Customer.customer_situation=="利用中").count()
        
    
    money_total = Contract.query.with_entities(subtotal).join(Product).filter(Contract.contract_situation == "契約中").first()
    money_total_credit = Contract.query.with_entities(subtotal).join(Product).filter(Contract.contract_situation == "契約中",Contract.pay_method_id=="クレジット").first()
    money_total_cash = Contract.query.with_entities(subtotal).join(Product).filter(Contract.contract_situation == "契約中",Contract.pay_method_id=="現金").first()


    Period_lists = Period.query.all()

    return render_template("index.html", customer_total=customer_total,money_total=money_total ,Period_lists=Period_lists,money_total_credit=money_total_credit,money_total_cash=money_total_cash)
#====================================================================================================



#====================================================================================================
#解約済み表示リスト
@app.route("/contract/delete/list")
def contract_delete_lists():
    join_query = db.session.query(Contract, Period, Customer, Product). \
        join(Period, Contract.period_id == Period.period_id). \
        join(Customer, Contract.customer_id == Customer.customer_id). \
        join(Product, Contract.product_id == Product.product_id)

    contract_delete_list = join_query.order_by(Customer.customer_id).filter(Contract.contract_situation=="解約済").with_entities(Contract.contract_id,Customer.customer_id,Customer.customer_name,Customer.telephon_number,Contract.period_id,Product.product_name,Product.product_price,Contract.contract_number,Contract.pay_method_id)

    return render_template("contract_delete_list.html",contract_delete_list=contract_delete_list)
#====================================================================================================



#====================================================================================================
#contract操作
@app.route("/create_contract", methods = ["GET","POST"])
def create_contract():
    
    if request.method == 'POST':
        
        contract_id = request.form.get('contract_id')
        period_id = request.form.get('period_id')
        customer_id = request.form.get('customer_id')
        product_id = request.form.get('product_id')
        contract_number = request.form.get('contract_number')
        contract_situation = request.form.get('contract_situation')
        pay_method_id = request.form.get('pay_method_id')
        
        contract = Contract(contract_id=contract_id, period_id=period_id, customer_id=customer_id, product_id=product_id, contract_number=contract_number, contract_situation=contract_situation,pay_method_id=pay_method_id)
        


        db.session.add(contract)
        db.session.commit()
        
        return redirect(url_for("customer_situation_true",customer_id=customer_id))
    # GET
    customer_lists = Customer.query.all()
    product_lists = Product.query.all()
    return render_template('create_contract.html',customer_lists=customer_lists,product_lists=product_lists)

@app.route("/contract/update/<int:contract_id>", methods = ["GET","POST"])
def contract_update(contract_id):
    contract_data = Contract.query.get(contract_id)
    if request.method == 'POST':

        

        period_id = request.form.get('period_id')
        customer_id = request.form.get('customer_id')
        product_id = request.form.get('product_id')
        contract_number = request.form.get('contract_number')

        pay_method_id = request.form.get('pay_method_id')

        contract_data.period_id = period_id
        contract_data.customer_id = customer_id
        contract_data.product_id = product_id
        contract_data.contract_number = contract_number

        contract_data.pay_method_id = pay_method_id
        db.session.commit()

        return redirect(url_for("list", period_id=contract_data.period_id))

    

    return render_template("contract_update.html",contract_data=contract_data)
@app.route("/contract/delete/<int:contract_id>")
def contract_delete(contract_id):
    contract_data = Contract.query.get(contract_id)

    contract_data.contract_situation = "解約済"


    db.session.commit()

    
    return redirect(url_for("customer_situation_false", customer_id=contract_data.customer_id, contract_id=contract_data.contract_id))

@app.route("/contract/true/<int:contract_id>/<int:customer_id>")
def contract_true(contract_id,customer_id):
    contract_data = Contract.query.get(contract_id)

    contract_data.contract_situation = "契約中"

    customer = Customer.query.get(customer_id) 

    customer.customer_situation = "利用中"

    db.session.commit()
    return redirect("/contract/delete/list")
#====================================================================================================



#====================================================================================================
#customer操作
@app.route("/create_customer", methods = ["GET","POST"])
def create_customer():
    
    if request.method == 'POST':
        
        customer_id = request.form.get('customer_id')
        customer_name = request.form.get('customer_name')
        telephon_number = request.form.get('telephon_number')
        customer_situation = "利用なし"
        
        customer = Customer(customer_id=customer_id,customer_name=customer_name,telephon_number=telephon_number,customer_situation=customer_situation)
        
        db.session.add(customer)
        db.session.commit()
        
        return redirect("/")
    
    return render_template('create_customer.html')

@app.route("/customer/update/<int:customer_id>", methods = ["GET","POST"])
def customer_update(customer_id):
    customer = Customer.query.get(customer_id)
    if request.method == 'POST':

        customer_name = request.form.get('customer_name')
        telephon_number = request.form.get('telephon_number')

        customer.customer_name = customer_name
        customer.telephon_number = telephon_number

        db.session.commit()

        return redirect("/customer")
    return render_template("customer_update.html",customer=customer)

@app.route("/customer/delete/<int:customer_id>")
def customer_delete_perfect(customer_id):
    contract_data = Contract.query.filter(Contract.contract_situation=="契約中",Contract.customer_id==customer_id).count()
    if contract_data==0:

        customer_contract_data_all = Contract.query.filter(Contract.customer_id==customer_id).all()
        for customer_contract_data in customer_contract_data_all:
            db.session.delete(customer_contract_data)
            db.session.commit()

        customer_data = Customer.query.get(customer_id)
        db.session.delete(customer_data)
        db.session.commit()    

        return redirect("/customer")
    
    return redirect("/customer/delete/err")

@app.route("/customer/delete/err")
def customer_err():
    return render_template("customer_delete_err.html")

@app.route("/customer_situation/<int:customer_id>")
def customer_situation_true(customer_id):

    customer = Customer.query.get(customer_id) 

    customer.customer_situation = "利用中"

    db.session.commit()

    return redirect("/")

@app.route("/customer_situation/false/<int:customer_id>/<contract_id>")
def customer_situation_false(customer_id,contract_id):
    contract_data_all = Contract.query.filter(Contract.contract_situation=="契約中",Contract.customer_id==customer_id).count()
    if contract_data_all == 0:
        customer = Customer.query.get(customer_id)
        customer.customer_situation = "利用なし"

        contract_data = Contract.query.get(contract_id)
        db.session.commit()
        return redirect(url_for("list", period_id=contract_data.period_id))
    
    customer = Customer.query.get(customer_id)
    customer.customer_situation = "利用中"
    contract_data = Contract.query.get(contract_id)
    db.session.commit()
    return redirect(url_for("list", period_id=contract_data.period_id))
    
#====================================================================================================



#====================================================================================================
#product操作
@app.route("/create_product", methods = ["GET","POST"])
def create_product():
    # POST
    if request.method == 'POST':
        # 入力値取得
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        product_price = request.form.get('product_price')

        # インスタンス生成
        product_data = Product(product_id=product_id,product_name=product_name,product_price=product_price)
        # 登録
        db.session.add(product_data)
        db.session.commit()
        # 一覧へ
        return redirect("/")
    # GET
    return render_template('create_product.html')

@app.route("/product/update/<product_id>", methods = ["GET","POST"])
def product_update(product_id):
    product = Product.query.get(product_id)
    if request.method == 'POST':

        product_name = request.form.get('product_name')
        product_price = request.form.get('product_price')

        product.product_name = product_name
        product.product_price = product_price

        db.session.commit()

        return redirect("/product")
    return render_template("product_update.html",product=product)

@app.route("/product/delete/<product_id>")
def product_delete_perfect(product_id):
    contract_data = Contract.query.filter(Contract.contract_situation=="契約中",Contract.product_id==product_id).count()
    if contract_data==0:

        
        
        product_contract_data_all = Contract.query.filter(Contract.product_id==product_id).all()
        for product_contract_data in product_contract_data_all:
            db.session.delete(product_contract_data)
            db.session.commit()

        
        product_data = Product.query.get(product_id)
        db.session.delete(product_data)
        db.session.commit() 
        return redirect("/product")

        
    
    return redirect("/product/delete/err")

@app.route("/product/delete/err")
def product_err():
    return render_template("product_delete_err.html")
#====================================================================================================



#====================================================================================================
#周期別リスト
@app.route("/period_contract/<period_id>")
def list(period_id):

    join_query = db.session.query(Contract, Period, Customer, Product). \
        join(Period, Contract.period_id == Period.period_id). \
        join(Customer, Contract.customer_id == Customer.customer_id). \
        join(Product, Contract.product_id == Product.product_id)
        
    subtotal = func.sum(Contract.contract_number * Product.product_price)


    period = Period.query.filter(Period.period_id == period_id).with_entities(Period.period_id).all()


    period_by_contract_list = join_query.filter(Contract.contract_situation == "契約中", Contract.period_id == period_id).with_entities(Contract.contract_id,Customer.customer_name,Customer.telephon_number,Product.product_name,Contract.contract_number,Product.product_price,Contract.pay_method_id).order_by(desc(Contract.customer_id)).all()
    
    groupby_customer_money = join_query.group_by(Contract.customer_id).with_entities(Contract.customer_id,Customer.customer_name,Customer.telephon_number,subtotal.label("subtotal")).filter(Contract.contract_situation == "契約中", Contract.period_id == period_id)
    


    period_customer_total = Contract.query.group_by(Contract.customer_id).with_entities(Contract.contract_id).filter(Contract.contract_situation == "契約中", Contract.period_id == period_id).count()

    period_money_total = Contract.query.with_entities(subtotal).join(Product).filter(Contract.contract_situation == "契約中", Contract.period_id == period_id).first()

    return render_template("period_contract_list.html", period_by_contract_list=period_by_contract_list,period=period
                           ,groupby_customer_money=groupby_customer_money,period_customer_total=period_customer_total
                           ,period_money_total=period_money_total,subtotal=subtotal)
#====================================================================================================



#====================================================================================================
#顧客一覧
@app.route("/customer")
def customer():
    customer_lists = Customer.query.all()

    return render_template("customer.html",customer_lists=customer_lists)
#顧客一覧---##顧客別リスト
@app.route("/customer/<customer_id>")
def customer_contract(customer_id):
        join_query = db.session.query(Contract, Period, Customer, Product). \
        join(Period, Contract.period_id == Period.period_id). \
        join(Customer, Contract.customer_id == Customer.customer_id). \
        join(Product, Contract.product_id == Product.product_id)

        subtotal = join_query.filter(Contract.contract_situation == "契約中",Contract.customer_id == customer_id).with_entities(func.sum(Contract.contract_number * Product.product_price).label("subtotal"))

        #全体契約数
        contract_number = Contract.query.filter(Contract.contract_situation == "契約中",Contract.customer_id == customer_id).with_entities(func.sum(Contract.contract_number).label("contract_number"))

        #選択した顧客の名前
        select_customer = Customer.query.filter(Customer.customer_id == customer_id).with_entities(Customer.customer_name)

        #顧客別"契約中"リストクエリ
        customer_contract_lists = join_query.order_by(Customer.customer_id).filter(Contract.contract_situation == "契約中",Contract.customer_id == customer_id).with_entities(Period.period_id,Contract.contract_number,Product.product_name,Product.product_price,Contract.pay_method_id).all()

        #顧客別"解約済"リストクエリ
        customer_contract_delete = join_query.order_by(Customer.customer_id).filter(Contract.contract_situation == "解約済",Contract.customer_id == customer_id).with_entities(Period.period_id,Contract.contract_number,Product.product_name,Product.product_price,Contract.pay_method_id).all()

        return render_template("customer_contract.html",contract_number=contract_number,select_customer=select_customer,customer_contract_lists=customer_contract_lists,subtotal=subtotal,customer_contract_delete=customer_contract_delete)
#====================================================================================================



#====================================================================================================
#商品一覧
@app.route("/product")
def product():
    product_lists = Product.query.all()

    return render_template("product.html", product_lists=product_lists)
#商品一覧---##商品別リスト
@app.route("/product/<product_id>")
def product_by_contract(product_id):

    join_query = db.session.query(Contract, Period, Customer, Product). \
        join(Period, Contract.period_id == Period.period_id). \
        join(Customer, Contract.customer_id == Customer.customer_id). \
        join(Product, Contract.product_id == Product.product_id)
    
    subtotal = join_query.filter(Contract.contract_situation == "契約中",Contract.product_id == product_id).with_entities(func.sum(Contract.contract_number * Product.product_price).label("subtotal"))

    contract_number = Contract.query.filter(Contract.contract_situation == "契約中",Contract.product_id == product_id).with_entities(func.sum(Contract.contract_number).label("contract_number"))


    select_product = Product.query.filter(Product.product_id == product_id).with_entities(Product.product_name).all()
    product_by_contract_lists = join_query.order_by(Product.product_id).filter(Contract.contract_situation == "契約中",Contract.product_id == product_id).with_entities(Contract.contract_number,Customer.customer_name,Customer.telephon_number,Period.period_id,Contract.pay_method_id).all()

    return render_template("product_by_contract.html", product_by_contract_lists=product_by_contract_lists,select_product=select_product,contract_number=contract_number,subtotal=subtotal)
#====================================================================================================


if __name__ == '__main__':
    app.run(debug=True)