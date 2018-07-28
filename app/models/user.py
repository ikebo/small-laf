"""
  Created by kebo on 2018/7/28
"""

from . import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openId = db.Column(db.String(100), unique=True) # 用户唯一标识
    avatarUrl = db.Column(db.String(200))  # 用户头像
    nickName = db.Column(db.String(30))    # 用户名
    phoneNumber = db.Column(db.String(11)) # 手机号
    qqNumber = db.Column(db.String(11))    # QQ号  5-11位
    weixinNumber = db.Column(db.String(20)) # 微信号  6-20位
    items = db.relationship('Item', backref='user',
                                lazy='dynamic') # 用户发布的物品

    def __init__(self, openId, avatarUrl, nickName):
        self.openId = openId
        self.avatarUrl = avatarUrl
        self.nickName = nickName


    def __repr__(self):
        return '{}: {}'.format(self.nickName, self.openId)

