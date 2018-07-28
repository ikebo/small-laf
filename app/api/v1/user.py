"""
  Created by kebo on 2018/7/28
"""
import json

from flask import jsonify
from flask import request

from app.utils.res import Res
from . import api_v1
from app.utils.http import HTTP
from app.models.user import User

from app.models import db

def R(r):
    return '/user' + r


@api_v1.route(R('/<code>'), methods=['GET'])
def get(code):
    # 获得session_key， 用户的openId
    sessionApi = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx597fa5ad3a318789&secret=74bccd487ac5429f98b7bc669366de53&js_code={}&grant_type=authorization_code'
    targetApi = sessionApi.format(code)

    # 返回值
    code = 0
    msg = 'user does not exist, but has been registered.'
    userdata = None

    res = HTTP.get(targetApi)  # dict
    print(res)
    # code出错
    if 'errcode' in res:
        code = 2
        msg = res['errmsg']
        res = Res(code, msg, userdata).json()
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
    userdata = user.json()

    res = Res(code, msg, userdata).json()

    return jsonify(res)


@api_v1.route('/avatar/<int:user_id>', methods=['POST'])
def update_avatar(user_id):
    user = User.query_user_by_id(user_id)
    if user is None:
        return jsonify(Res(0,'user deos not exist').json())

    data = json.loads(str(request.data, encoding='utf-8'))
    print(data)
    if user.update_avatar(data):
        userData = user.get_contact()
        return jsonify(Res(1, 'update avatar successfully', userData).json())
    else:
        return jsonify(Res(2, 'something error.').json())