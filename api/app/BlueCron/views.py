# coding=utf-8

import datetime, time
import uuid
import hashlib
import xml.etree.cElementTree as ET

from flask import (current_app, request, jsonify)
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError
import requests

from . import blue_cron
from .job import FUNC_MAP

TRIGGER_TYPE = ['interval', 'cron']
SCHEDULER_STATE_MAP = {0:'STOPPED', 1:'RUNNING', 2:'PAUSED'}

# FUNCs
@blue_cron.route('/funcs', methods=['GET'])
def func_index():
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':[], \
    }
    try:
        result['detail'].extend([{'func':k, 'info':v.get('info', '')} for k,v in FUNC_MAP.items()])
    except Exception, e:
        result['msg'] = u"[error] 获取Func类型列表出错"
        code = 500
    else:
        result['msg'] = u"[success] 获取Func类型列表成功"
        result['ret'] = 0
        code = 200
    return jsonify(result), code

# TRIGGERs
@blue_cron.route('/triggers', methods=['GET'])
def trigger_index():
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':[], \
    }
    try:
        result['detail'].extend(TRIGGER_TYPE)
    except Exception, e:
        result['msg'] = u"[error] 获取Trigger类型列表出错"
        code = 500
    else:
        result['msg'] = u"[success] 获取Trigger类型列表成功"
        result['ret'] = 0
        code = 200
    return jsonify(result), code

# JOBs
@blue_cron.route('/jobs', methods=['GET', 'POST'])
def jobs_index():
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':[], \
    }

    if request.is_json:
        data = request.get_json()
    else:
        data = request.values
    #
    req_method = request.method

    if req_method == 'GET':
        try:
            all_jobs = current_app.apscheduler.get_jobs()
        except Exception, e:                
            result['msg'] = u"[error] 获取所有Job实例出错"
            code = 500
        else:
            result['detail'].extend([\
                                    {'id':j.id, 'name':j.name, \
                                    'func':j.func_ref, \
                                    'next_run':str(time.mktime(j.next_run_time.timetuple())) \
                                        if j.next_run_time else None\
                                    } \
                                for j in all_jobs])
            result['msg'] = u"[success] 获取所有Job信息成功"
            result['ret'] = 0
            code = 200
    elif req_method == 'POST':
        try:
            data.pop('id')
        except KeyError:
            pass
        func = data.get('func', None)
        kwargs = data.get('kwargs', None)
        trigger = data.get('trigger', None)
        if all([func, trigger]) and (func in FUNC_MAP.keys()) and (trigger in TRIGGER_TYPE):
            try:
                new_job = current_app.apscheduler.add_job(id=uuid.uuid4().hex, **data)
            except ConflictingIdError, e:
                result['msg'] = u"[error] JobID已经存在"
                code = 409
            except Exception, e:
                result['msg'] = u"[error] 添加Job操作失败"
                code = 500
            else:
                new_job_info = {}
                new_job_info['id'] = new_job.id
                new_job_info['name'] = new_job.name
                new_job_info['func_ref'] = new_job.func_ref
                new_job_info['next_run_time'] = str(time.mktime(new_job.next_run_time.timetuple())) if \
                                                    new_job.next_run_time else None
                new_job_info['trigger'] = new_job.trigger.__class__.__name__
                new_job_info['jobstore'] = new_job._jobstore_alias
                result['detail'].append(new_job_info)
                result['msg'] = u"[success] 添加Job操作成功"
                result['ret'] = 0
                code = 201
        else:
            result['msg'] = u"[error] 请求参数不合法"
        #
    #
    return jsonify(result), code

@blue_cron.route('/jobs/<jid>', methods=['GET', 'DELETE'])
def jobs_operate_single(jid):
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':{}, \
    }
    try:
        job = current_app.apscheduler.get_job(jid)
        if not job:
            raise JobLookupError(jid)
        #
    except JobLookupError, e:
        result['msg'] = u"[error] 没有找到指定的 Job<{0}>".format(jid)            
        code = 404
    else:
        req_method = request.method
        if req_method == 'GET':
            result['detail']['id'] = jid
            result['detail']['name'] = job.name
            result['detail']['func_ref'] = job.func_ref
            result['detail']['next_run_time'] = str(time.mktime(job.next_run_time.timetuple())) if \
                                                job.next_run_time else None
            result['detail']['trigger'] = job.trigger.__class__.__name__
            result['detail']['jobstore'] = job._jobstore_alias
            result['msg'] = u"[success] 获取指定Job信息成功"
            result['ret'] = 0
            code = 200
        elif req_method == 'DELETE':
            try:
                job.remove()
            except Exception, e:
                result['msg'] = u"[error] 删除指定 Job<{0}> 操作出错".format(jid)
                code = 500
            else:
                result['msg'] = u"[success] 删除指定 Job<{0}> 操作完成".format(jid)
                result['ret'] = 0
                code = 200
        #
    return jsonify(result), code

