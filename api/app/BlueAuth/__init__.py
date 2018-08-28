# coding=utf-8

from flask import Blueprint

blue_auth = Blueprint('blue_auth', __name__, url_prefix='/blue_auth')

from . import views
