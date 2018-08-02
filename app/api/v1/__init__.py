"""
  Created by kebo on 2018/7/28
"""
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__)

from . import user
from . import item