"""
  Created by kebo on 2018/7/28
"""
import json

class Res():
    def __init__(self, code, msg, userdata=None):
        self.code = code
        self.msg = msg
        self.userdata = userdata

    def json(self):
        d = dict(code=self.code, msg = self.msg, userData = self.userdata)
        return json.dumps(d)