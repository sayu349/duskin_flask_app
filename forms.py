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

