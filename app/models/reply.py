"""
  Created by kebo on 2018/8/31
"""

from . import db
import datetime


class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(60))  # 内容
    time = db.Column(db.DateTime)       # 回复时间

    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    def __init__(self, content, comment_id):
        self.content = content
        self.time = datetime.datetime.now()
        self.comment_id = comment_id