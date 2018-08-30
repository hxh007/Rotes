# coding=utf-8

from datetime import datetime
from app import db


class BaseModel():
    ctime = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now, index=True)
    lastchange = db.Column(db.DateTime(timezone=True), nullable=True, default=datetime.now, onupdate=datetime.now)
    status = db.Column(db.Boolean, default=True)
    remark = db.Column(db.String(128), nullable=True)  # 备用字段


class OnDuty(BaseModel, db.Model):
    __tablename__= 'onduty'
    id = db.Column(db.Integer, primary_key=True, index=True)
    department_name = db.Column(db.String(64), nullable=False)
    principal = db.Column(db.String(64), nullable=False)
    role_name = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    duty_time = db.Column(db.Date(), nullable=False, index=True)

    def __repr__(self):
        return '<OnDuty %r>' % self.name


class TempText(BaseModel, db.Model):
    __tablename__ = 'temptext'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(64))
    content = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<TempText %r>' % self.content
