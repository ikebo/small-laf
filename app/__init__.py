"""
  Created by kebo on 2018/7/28
"""

from flask import Flask, jsonify, Response
from app.utils.res import Res
from app.utils.cache import cached, delete_like
import os

from flask_cache import Cache
app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)   # 注册缓存
# 重写缓存key_prefix机制
cache.cached = cached
cache.delete_like = delete_like

app.config.from_object('app.settings')


# 注册蓝图
from app.api.v1 import api_v1 as api_v1_blueprint
app.register_blueprint(api_v1_blueprint, url_prefix='/service/api/v1')

from app.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/service/admin')


@app.route('/service/static/uploads/<path>/<uri>')
def get_image(path, uri):
    sep = os.path.sep
    uri = path + sep + uri
    print('uri ', uri)
    imgPath = os.path.abspath('.') + sep + 'app' + sep + 'static' + sep + 'uploads' + sep
    imgPath = imgPath + uri
    print('imgPath ', imgPath)
    mdict = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif'
    }
    mime = mdict[((uri.split(sep)[1]).split('.')[1])]
    print('mime ', mime)
    if not os.path.exists(imgPath):
        return jsonify(Res(0, 'image does not exists').raw())
    with open(imgPath, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mime)

@app.route('/service/')
def hello():
    return '<h2>Hello Service</h2>'

# 创建数据库
from app.models import db

with app.app_context():
    db.init_app(app)
    db.create_all()
