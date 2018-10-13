import json

from flask import request, jsonify, session

from app.utils.decorators import log
from app.utils.res import Res
from app.utils.util import admin_auth
from . import api_v1

def R(r):
    return '/admin' + r

@api_v1.route(R('/login'), methods=['POST'])
@log
def login():
    data = json.loads(str(request.data, encoding='utf-8'))
    if admin_auth(data):
        session['admin'] = True
        return jsonify(Res(1, 'login successfully').raw())
    else:
        return jsonify(Res(0, 'username or password not correct.').raw())
