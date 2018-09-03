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


def db_session_commit():
    result = {'code': 0, 'msg': '数据提交成功'}
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        result['code'] = 1
        result['msg'] = u'数据提交失败'
    return result

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
tb_management_user = db.Table(
    'info_management_user',
    db.Column('management_id', db.Integer, db.ForeignKey('info_management.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True)
)

# 管理员权限表 建立管理员和权限的多对多关系
tb_management_permission = db.Table(
    'info_management_permission',
    db.Column('management_id', db.Integer, db.ForeignKey('info_management.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('info_permission.id'), primary_key=True)
)

# 用户表
class User(db.Model, BaseModel):
    __tablename__ = 'info_user'
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(128), nullable=False, unique=True) # 用户名
    fullname = db.Column(db.String(128), nullable=False) # 姓名
    mobile = db.Column(db.String(128), nullable=False, unique=True) # 手机号
    tag = db.Column(db.String(64), unique=True) # 工号
    is_department = db.Column(db.Boolean, default=False)  # 部门管理员
    password_hash = db.Column(db.String(128))
    login_time = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)

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

    # 数据提交
    def add(self, user):
        db.session.add(user)
        return db_session_commit()

    # 删除用户
    def delete(self, user):
        db.session.delete(user)
        return db_session_commit()

    def to_dict(self):
        resp_dict = {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'mobile': self.mobile,
            'tag': self.tag,
            'is_department': self.is_department,
            'status': self.status,
            'login_time': self.login_time.strftime("%Y-%m-%d %H:%M:%S"),
            'lastchange': self.lastchange.strftime("%Y-%m-%d %H:%M:%S"),
            'remark': self.remark
        }
        return resp_dict

    def add_data(self, paras):
        self.username = paras[0]
        self.fullname = paras[1]
        self.mobile = paras[2]
        self.password = paras[3]
        self.tag = paras[4]

    def add_datas(self, paras):
        self.username = paras[0]
        self.fullname = paras[1]
        self.mobile = paras[2]
        self.password = paras[3]
        self.tag = paras[4]
        self.is_department = paras[5]
        self.status = paras[6]
        self.remark = paras[7]
    def __repr__(self):
        return '<User %r>' % self.username


#部门表
class Department(db.Model, BaseModel):
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

    def add_data(self, paras):
        self.name = paras[0]
        self.alias = paras[1]

    def __repr__(self):
        return '<Departmenet %r>' % self.name


# 角色表
class Role(db.Model, BaseModel):
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
class Management(db.Model, BaseModel):
    __tablename__ = 'info_management'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    alias = db.Column(db.String(128))
    # 管理员用户关系
    users = db.relationship('User', secondary=tb_management_user, backref=db.backref('u_managements', lazy='dynamic'), lazy='dynamic')
    # 管理员权限关系
    permissions = db.relationship('Permission', secondary=tb_management_permission, backref=db.backref('p_managements', lazy='dynamic'), lazy='dynamic')

    def add(self, management):
        db.session.add(management)
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
        return '<management %r>' % self.name


# 权限表
class Permission(db.Model, BaseModel):
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
class ActionType(db.Model):
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

