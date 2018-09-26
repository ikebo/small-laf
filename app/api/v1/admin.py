import json

from flask import request, jsonify, session
from app.utils.res import Res
from . import api_v1
from app import app

def R(r):
    return '/admin' + r

@api_v1.route(R('/login'), methods=['POST'])
def login():
    data = json.loads(str(request.data, encoding='utf-8'))
    if data.get('username', None) == 'admin' and data.get('password', None) == app.config['SECRET_KEY']:
        session['admin'] = True
        return jsonify(Res(1, 'login successfully').raw())
    else:
        return jsonify(Res(0, 'username or password not correct.').raw())