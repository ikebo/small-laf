"""
  Created by kebo on 2018/7/28
"""
import os
from app import app

SQLALCHEMY_DATABASE_URI = r'sqlite:///service.sqlite3'

SECRET_KEY = 'whxylaf'

UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif'}

ADVICE_PATH = UPLOAD_FOLDER + os.path.sep + 'advice.txt'

# 最大 1M
MAX_CONTENT_LENGTH = 1 * 1024 * 1024

# SERVER = 'http://120.79.192.233/service'
SERVER = 'http://127.0.0.1:3000'
