# coding=utf-8
from app import db
from . import blue_auth
from app.models import User, Management, ActionType, db_session_add, Role
from .datas import DEFAULT_SUPPER_MANAGEMENT, DEFAULT_SUPPER_USER, DEFAULT_ACTION, DEFAULT_ROLES


# 数据初始化
@blue_auth.before_app_first_request
def data_init():
    # 添加管理（组）
    c_managements = Management.query.with_entities(Management.name).all()
    # 添加超级管理
    if not len(c_managements):
        for m in DEFAULT_SUPPER_MANAGEMENT:
            new_management = Management()
            new_management.name = m['name']
            new_management.alias = m['alias']
            db_session_add(new_management)
    else:
        pass
    # 添加超级管理员
    c_users = User.query.with_entities(User.username).all()
    if not len(c_users):
        for s in DEFAULT_SUPPER_USER:
            new_user = User()
            new_user.username = s['username']
            new_user.fullname = s['fullname']
            new_user.mobile = s['mobile']
            new_user.password = s['password']
            management_wanted = Management.query.filter_by(name=s.get('management', 'UNKNOW')).first()
            if management_wanted:
                management_wanted.users.append(new_user)
            else:
                del new_user
                continue
            try:
                db.session.add_all([new_user, management_wanted])
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
    else:
        pass
    # 添加操作到数据库
    a_action = ActionType.query.with_entities(ActionType.codename).all()
    if len(a_action) == 0:
        for a in DEFAULT_ACTION:
            new_action = ActionType()
            new_action.codename = a['codename']
            new_action.alias = a['alias']
            db_session_add(new_action)
    else:
        pass
    # 添加角色
    r_roles = Role.query.with_entities(Role.name).all()
    if len(r_roles) == 0:
        for a in DEFAULT_ROLES:
            new_role = Role()
            new_role.name = a['name']
            new_role.alias = a['alias']
            db_session_add(new_role)
    else:
        pass
