# coding=utf-8

# 导入蓝图
from flask import Blueprint


# 创建蓝图对象
blue_watch = Blueprint('blue_watch', __name__)

# 导入使用蓝图对象的模块
from . import views
