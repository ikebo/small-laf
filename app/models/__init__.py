"""
  Created by kebo on 2018/7/28
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from . import user
from . import item