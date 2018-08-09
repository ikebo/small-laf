"""
  Created by kebo on 2018/8/9
"""

from . import admin


@admin.route('/')
def index():
    return 'admin'
