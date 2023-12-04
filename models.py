from flask_sqlalchemy import SQLAlchemy

# Flask-SQLAlchemyの生成
db = SQLAlchemy()

# ==================================================
# モデル
# ==================================================

"""
顧客マスタ
- id (PK)       : 顧客ID
- customer_name : 顧客名
- phone_number  : 電話番号
"""
class Customer(db.Model):
    # テーブル名
    __tablename__ = "customers"
    # 顧客ID
    id = db.Column(db.Integer, primary_key=True)
    # 顧客名
    customer_name = db.Column(db.String)
    # 電話番号
    phone_number = db.Column(db.String)
    # ---------------------------------------------------
    # リレーション構築（顧客マスタ ➡ 契約マスタ）
    contract = db.relationship("Contract", back_populates='customer')
    # ---------------------------------------------------
    # リレーション構築（顧客マスタ ➡ 支払いマスタ）
    pay   = db.relationship("Pay", back_populates='customer')

"""
商品マスタ
- id (PK)       : 商品ID
- product_name  : 商品名
- product_price : 商品価格
"""
class Product(db.Model):
    __tablename__ = "products"
    # 商品ID
    id = db.Column(db.Integer, primary_key=True)
    # 商品名
    product_name = db.Column(db.String)
    # 商品価格
    product_price = db.Column(db.Integer)
    # ---------------------------------------------------
    # リレーション構築（商品マスタ ➡ 契約マスタ）
    contract = db.relationship("Contract", back_populates='product')

"""
決済方法マスタ
- id (PK)         : 決済方法ID
- pay_method_name : 決済方法名
"""
class Pay_method(db.Model):
    __tablename__ = "pay_methods"
    # 決済方法ID
    id = db.Column(db.Integer, primary_key=True)
    # 決済方法名
    pay_method_name = db.Column(db.String)
    # ---------------------------------------------------
    # リレーション構築（決済方法マスタ ➡ 支払いマスタ）
    pay = db.relationship("Pay", back_populates='pay_method')

"""
周期マスタ
- id (PK)  : 周期ID
- week     : 週
- week_day : 曜日
"""
class Delivery_cycle(db.Model):
    __tablename__ = "delivery_cycles"
    # 周期ID
    id = db.Column(db.Integer, primary_key=True)
    # 週
    week = db.Column(db.String)
    # 曜日
    week_day = db.Column(db.String)
    # ---------------------------------------------------
    # リレーション構築（周期マスタ ➡ 契約マスタ）
    contract = db.relationship("Contract", back_populates='delivery_cycle')

"""
契約マスタ
- id                (PK) : 契約ID
- delivery_cycle_id (FK) : 周期ID
- customer_id       (FK) : 顧客ID
- product_id        (FK) : 商品ID
- contract_number        : 契約数
- contract_situation     : 契約状況
- subtotal               : 小計
"""
class Contract(db.Model):
    __tablename__ = "contracts"
    # ID
    id = db.Column(db.Integer, primary_key=True)
    # 周期ID
    delivery_cycle_id = db.Column(db.Integer, db.ForeignKey("delivery_cycles.id"))
    # 顧客ID
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    # 商品ID
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    # 契約数
    contract_number = db.Column(db.Integer)
    # 契約状況
    contract_situation = db.Column(db.String)
    # 小計
    amount = db.Column(db.Integer)
    # ---------------------------------------------------
    """
    リレーション構築
    1. 周期マスタ ➡ 契約マスタ
    2. 顧客マスタ ➡ 契約マスタ
    3. 商品マスタ ➡ 契約マスタ
    """
    delivery_cycle = db.relationship("Delivery_cycle", back_populates='contract')
    customer       = db.relationship("Customer", back_populates='contract')
    product        = db.relationship("Product", back_populates='contract')
    # ---------------------------------------------------
    # リレーション構築（契約マスタ ➡ 支払いマスタ）
    pay = db.relationship("Pay", back_populates='contract')


"""
支払いマスタ
- id            (PK) : 支払ID
- customer_id   (FK) : 顧客ID
- contract_id   (FK) : 契約ID
- pay_method_id (FK) : 決済方法ID
- Payment_amount     : 支払額
"""
class Pay(db.Model):
    __tablename__ = "pays"
    # 支払ID
    id = db.Column(db.Integer, primary_key=True)
    # 顧客ID
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    # 契約ID
    contract_id  = db.Column(db.Integer, db.ForeignKey("contracts.id"))
    # 決済方法ID
    pay_method_id  = db.Column(db.Integer, db.ForeignKey("pay_methods.id"))
    # 支払額
    payment_amount = db.Column(db.Integer)
    # ---------------------------------------------------
    """
    リレーション構築
    1. 顧客マスタ     ➡ 支払いマスタ
    2. 契約マスタ     ➡ 支払いマスタ
    3. 決済方法マスタ ➡ 支払いマスタ
    """
    customer   = db.relationship("Customer", back_populates='pay')
    contract   = db.relationship("Contract", back_populates='pay')
    pay_method = db.relationship("Pay_method", back_populates='pay')