@blue_cron.route('/jobs/<jid>/pause', methods=['POST'])
def jobs_pause_singel(jid):
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':{}, \
    }
    try:
        job = current_app.apscheduler.get_job(jid)
        if not job:
            raise JobLookupError(jid)
    except JobLookupError, e:
        result['msg'] = u"[error] 没有找到指定的 Job<{0}>".format(jid)
        code = 404
    else:
        try:
            job.pause()
        except Exception, e:
            result['msg'] = u"[error] 暂停 Job<{0}> 操作出错".format(jid)
            code = 500
        else:
            result['msg'] = u"[success] 暂停 Job<{0}> 操作完成".format(jid)
            result['ret'] = 0
            code = 200
    return jsonify(result), code

@blue_cron.route('/jobs/<jid>/resume', methods=['POST'])
def jobs_resume_singel(jid):
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':{}, \
    }
    try:
        job = current_app.apscheduler.get_job(jid)
        if not job:
            raise JobLookupError(jid)
    except JobLookupError, e:
        result['msg'] = u"[error] 没有找到指定的 Job<{0}>".format(jid)
        code = 404
    else:
        try:
            job.resume()
        except Exception, e:
            result['msg'] = u"[error] 恢复 Job<{0}> 操作出错".format(jid)
            code = 500
        else:
            result['msg'] = u"[success] 恢复 Job<{0}> 操作完成".format(jid)
            result['detail']['next_run'] = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S.%f') if job.next_run_time else None
            result['ret'] = 0
            code = 200
    return jsonify(result), code

# SCHEDULERs
@blue_cron.route('/schedulers', methods=['GET'])
def schedulers_index():
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':{}, \
    }
    try:
        result['detail']['type'] = str(current_app.apscheduler.scheduler.__class__.__name__)
        result['detail']['status'] = SCHEDULER_STATE_MAP.get(current_app.apscheduler.scheduler.state, 'UNKNOW')
        result['detail']['tz'] = str(current_app.apscheduler.scheduler.timezone.zone)
    except Exception, e:
        result['msg'] = u"[error] 获取Schedule信息失败"
        code = 500
    else:
        result['msg'] = u"[success] 获取Schedule信息成功"
        result['ret'] = 0
        code = 200
    return jsonify(result), code

@blue_cron.route('/schedulers/pause', methods=['POST'])
def schedulers_pause_single():
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':{}, \
    }
    try:
        current_app.apscheduler.scheduler.pause()
    except Exception, e:
        result['msg'] = u"[error] Schedule暂停操作出错"
        code = 500
    else:
        result['msg'] = u"[success] Schdeuler暂停操作完成"
        result['detail']['current'] = SCHEDULER_STATE_MAP.get(current_app.apscheduler.scheduler.state, 'UNKNOW')
        result['ret'] = 0
        code = 200
    return jsonify(result), code

@blue_cron.route('/schedulers/resume', methods=['POST'])
def schedulers_resume_single():
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':{}, \
    }
    try:
        current_app.apscheduler.scheduler.resume()
    except Exception, e:
        result['msg'] = u"[error] Scheduler恢复操作出错"
        code = 500
    else:
        result['msg'] = u"[success] Schdeuler恢复操作完成"
        result['detail']['current'] = SCHEDULER_STATE_MAP.get(current_app.apscheduler.scheduler.state, 'UNKNOW')
        result['ret'] = 0
        code = 200
    return jsonify(result), code

