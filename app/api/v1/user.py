"""
  Created by kebo on 2018/7/28
"""
import json
import os
from flask import jsonify
from flask import request, make_response
import threading
from multiprocessing import Process

from app.utils.decorators import log
from app.utils.res import Res
from app.utils.util import format_advice
from . import api_v1
from app.utils.http import HTTP
from app.models.user import User
from app.utils.em import send_email
from app.models import db
from app import app
from app import cache
from app.utils.http import request_auth, get_personal_info, get_course_info

def R(r):
    return '/user' + r


@api_v1.route(R('/<code>'), methods=['GET'])
@log
def get(code):
    # 获得session_key， 用户的openId
    sessionApi = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'
    targetApi = sessionApi.format(app.config['APP_ID'], app.config['APP_SECRET'], code)
    
    # 返回值
    code = 1
    msg = 'user does not exist, but has been registered.'
    data = None

    res = HTTP.get(targetApi)  # dict
    print(res)
    # code出错
    if 'errcode' in res:
        code = 2
        msg = res['errmsg']
        res = Res(code, msg, data).raw()
        return jsonify(res)

    # 正常, 获得openId
    openId = res['openid']
    user = User.query_user_by_openId(openId)

    # 根据user构造返回值
    if user is not None:
        code = 1
        msg = 'user exist'
    else:
        user = User(openId)
        db.session.add(user)
        db.session.commit()

    print(user.id)
    data = user.raw()

    res = Res(code, msg, data).raw()

    return jsonify(res)


@api_v1.route(R('/<int:user_id>'), methods=['GET'])
@log
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify(Res(0, 'user does not exsits').raw())
    else:
        return jsonify(Res(1, 'get user successfully', user.raw()).raw())


@api_v1.route(R('/avatar/<int:user_id>'), methods=['POST'])
@log
def update_avatar(user_id):
    user = User.query_user_by_id(user_id)
    if user is None:
        return jsonify(Res(0, 'user does not exist').raw())

    data = json.loads(str(request.data, encoding='utf-8'))
    print(data)
    if user.update_avatar(data):
        return jsonify(Res(1, 'update avatar successfully').raw())
    else:
        return jsonify(Res(2, 'something error.').raw())


@api_v1.route(R('/contact/<int:user_id>'), methods=['POST'])
def update_contact(user_id):
    user = User.query_user_by_id(user_id)
    if user is None:
        return jsonify(Res(0, 'user does not exist').json())

    data = json.loads(str(request.data, encoding='utf-8'))
    print(data)
    if user.update_contact(data):
        return jsonify(Res(1, 'update contact successfully').json())
    else:
        return jsonify(Res(2, 'something error.').json())


@api_v1.route(R(''), methods=['GET'])
@log
def get_users():
    try:
        users = User.query.all()
        users = [user.raw() for user in users]
        if users is not None:
            return jsonify(Res(1, 'get users successfully', users).raw())
        return jsonify(Res(0, 'get users failed').raw())
    except Exception as e:
        print(e)
        return jsonify(Res(2, 'something error').raw())

@api_v1.route(R('/advice'), methods=['POST'])
@log
def advice():
    try:
        data = json.loads(str(request.data, encoding='utf-8'))
        user_id = str(data['user_id'])
        advice = format_advice(user_id, data['advice'])
        print(advice)
        # send_email_worker = threading.Thread(target=send_email, args=(advice,))
        # send_email_worker.start()
        # send_email_worker.join()
        # worker = Process(target=send_email, args=(advice,))
        # worker.start()
        with open(app.config['ADVICE_PATH'], 'a') as f:
            f.write(advice)
        return jsonify(Res(1, 'post advice successfully').raw())
    except Exception as e:
        print(e)
        return jsonify(Res(2, 'something error').raw())


@api_v1.route(R('/course'), methods=['POST'])
@log
def get_course():
    try:
        username = request.form['stu_id']
        password = request.form['stu_pwd']
        res = get_course_info(username, password)
        if not res:
            return jsonify(Res(0, 'fail').raw())
        return jsonify(Res(1, 'success', res).raw())
    except Exception as e:
        return jsonify(Res(2, 'something error').raw())

@api_v1.route(R('/personal'), methods=['POST'])
@log
def get_personal():
    try:
        username = request.form['stu_id']
        password = request.form['stu_pwd']
        res = get_personal_info(username, password)
        if not res:
            return jsonify(Res(0, 'fail').raw())
        return jsonify(Res(1, 'success', res).raw())
    except Exception as e:
        return jsonify(Res(2, 'something error').raw())


@api_v1.route(R('/auth'), methods=['POST'])
def auth():
    try:
        # data = json.loads(str(request.data, encoding='utf-8'))
        # print('..')
        # user_id = data['user_id']
        # print('..', data)
        # stu_id = data['stu_id']
        # stu_pwd = data['stu_pwd']
        # print('...')
        stu_id = request.form['stu_id']
        stu_pwd = request.form['stu_pwd']
        if request_auth(stu_id, stu_pwd):
            # user = User.query.get(user_id)
            # if user.set_auth():
            return jsonify(Res(1, 'success').raw())
        else:
            return jsonify(Res(0, '密码错误').raw())
    except Exception as e:
        print(e)
        return jsonify(Res(2, 'something error').raw())


@api_v1.route(R('/wxauth'), methods=['GET'])
@log
def wxauth():
    code = request.args.get('code', 'fail to get code')
    response = make_response(code, 200)
    response.headers['Content-type'] = 'text/plain'
    return response
    

@api_v1.route(R('/<int:user_id>'), methods=['DELETE'])
@log
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify(Res(0, 'user does not exists').raw())
    if user.delete():
        return jsonify(Res(1, 'delete user successfully').raw())
    else:
        return jsonify(Res(2, 'something error').raw())
