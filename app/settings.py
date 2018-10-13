"""
  Created by kebo on 2018/7/28
"""
import os
from app import app

SQLALCHEMY_DATABASE_URI = r'sqlite:///service.sqlite3'

SECRET_KEY = '7fc7ey1a5n7ge43eev7e8r041f0ae75976e8bd576'

UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif'}

ADVICE_PATH = UPLOAD_FOLDER + os.path.sep + 'advice.txt'

# 最大 1M
MAX_CONTENT_LENGTH = 1 * 1024 * 1024

SERVER = 'https://ikebo.cn/service'

EMAIL_PWD = 'yang4ever'

APP_ID = 'wx07be1dea85bf1254'
APP_SECRET = 'b1dad89211712612fc25cc498bc9efc5'

ADMIN_USERNAME = '21232f297a57a5a743894a0e4a801fc3'
ADMIN_PWD = 'aae315a6ff9bbc14ae0667762e0e330c'

# appid = 'wx597fa5ad3a318789'
# appsecret = '3cbe23dd818482327192b5091f0134a3'
