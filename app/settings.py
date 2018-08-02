"""
  Created by kebo on 2018/7/28
"""
import os
from app import app

SQLALCHEMY_DATABASE_URI = r'sqlite:///service.sqlite3'

UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif'}

# 最大 1M
MAX_CONTENT_LENGTH = 1 * 1024 * 1024