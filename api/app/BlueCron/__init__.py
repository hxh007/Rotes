# coding=utf-8

from flask import Blueprint

blue_cron = Blueprint('blue_cron', __name__, url_prefix='/cron')

from . import views
