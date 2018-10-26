# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/21
from . import api_v1
from app.utils.advice import get_yesterday_advice
from app.utils.res import Res
from flask import jsonify


# 接口URL: http://localhost:3000/service/api/v1/advice
# 建议接口 -> 请求获得昨天提交的建议
@api_v1.route('/advice', methods=["GET"])
def get_advices():
    try:
        data = get_yesterday_advice()
        if isinstance(data, bytes):                 # 如果是bytes转成str -> json无法dumps bytes
            data = str(data, encoding='utf-8')
        return jsonify(Res(1, 'get advices successfully', data).raw())
    except Exception as e:
        print(e)
    return jsonify(Res(0, 'something error').raw())
