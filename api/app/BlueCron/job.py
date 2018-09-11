# coding=utf-8

import datetime

def test_job_notice():
    # TODO: send notice
    print datetime.datetime.now().strftime("%Y%m%d %H%M%S")

def test_job_conversation():
    # TODO: create ding conversation
    print u"创建钉钉会话"

FUNC_MAP = {'app.BlueCron.job:test_job_notice':{'func':test_job_notice, 'info':u"[测试] 通知任务"}, \
            'app.BlueCron.job:test_job_conversation':{'func':test_job_conversation, 'info':u"[测试] 钉钉建群任务"}, \
}
