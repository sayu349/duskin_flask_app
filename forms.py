from wtforms import Form
from wtforms.fields import StringField, SubmitField, IntegerField

#--------------------------------------------------------------------------------------------------------------------------------

# 顧客情報追加フォーム
"""
商品マスタ
- id (PK)       : 商品ID
- product_name  : 商品名
- product_price : 商品価格
"""
class AddCustomerForm(Form):
    # 顧客ID：整数入力
    customer_id = IntegerField("顧客ID")

    # 顧客名：文字列入力
    customer_name = StringField("顧客名")

    # 電話番号：文字列入力
    phone_number = StringField("電話番号",render_kw={"placeholder":"080-1234-5678（ハイフンあり）"})

    # ボタン
    submit = SubmitField("送信")

#--------------------------------------------------------------------------------------------------------------------------------

# 商品情報追加フォーム
"""
商品マスタ
- id (PK)       : 商品ID
- product_name  : 商品名
- product_price : 商品価格
"""
class AddProductForm(Form):
    # 顧客ID：整数入力
    product_id = IntegerField("商品ID")

    # 顧客名：文字列入力
    product_name = StringField("商品名")

    # 商品価格：整数入力
    product_price = IntegerField("商品価格")

    # ボタン
    submit = SubmitField("送信")

#--------------------------------------------------------------------------------------------------------------------------------

# 決済方法追加フォーム
"""
決済方法マスタ
- id (PK)         : 決済方法ID
- pay_method_name : 決済方法名
"""
class AddPayMethodForm(Form):
    # 決済方法ID：整数入力
    pay_method_id = IntegerField("決済方法ID")

    # 顧客名：文字列入力
    pay_method_name = StringField("決済方法名")

    # ボタン
    submit = SubmitField("送信")

#--------------------------------------------------------------------------------------------------------------------------------

# 周期情報追加フォーム
"""
周期マスタ
- id (PK)  : 周期ID
- week     : 週
- week_day : 曜日
"""
class AddDeliveryCycleForm(Form):
    # 周期ID：整数入力
    delivery_cycle_id = IntegerField("周期ID")

    # 週：文字列入力
    week = StringField("週")

    # 曜日：文字列入力
    week_day = StringField("曜日")

    # ボタン
    submit = SubmitField("送信")

#--------------------------------------------------------------------------------------------------------------------------------

# 契約情報追加フォーム
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
class AddContractForm(Form):
    # 契約ID：整数入力
    contract_id = IntegerField("契約ID")

    # 周期ID：整数入力
    delivery_cycle_id = IntegerField("周期ID")

    # 顧客ID：整数入力
    customer_id = IntegerField("顧客ID")

    # 商品ID：整数入力
    product_id = IntegerField("商品ID")

    # 契約数：文字列入力
    contract_number = IntegerField("契約数")

    # 契約状況；文字列入力
    contract_situation = StringField("契約状況")

    # 小計：整数入力
    amount = IntegerField("小計")

    # ボタン
    submit = SubmitField("送信")

#--------------------------------------------------------------------------------------------------------------------------------