# coding=utf-8

from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


# 基类
class BaseModel():
    ctime = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now, index=True)
    lastchange = db.Column(db.DateTime(timezone=True), nullable=True, default=datetime.now, onupdate=datetime.now)
    status = db.Column(db.Boolean, default=True)
    remark = db.Column(db.String(128), nullable=True)  # 备用字段


# 值班表
class Duty(BaseModel, db.Model):
    __tablename__ = 'duty'
    id = db.Column(db.Integer, primary_key=True, index=True)
    depart = db.Column(db.String(64), nullable=False)   # 部门
    role = db.Column(db.String(64), nullable=False)    # 角色
    duty_name = db.Column(db.String(64), nullable=False)  # 值班人
    duty_time = db.Column(db.Date(), nullable=False, index=True)  # 值班时间

    def __repr__(self):
        return '<Duty %r>' % self.duty_name


# 短信内容模板表
class TempText(BaseModel, db.Model):
    __tablename__ = 'temptext'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(64))     # 名字
    content = db.Column(db.String(256), nullable=False)  # 短信内容

    def __repr__(self):
        return '<TempText %r>' % self.content


# houxianghui
def db_session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason

# 角色用户表，建立用户和角色多对多的关系
tb_role_user = db.Table(
    "info_role_user",
    db.Column("role_id", db.Integer, db.ForeignKey("info_role.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True)
)

# 部门用户表 建立部门和用户多对多的关系
tb_department_user = db.Table(
    "info_department_user",
    db.Column("department_id", db.Integer, db.ForeignKey("info_department.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True),
    db.Column('ctime', db.DateTime(timezone=True), default=datetime.now)
)

# 部门角色表 建立部门和角色多对多的关系
tb_department_role = db.Table(
    'info_department_role',
    db.Column('department_id', db.Integer, db.ForeignKey('info_department.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('info_role.id'), primary_key=True)
)

# 管理员用户表 建立管理员和用户的多对多关系
tb_manager_user = db.Table(
    'info_manager_user',
    db.Column('manager_id', db.Integer, db.ForeignKey('info_manager.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True)
)

# 管理员权限表 建立管理员和权限的多对多关系
tb_manager_permission = db.Table(
    'info_manager_permission',
    db.Column('manager_id', db.Integer, db.ForeignKey('info_manager.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('info_permission.id'), primary_key=True)
)

# 用户表
class User(BaseModel, db.Model):
    __tablename__ = 'info_user'
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    alias = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    login_time = db.Column(db.Integer)

    @property
    def password(self):
        raise AttributeError('self.password is unreadable')

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.status

    def add(self, user):
        db.session.add(user)
        return db_session_commit()

    def to_dict(self):
        resp_dict = {
            'id': self.id,
            'username': self.username,
            'alias': self.alias,
            'mobile': self.mobile,
            'status': self.status,
            'login_time': self.login_time,
            'laskchange': self.lastchange,
            'remark': self.remark
        }
        return resp_dict

    def __repr__(self):
        return '<User %r>' % self.username


#部门表
class Department(BaseModel, db.Model):
    __tablename__ = 'info_department'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    alias = db.Column(db.String, nullable=False, unique=True)
    # 部门用户关系
    users = db.relationship('User', secondary=tb_department_user, backref=db.backref('departments', lazy='dynamic'), lazy='dynamic')
    # 部门角色关系
    roles = db.relationship('Role', secondary=tb_department_role, backref=db.backref('department', lazy='dynamic'), lazy='dynamic')
    # 部门权限关系
    permissions = db.relationship('Permission', backref='departments', lazy='dynamic')

    def add(self, department):
        db.session.add(department)
        return db_session_commit()

    def to_dict(self):
        resp_dict = {
            'id': self.id,
            'name': self.name,
            'alias': self.alias,
            'remark': self.remark,
            'status': self.status,
            'lastchange': self.lastchange
        }
        return resp_dict

    def __repr__(self):
        return '<Departmenet %r>' % self.name


# 角色表
class Role(BaseModel, db.Model):
    __tablename__ = 'info_role'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    alias = db.Column(db.String(128))
    # 角色用户关系
    users = db.relationship('User', secondary=tb_role_user, backref=db.backref('roles', lazy='dynamic'), lazy='dynamic')

    def add(self, role):
        db.session.add(role)
        return db_session_commit()

    def to_dict(self):
        resp_dict = {
            'id': self.id,
            'name': self.name,
            'alias': self.alias,
            'remark': self.remark,
            'status': self.status,
            'lastchange': self.lastchange
        }
        return resp_dict

    def __repr__(self):
        return '<Role %r>' % self.name


# 管理员表
class Manager(BaseModel, db.Model):
    __tablename__ = 'info_manager'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    alias = db.Column(db.String(128))
    # 管理员用户关系
    users = db.relationship('User', secondary=tb_manager_user, backref=db.backref('u_managers', lazy='dynamic'), lazy='dynamic')
    # 管理员权限关系
    permissions = db.relationship('Permission', secondary=tb_manager_permission, backref=db.backref('p_managers', lazy='dynamic'), lazy='dynamic')

    def add(self, manager):
        db.session.add(manager)
        return db.session_commit()

    def to_dict(self):
        resp_dict = {
            'id': self.id,
            'name': self.name,
            'alias': self.alias,
            'remark': self.remark,
            'status': self.status,
            'lastchange': self.lastchange
        }
        return resp_dict

    def __repr__(self):
        return '<Manager %r>' % self.name


# 权限表
class Permission(BaseModel, db.Model):
    __tablename__ = 'info_permission'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    alias = db.Column(db.String(128))
    codename = db.Column(db.String(64), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('info_department.id'))

    def add(self, permission):
        db.session.add(permission)
        return db.session_commit()

    def to_dict(self):
        resp_dict = {
            'id': self.id,
            'name': self.name,
            'alias': self.alias,
            'remark': self.remark,
            'status': self.status,
            'lastchange': self.lastchange
        }
        return resp_dict

    def __repr__(self):
        return '<Permission %r>' % self.name


# 操作类型表
class Action_type(db.Model):
    __tablename__ = 'info_action_type'
    id = db.Column(db.Integer, primary_key=True, index=True)
    codename = db.Column(db.String(64), unique=True, nullable=False)
    alias = db.Column(db.String(64), unique=True, nullable=False)

    def add(self, permission):
        db.session.add(permission)
        return db.session_commit()

    def to_dict(self):
        resp_dict = {
            'id': self.id,
            'codename': self.codename,
            'alias': self.alias
        }
        return resp_dict

    def __repr__(self):
        return '<Action_type %r>' % self.codename