# JOBSTOREs
@blue_cron.route('/jobstores', methods=['GET'])
def jobstores_index():
    code = 400
    result = {'ret':1, \
            'msg': u"[error] 默认信息", \
            'detail': [], \
    }
    try:
        all_js = current_app.apscheduler.scheduler._jobstores
    except Exception, e:
        result['msg'] = u"[error] 内部获取JobStore实例失败"
        code = 500
    else:
        for k,v in all_js.items():
            result['detail'].append({'alias':k, 'ref':v.__repr__()})
        #
        result['ret'] = 0
        result['msg'] = u"[success] 查询所有JobStore成功"
        code = 200
    return jsonify(result), code

@blue_cron.route('/jobstores/<jsname>', methods=['GET'])
def jobstores_query_single(jsname):
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':{}
    }
    try:
        queryed_js = current_app.apscheduler.scheduler._jobstores.get(jsname, None)
        if queryed_js:
            result['detail']['alias'] = jsname
            result['detail']['ref'] = queryed_js.__repr__()
            result['msg'] = u"[success] 查询指定 JobStore<{0}> 成功".format(jsname)
            result['ret'] = 0
            code = 200
        else:
            result['msg'] = u"[error] 没有找到指定的 JobStore<{0}>".format(jsname)
            code = 404
    except Exception, e:
        result['msg'] = u"[error] 内部获取 JobStore<{0}> 实例失败".format(jsname)
        code = 500
    return jsonify(result), code

# SEND SMS MESSAGE
@blue_cron.route('/sms', methods=['POST'])
def send_sms_message():
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':{}, \
    }
    if request.is_json:
        data = request.get_json()
    else:
        data = request.values
    #

    sn = current_app.config.get('SMS_SN', None)
    pw = current_app.config.get('SMS_PW', None)
    gw = current_app.config.get('SMS_GW', None)
    if all([sn, pw, gw]):
        query_mobiles = data.get('mobiles', [])
        sms_content = data.get('message', '')
        fomted_sms_content = u"[央视网] "+sms_content
        if query_mobiles:
            pwd = hashlib.md5(sn+pw).hexdigest().upper()
            gw_data = {}
            gw_data['sn'] = sn
            gw_data['pwd'] = pwd
            gw_data['mobile'] = ",".join(set(query_mobiles))
            gw_data['content'] = fomted_sms_content.encode('gb2312')
            gw_data['ext'] = ''
            gw_data['stime'] = ''
            gw_data['rrid'] = ''

            resp = requests.get(gw+'/mt', params=gw_data)
            if resp.status_code == 200:
                xxl = ET.fromstring(resp.text)
                result['msg'] = u"[success] 已经发送:{sms}".format(sms=xxl.text)
                result['ret'] = 0
                code = 202
            else:
                result['msg'] = u"[error] 短信网关错误: HTTP{http_code}".format(http_code=resp.status_code)
            #
        else:
            result['msg'] = u"[error] 手机号列表为空"
        #
    else:
        result['msg'] = u"[error] 短信环境变量错误"
        code = 500
    #
    return jsonify(result), code

# CREATE DING CONVERSATION
@blue_cron.route('/ding', methods=['POST'])
def create_ding_conversation():
    code = 400
    result = {'ret':1, \
            'msg':u"[error] 默认信息", \
            'detail':{}, \
    }
    if request.is_json:
        data = request.get_json()
    else:
        data = request.values
    #

    ding_userids = data.get('userids', []) 
    ding_message = data.get('message', '')
    
    if ding_userids and isinstance(ding_userids, list):
        today_tag = datetime.datetime.now()

        # request params
        req_data = {}
        req_data['name'] = u"{0}人工".format(today_tag.strftime("%Y%m%d%H%M%S"))
        req_data['msg'] = ding_message
        req_data['owner'] = current_app.config['DING_DEFAULT_OWNER']
        req_data['userlist'] = list(set(ding_userids))

        ding_gw = current_app.config['DING_GW']
        req = requests.post(ding_gw, json=req_data, headers={'Content-Type':'application/json'})
        if req.status_code == 201:
            try:
                resp = req.json()
            except Exception, e:
                result['msg'] = u"[error] 建群接口Resp无法解析成JSON"
                code = 500
            else:
                result['ret'] = 0
                result['msg'] = u"[success] 创建成功: id{tid}".format(tid=resp['detail'].get('chatid', ''))
                code = 202
        else:
            result['msg'] = u"[error] 调用建群接口失败: HTTP{http_code}".format(http_code=req.status_code)
        #
    else:
        result['msg'] = u"[error] 请求参数不合法"

    return jsonify(result), code
