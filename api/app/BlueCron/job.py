# coding=utf-8

import datetime
import hashlib
import xml.etree.cElementTree as ET

import requests
from requests.exceptions import HTTPError
from flask import current_app
from sqlalchemy import exc

from ..models import Duty, TempText, NoticeRecord
from .. import db, cron_scheduler

def listener_cronEvent(event, **kwargs):
    if event.exception:
        with cron_scheduler.app.app_context():
            if current_app.config['DEBUG']:
                current_app.logger.debug("jid:{jid}\nstore:{jstore}\ninfo:{e}".format(jid=event.job_id, \
                    jstore = event.jobstore, \
                    e = event.exception, \
                ))
            else:
                current_app.logger.error("{t} {jstore} {jid} \"{e}\"".format(t=datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f'), \
                    jstore = event.jobstore, \
                    jid = event.job_id, \
                    e = event.exception, \
                ))
            #
        #
    else:
        psss
    #

def test_job_notice():
    # TODO: send notice
    print datetime.datetime.now().strftime("%Y%m%d %H%M%S")
    # raise ValueError("SMS environment error.")
    raise HTTPError('SMS gateway requests error')
    # raise ValueError("mobile list is empty.")
    # raise exc.SQLAlchemyError('failed to add notice record')

def test_job_conversation():
    # TODO: create ding conversation
    print u"创建钉钉会话"

def daily_sms_notice():
    result = False
    with cron_scheduler.app.app_context():
        sn = current_app.config.get('SMS_SN', None)
        pw = current_app.config.get('SMS_PW', None)
        gw = current_app.config.get('SMS_GW', None)
        query_sms_temp = TempText.query.with_entities(TempText.content).filter_by(name='SMS').first()
        if all([sn, pw, gw, query_sms_temp]):
            r = NoticeRecord()
            r.kind = 'SMS'
            next_day_tag = datetime.date.today()+datetime.timedelta(days=1)
            query_mobiles = Duty.query.with_entities(Duty.mobile).\
                            filter(Duty.mobile.isnot(None)).filter_by(duty_time=next_day_tag).distinct().all()
            sms_content = u"[央视网] "+query_sms_temp[0].encode('utf-8').format(TOMORROW=next_day_tag.strftime("%Y-%m-%d")).decode('utf-8')
            if query_mobiles:
                pwd = hashlib.md5(sn+pw).hexdigest().upper()
                gw_data = {}
                gw_data['sn'] = sn
                gw_data['pwd'] = pwd
                gw_data['mobile'] = ",".join([i[0] for i in set(query_mobiles)])
                gw_data['content'] = sms_content.encode('gb2312')
                gw_data['ext'] = ''
                gw_data['stime'] = ''
                gw_data['rrid'] = ''

                resp = requests.get(gw+'/mt', params=gw_data)
                if resp.status_code == 200:
                    xxl = ET.fromstring(resp.text)
                    r.info = u"tag:success|http:200|smsid:{sms}".format(sms=xxl.text)
                    result = True
                else:
                    r.info = u"tag:error|http:{http_code}".format(http_code=resp.status_code)
                    # TODO: 抛aps异常
                    raise HTTPError('SMS gateway requests error, http:{hcode}'.format(hcode=resp.status_code))
                #
            else:
                r.info = u"tag:error|{d}运维值班手机号列表为空".format(d=next_day_tag.strftime('%Y%m%d'))
                # TODO: 抛aps异常
                raise ValueError("{d} mobile list is empty.".format(d=next_day_tag.strftime('%Y%m%d')))
            #
            db.session.add(r)
            try:
                db.session.commit()
            except Exception, e:
                db.session.rollback()
                # TODO: 抛aps异常
                raise exc.SQLAlchemyError('failed to add notice record')
            else:
                result = True
            #
        else:
            # TODO: 抛aps异常
            raise ValueError("SMS environment error.")
        #
    return result

FUNC_MAP = {'app.BlueCron.job:test_job_notice':{'func':test_job_notice, 'info':u"[测试] 通知任务"}, \
            'app.BlueCron.job:test_job_conversation':{'func':test_job_conversation, 'info':u"[测试] 钉钉建群任务"}, \
            'app.BlueCron.job:daily_sms_notice':{'func':daily_sms_notice, 'info':u"[短信] 第二天值班短信通知"}, \
}
