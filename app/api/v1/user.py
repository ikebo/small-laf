"""
  Created by kebo on 2018/7/28
"""

from . import api_v1

def R(r):
    return '/user' + r

@api_v1.route(R('/get'), methods=['GET'])
def get():
    return 'yes'