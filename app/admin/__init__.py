"""
  Created by kebo on 2018/8/9
"""

from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import index