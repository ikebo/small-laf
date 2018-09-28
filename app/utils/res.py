"""
  Created by kebo on 2018/7/28
"""
import json

class Res():
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def json(self):
        d = dict(code=self.code, msg = self.msg, data = self.data)
        return json.dumps(d)

    def raw(self):
        return dict(code=self.code, msg = self.msg, data=self.data)
