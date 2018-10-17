# coding=utf-8
import unittest
from app import create_app, db
from app.BlueAuth.data_init import data_init

test_app = create_app('test_config')


class Alltests(unittest.TestCase):

    # 测试准备
    def setUp(self):
        self.test_app = test_app.test_client()
        db.create_all(app=test_app)

    # 测试执行完
    # def tearDown(self):
    #     with test_app.app_context():
    #         db.session.remove()
    #         db.drop_all()

    # 数据初始化
    def test_datainit(self):
        with test_app.app_context():
            data_init()

    def test_add_duty(self):
        resu = self.test_app.post('duty/1')
        print resu
if __name__ == '__main__':
    unittest.main()