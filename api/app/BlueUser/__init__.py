# coding=utf-8

from flask import Blueprint


blue_user = Blueprint('blue_user', __name__, url_prefix='/users')

from . import user