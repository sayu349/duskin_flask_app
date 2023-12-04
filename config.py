import os

# ==================================================
# 設定
# ==================================================
class Config(object):
    # デバッグモード
    DEBUG=True
    # セキュリティーキー
    SECRET_KEY = os.urandom(24)
    # 警告対策
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DB設定
    base_dir = os.path.dirname(__file__)
    database = "sqlite:///" + os.path.join(base_dir, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = database