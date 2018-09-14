# coding=utf-8

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models import Duty, TempText, User, Department, Role, Management, Permission, ActionType

# 调用工厂方法 获取app
app = create_app('dev_config')
# 使用管理器
manager = Manager(app)
# 数据库迁移
Migrate(app, db)
# 数据库初始化
db.create_all(app=app)


# Shell 初始化
def make_shell_context():
    return dict(
        app=app, db=db, Duty=Duty, TempText=TempText, User=User, Department=Department,
        Role=Role, Management=Management, Permission=Permission, ActionType=ActionType
    )

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
