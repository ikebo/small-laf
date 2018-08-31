"""
  Created by kebo on 2018/8/31
"""

from . import db
import datetime

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(60)) # 评论内容
    time = db.Column(db.DateTime)  # 评论时间

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))  # 评论所属物品
    replies = db.relationship('Reply', backref='comment',
                              lazy='dynamic')  # 评论回复

    def __init__(self, content, item_id):
        self.content = content
        self.time = datetime.datetime.now()
        self.item_id = item_id