# coding=utf-8

import datetime, time

from flask import (current_app, request, jsonify)
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError

from . import blue_cron
from .job import FUNC_MAP

TRIGGER_TYPE = ['interval', 'cron']

# JOBs
@blue_cron.route('/jobs', methods=['GET', 'POST'])
def jobs_index():
    # TODO: query
    return jsonify('jobs_index')

@blue_cron.route('/jobs/<jid>', methods=['GET', 'PATCH', 'DELETE'])
def jobs_operate_single(jid):
    # TODO: operate job with jid
    return jsonify('jobs_operate_single')

@blue_cron.route('/jobs/<jid>/pause', methods=['POST'])
def jobs_pause_singel(jid):
    # TODO: pause job with jid
    return jsonify('jobs_pause_singel')

@blue_cron.route('/jobs/<jid>/resume', methods=['POST'])
def jobs_resume_singel(jid):
    # TODO: resume job with jid
    return jsonify('jobs_resume_singel')

# SCHEDULERs
@blue_cron.route('/schedulers', methods=['GET'])
def schedulers_index():
    # TODO: query all schedulers
    return jsonify('schedulers_index')

@blue_cron.route('/schedulers/<sname>/pause', methods=['POST'])
def schedulers_pause_single(sname):
    # TODO: pause scheduler with sname
    return jsonify('schedulers_pause_single')

@blue_cron.route('/schedulers/<sname>/resume', methods=['POST'])
def schedulers_resume_single(sname):
    # TODO: resume scheduler with sname
    return jsonify('schedulers_resume_single')

# JOBSTOREs
@blue_cron.route('/jobstores', methods=['GET'])
def jobstores_index():
    # TODO: query all jobstores
    return jsonify('jobstores_index')

@blue_cron.route('/jobstores/<jsname>', methods=['GET'])
def jobstores_query_single(jsname):
    # TODO: query with jsname
    return jsonify('jobstores_query_single')
