from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db, Period, app, Product, Customer



with app.app_context():

#Periodデフォルト登録
    A1 = Period(period_id = "A月")
    A2 = Period(period_id = "A火")
    A3 = Period(period_id = "A水")
    A4 = Period(period_id = "A木")
    A5 = Period(period_id = "A金")
    A6 = Period(period_id = "A土")
    A7 = Period(period_id = "A日")

    B1 = Period(period_id = "B月")
    B2 = Period(period_id = "B火")
    B3 = Period(period_id = "B水")
    B4 = Period(period_id = "B木")
    B5 = Period(period_id = "B金")
    B6 = Period(period_id = "B土")
    B7 = Period(period_id = "B日")

    C1 = Period(period_id = "C月")
    C2 = Period(period_id = "C火")
    C3 = Period(period_id = "C水")
    C4 = Period(period_id = "C木")
    C5 = Period(period_id = "C金")
    C6 = Period(period_id = "C土")
    C7 = Period(period_id = "C日")

    D1 = Period(period_id = "D月")
    D2 = Period(period_id = "D火")
    D3 = Period(period_id = "D水")
    D4 = Period(period_id = "D木")
    D5 = Period(period_id = "D金")
    D6 = Period(period_id = "D土")
    D7 = Period(period_id = "D日")

    db.session.add_all([A1,A2,A3,A4,A5,A6,A7,B1,B2,B3,B4,B5,B6,B7,C1,C2,C3,C4,C5,C6,C7,D1,D2,D3,D4,D5,D6,D7])
    db.session.commit()
#↑↑↑↑↑

#Productデフォルト登録
with app.app_context():
    floor_mop = Product(product_id = "S212", product_name = "ゴールデンモップ", product_price = 930)
    handy_mop = Product(product_id = "S237", product_name = "フリージー", product_price = 1040)
    db.session.add_all([floor_mop,handy_mop])
    db.session.commit()



with app.app_context():
    user1 = Customer(customer_id = 1, customer_name = "A", telephon_number = "090-4444-2111", customer_situation = "利用なし")
    user2 = Customer(customer_id = 2, customer_name = "B", telephon_number = "080-2222-3456", customer_situation = "利用なし")
    db.session.add_all([user1,user2])
    db.session.commit()