# coding=utf-8

import datetime

def test_job_notice():
    # TODO: send notice
    print datetime.datetime.now().strftime("%Y%m%d %H%M%S")

def test_job_conversation():
    # TODO: create ding conversation
    print u"创建钉钉会话"

FUNC_MAP = {'app.BlueCron.job:test_job_notice':test_job_notice, \
            'app.BlueCron.job:test_job_conversation':test_job_conversation, \
}