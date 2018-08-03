"""
  Created by kebo on 2018/7/28
"""

from flask import Flask

app = Flask(__name__)

app.config.from_object('app.settings')

# 注册蓝图
from app.api.v1 import api_v1 as api_v1_blueprint
app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

@app.route('/service/')
def hello():
    return '<h2>Hello Service</h2>'

# 创建数据库
from app.models import db
with app.app_context():
    db.init_app(app)
    db.create_all()
