# coding=utf-8

from redis import StrictRedis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_apscheduler import APScheduler
from apscheduler.events import (EVENT_JOB_ERROR, EVENT_JOB_EXECUTED)

from config import config, Config
# 实例化sqlalchemy
db = SQLAlchemy()

# redis
Redis = StrictRedis(host=Config.REDIS_HOST,
                    port=Config.REDIS_PORT,
                    db=Config.REDIS_DB,
                    password=Config.REDIS_PASSWORD,
                    max_connections=int(Config.REDIS_MAX_CONNECTIONS))

cron_scheduler = APScheduler()

# 定义工厂方法
def create_app(config_name):
    # 实例化Flask
    app = Flask(__name__)
    # 使用配置对象
    app.config.from_object(config[config_name])

    # 关联程序实例
    db.init_app(app)
    CORS(app)
    from .BlueCron.job import listener_cronEvent
    cron_scheduler.init_app(app)
    cron_scheduler.add_listener(listener_cronEvent, EVENT_JOB_EXECUTED|EVENT_JOB_ERROR)
    cron_scheduler.start(paused=True)

    # 注册蓝图
    from .BlueWatch import blue_watch
    app.register_blueprint(blue_watch)
    from .BlueAuth import blue_auth
    app.register_blueprint(blue_auth)
    from .BlueUser import  blue_user
    app.register_blueprint(blue_user)

    from .BlueCron import blue_cron
    app.register_blueprint(blue_cron)

    return app
