from flask import Flask, request, render_template, redirect, url_for
from flask_migrate import Migrate
from models import db

# forms.pyから各フォームを追加する
from forms import AddCustomerForm, AddProductForm, AddPayMethodForm, AddDeliveryCycleForm


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

# 決済方法一覧
@app.route("/pay_method_list")
def pay_method_list_page():
    # customerテーブルを取得する
    """
    クエリイメージ：
    SERECT
        *
    FROM
        pay_methods
    ORDER BY
        pay_method_id ASC
    """
    pay_methods = Pay_method.query.order_by(Pay_method.id).all()
    return render_template("pay_method_list.html",pay_methods=pay_methods)

# 決済方法追加
@app.route("/add_pay_method", methods=["GET", "POST"])
def add_pay_method_page():
    form = AddPayMethodForm(request.form)
    # Post
    if request.method == "POST":
        # データ受け取り
        pay_method_id = form.pay_method_id.data
        pay_method_name = form.pay_method_name.data
        # DBにデータ追加
        """
        クエリイメージ：
        INSERT INTO pay_methods (id, pay_method_name) VALUES (pay_method_id, pay_method_name)
        """
        new_pay_method = Pay_method(id=pay_method_id, pay_method_name=pay_method_name)
        db.session.add(new_pay_method)
        db.session.commit()
        # ホーム画面に戻す
        return redirect(url_for("home_page"))
    # Get
    else:
        return render_template("add_pay_method.html", form=form)

# 周期情報一覧
@app.route("/delivery_cycle_list")
def delivery_cycle_list_page():
    # customerテーブルを取得する
    """
    クエリイメージ：
    SERECT
        *
    FROM
        delivery_cycles
    ORDER BY
        delivery_cycle_id ASC
    """
    delivery_cycles = Delivery_cycle.query.order_by(Delivery_cycle.id).all()
    return render_template("delivery_cycle_list.html",delivery_cycles=delivery_cycles)

# 周期情報追加
@app.route("/add_delivery_cycle", methods=["GET", "POST"])
def add_delivery_cycle_page():
    form = AddDeliveryCycleForm(request.form)
    # Post
    if request.method == "POST":
        # データ受け取り
        delivery_cycle_id = form.delivery_cycle_id.data
        week = form.week.data
        week_day = form.week_day.data
        # DBにデータ追加
        """
        クエリイメージ：
        INSERT INTO delivery_cycles (id, week, week_day) VALUES (delivery_cycle_id, week, week_day)
        """
        new_delivery_cycle = Delivery_cycle(id=delivery_cycle_id, week=week, week_day=week_day)
        db.session.add(new_delivery_cycle)
        db.session.commit()
        # ホーム画面に戻す
        return redirect(url_for("home_page"))
    # Get
    else:
        return render_template("add_delivery_cycle.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)