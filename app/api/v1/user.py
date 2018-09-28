"""
  Created by kebo on 2018/7/28
"""
import json
import os
from flask import jsonify
from flask import request
import threading
from multiprocessing import Process

from app.utils.res import Res
from app.utils.util import format_advice
from . import api_v1
from app.utils.http import HTTP
from app.models.user import User
from app.utils.em import send_email
from app.models import db
from app import app

def R(r):
    return '/user' + r


@api_v1.route(R('/<code>'), methods=['GET'])
def get(code):
    # 获得session_key， 用户的openId
    sessionApi = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx597fa5ad3a318789&secret=74bccd487ac5429f98b7bc669366de53&js_code={}&grant_type=authorization_code'
    targetApi = sessionApi.format(code)

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
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify(Res(0, 'user does not exsits').raw())
    else:
        return jsonify(Res(1, 'get user successfully', user.raw()).raw())


@api_v1.route(R('/avatar/<int:user_id>'), methods=['POST'])
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
def advice():
    try:
        data = json.loads(str(request.data, encoding='utf-8'))
        user_id = str(data['user_id'])
        advice = format_advice(user_id, data['advice'])
        print(advice)
        send_email_worker = threading.Thread(target=send_email, args=(advice,))
        send_email_worker.start()
        # worker = Process(target=send_email, args=(advice,))
        # worker.start()
        with open(app.config['ADVICE_PATH'], 'a') as f:
            f.write(advice)
        send_email_worker.join()
        return jsonify(Res(1, 'post advice successfully').raw())
    except Exception as e:
        print(e)
        return jsonify(Res(2, 'something error').raw())

@api_v1.route(R('/auth'), methods=['POST'])
def auth():
    try:
        data = json.loads(str(request.data, encoding='utf-8'))
        user_id = str(data['user_id'])
        stu_id = data['stu_id']
        stu_pwd = data['stu_pwd']
        print(user_id, stu_id, stu_pwd)
        return jsonify(Res(0, '认证待开通').raw())
    except Exception as e:
        print(e)
        return jsonify(Res(2, 'something error').raw())


@api_v1.route(R('/<int:user_id>'), methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify(Res(0, 'user does not exists').raw())
    if user.delete():
        return jsonify(Res(1, 'delete user successfully').raw())
    else:
        return jsonify(Res(2, 'something error').raw())
