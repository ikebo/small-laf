"""
  Created by kebo on 2018/10/12
"""
import os
from datetime import datetime
from app import app
from flask import request, Response, url_for, session, redirect
from functools import wraps
import json

from app.utils.file import get_current_date


# login_required 装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('admin', None):
            return redirect(url_for('.login'))
        return func(*args, **kwargs)
    return wrapper


# log 装饰器, 状态不正常才打log
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        response = json.loads(str(result.response[0], encoding='utf-8'))
        if response.get('code',None) is not 1:
            # 异常情况, 将请求信息 及 响应信息输出到文件
            log_content = _generate_log(response)
            _logto_file(log_content)
        return result
    return wrapper


# 将log内容输出到文件,
def _logto_file(content):
    log_name = get_current_date() + '.txt'
    file = url_for('static', filename='log/{}'.format(log_name))
    file = os.path.join(app.static_folder, 'log/{}'.format(log_name))
    if not os.path.exists(file):
        open(file, 'w')
    with open(file, 'a+') as f:
        f.write(content)

# 生成log内容
def _generate_log(response):
    t = datetime.now().strftime("%m-%d %H:%M:%S")
    log_header = '[{0}] {1} {2}'.format(t, request.method, request.full_path)
    log_body = 'code:{}  msg:{}'.format(response.get('code',None),response.get('msg',None))
    return log_header + '\n' + log_body + '\n\n'