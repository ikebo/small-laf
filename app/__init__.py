"""
  Created by kebo on 2018/7/28
"""

from flask import Flask, jsonify, Response
from app.utils.res import Res
import os

app = Flask(__name__)

app.config.from_object('app.settings')

# 注册蓝图
from app.api.v1 import api_v1 as api_v1_blueprint
app.register_blueprint(api_v1_blueprint, url_prefix='/service/api/v1')

from app.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')


@app.route('/service/static/uploads/<path>/<uri>')
def get_image(path, uri):
    uri = path + '/' + uri
    print('uri ', uri)
    imgPath = '/var/www/laf/app/static/uploads/' + uri
    print('imgPath ', imgPath)
    mdict = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif'
    }
    mime = mdict[((uri.split('/')[1]).split('.')[1])]
    print('mime ', mime)
    if not os.path.exists(imgPath):
        return jsonify(Res(0, 'image does not exists').raw())
    with open(imgPath, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mime)


# 创建数据库
from app.models import db

with app.app_context():
    db.init_app(app)
    db.create_all()
