from flask import Flask, request, render_template, redirect, url_for
from flask_migrate import Migrate
from models import db

# forms.pyから各フォームを追加する
from forms import AddCustomerForm, AddProductForm


app = Flask(__name__)

# 下記設定内容は、config.pyにまとめてみよう！
# ---------------------------------------------------------------------
# before
"""
#DBファイル設定
app.config['SECRET_KEY'] = os.urandom(24)
base_dir = os.path.dirname(__file__)
database = "sqlite:///" + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = False
"""
# ---------------------------------------------------------------------
# after
app.config.from_object("config.Config")
# ---------------------------------------------------------------------


# DBとFlaskの紐づけ
db.init_app(app)
# マイグレーションの利用を宣言
Migrate(app, db)


# 各モデル(DB・Table)の設定は、models.pyにまとめてみよう！
# ---------------------------------------------------------------------
# before
"""
各クラスがapp.pyに、設定されていました

Contract   : 契約マスタ
Period     : 周期マスタ
Week       : 週マスタ
Week_day   : 曜日マスタ
Customer   : 顧客マスタ
Product    : 商品マスタ
Pay        : 支払いマスタ
Pay_method : 支払い方法マスタ
"""
# ---------------------------------------------------------------------
# after
"""
Contract       : 契約マスタ
Delivery_cycle : 周期マスタ   ← 名前変更しました(Periodから変更)
Week           : 週マスタ     ← とりあえず後回し
Week_day       : 曜日マスタ   ← とりあえず後回し
Customer       : 顧客マスタ
Product        : 商品マスタ
Pay            : 支払いマスタ
Pay_method     : 支払い方法マスタ
"""
from models import (
                    Contract,
                    Delivery_cycle,
                    Customer,
                    Product,
                    Pay,
                    Pay_method
                )
# ---------------------------------------------------------------------


# ==================================================
# ルーティング
# ==================================================

# ホーム画面
@app.route("/")
def home_page():
    return render_template("home.html")

# 顧客情報一覧
@app.route("/customer_list")
def customer_list_page():
    # customerテーブルを取得する
    """
    クエリイメージ：
    SERECT
        *
    FROM
        customer
    ORDER BY
        customer_id ASC
    """
    customers = Customer.query.order_by(Customer.id).all()
    return render_template("customer_list.html",customers=customers)

# 顧客情報追加
@app.route("/add_customer", methods=["GET", "POST"])
def add_customer_page():
    form = AddCustomerForm(request.form)
    # Post
    if request.method == "POST":
        # データ受け取り
        customer_id = form.customer_id.data
        customer_name = form.customer_name.data
        phone_number = form.phone_number.data
        # DBにデータ追加
        """
        クエリイメージ：
        INSERT INTO customers (id, customer_name, phone_number) VALUES (customer_id, customer_name, phone_number)
        """
        new_customer = Customer(id=customer_id, customer_name=customer_name, phone_number=phone_number)
        db.session.add(new_customer)
        db.session.commit()
        # ホーム画面に戻す
        return redirect(url_for("home_page"))
    # Get
    else:
        return render_template("add_customer.html", form=form)

# 商品情報一覧
@app.route("/product_list")
def product_list_page():
    # customerテーブルを取得する
    """
    クエリイメージ：
    SERECT
        *
    FROM
        products
    ORDER BY
        priduct_id ASC
    """
    products = Product.query.order_by(Product.id).all()
    return render_template("product_list.html",products=products)

# 商品情報追加
@app.route("/add_product", methods=["GET", "POST"])
def add_product_page():
    form = AddProductForm(request.form)
    # Post
    if request.method == "POST":
        # データ受け取り
        product_id = form.product_id.data
        product_name = form.product_name.data
        product_price = form.product_price.data
        # DBにデータ追加
        """
        クエリイメージ：
        INSERT INTO products (id, product_name, product_price) VALUES (product_id, product_name, product_price)
        """
        new_product = Product(id=product_id, product_name=product_name, product_price=product_price)
        db.session.add(new_product)
        db.session.commit()
        # ホーム画面に戻す
        return redirect(url_for("home_page"))
    # Get
    else:
        return render_template("add_product.html", form=form)

"""
@app.route("/create_contract", methods = ["GET","POST"])
def create_contract():
    # POST
    if request.method == 'POST':
        # 入力値取得
        contract_id = request.form.get('contract_id')
        period_id = request.form.get('period_id')
        product_id = request.form.get('product_id')
        contract_number = request.form.get('contract_number')
        contract_situation = request.form.get('contract_situation')
        # インスタンス生成
        contract = Contract(contract_id=contract_id, period_id=period_id, product_id=product_id, contract_number=contract_number, contract_situation=contract_situation)
        # 登録
        db.session.add(contract)
        db.session.commit()
        # 一覧へ
        return redirect("/")
    # GET
    return render_template('create_contract.html')


@app.route("/period_contract/<int:period_id>", methods = ["POST"])
def list(period_id):
    period_by_contract_list = (
        db.session.query(Contract.contract_id, Contract.customer_id, Customer.customer_name, Customer.telephon_number, Product.product_name, Product.product_price, Contract.contract_number, Contract.contract_situationm)
        .filter(Contract.contract_situationm != "解約済み", Contract.period_id == period_id)
        .order_by(Contract.customer_id)
    )
    customer_by_contract_cutomer_total = (
        db.session.query(func.sum(Product.product_price * Contract.contract_number).label("money_total"), Customer.customer_name, Customer.telephon_number)
        .filter(Contract.contract_situationm != "解約済み", Contract.period_id == period_id)
        .group_by(Contract.customer_id)
        .order_by(Contract.customer_id)
    )



    period_by_contract_cutomer_total = (
        db.session.query(db.func.count(distinct(Contract.customer_id)).label("customer_total") , db.func.sum(Contract.contract_number * Product.product_price).label("money_total"))
        .filter(Contract.contract_situationm != "解約済み", Contract.period_id == period_id)
    )

    return render_template("period_contract_list.html", period_by_contract_list=period_by_contract_list ,
                                customer_by_contract_cutomer_total=customer_by_contract_cutomer_total ,
                                period_by_contract_cutomer_total=period_by_contract_cutomer_total)


@app.route("/product")
def product():
    prouduct_lists =(
        db.session.query(Product.product_id, Product.product_name, Product.product_price)
        .order_by(Product.product_id)
    )

    return render_template("product.html", prouduct_lists=prouduct_lists)


@app.route("/product/<int:product_id>", methods = ["POST"])
def product_by_contract(product_id):
    product_by_contract_lists = (
        db.session.query(Contract.period_id, Customer.customer_name, Customer.telephon_number)
        .filter(Contract.contract_situationm != "解約済み", Contract.product_id == product_id)
        .order_by(Contract.customer_id)
    )
    return render_template("product_by_contract.html", product_by_contract_lists=product_by_contract_lists)
"""



if __name__ == '__main__':
    app.run(debug=True)