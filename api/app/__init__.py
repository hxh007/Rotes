# coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

# 实例化sqlalchemy
db = SQLAlchemy()


# 定义工厂方法
def create_app(config_name):
    # 实例化Flask
    app = Flask(__name__)
    # 使用配置对象
    app.config.from_object(config[config_name])

    # 关联程序实例
    db.init_app(app)

    # 注册蓝图
    from .BlueWatch import blue_watch
    app.register_blueprint(blue_watch)
    from .BlueAuth import blue_auth
    app.register_blueprint(blue_auth)

    return app
