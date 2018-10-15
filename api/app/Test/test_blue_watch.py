# coding=utf-8
import requests
import unittest

from flask import url_for


class TestDuty(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.add_duty = 'http://127.0.0.1:5000/duty'
        cls.duty_edit = 'http://127.0.0.1:5000/duty/<int:duty_id>'
        cls.dutyLists = 'http://127.0.0.1:5000/dutyLists'
        cls.dutysCount = 'http://127.0.0.1:5000/dutysCount'
        cls.exportduty = 'http://127.0.0.1:5000/dutyinfo'
        cls.xlsx = 'http://127.0.0.1:5000/datatoxlsx'
        cls.smsTemplate = 'http://127.0.0.1:5000/tempContent'

    def test_duty_add(self):
        params = {'departId': 1, 'roleId': 1, 'staffId': 2, 'dutyDate': '2018-08-01'}
        test_result = requests.post(self.add_duty, params=params).json()
        if test_result['msg'] == u'数据提交成功':
            print 'Success'
        else:
            print 'Fail:'+test_result['msg']
    # def test_duty_edit(self):
    #     params = {}
    #     test_result = requests.get(self.duty_edit).json()

if __name__ == '__main__':
    unittest.main()
