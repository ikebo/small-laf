"""
  Created by kebo on 2018/7/28
"""

from . import db
import json


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openId = db.Column(db.String(100), unique=True)  # 用户唯一标识
    avatarUrl = db.Column(db.String(200))  # 用户头像
    nickName = db.Column(db.String(30))  # 用户名
    phoneNumber = db.Column(db.String(11))  # 手机号
    qqNumber = db.Column(db.String(11))  # QQ号  5-11位
    weixinNumber = db.Column(db.String(20))  # 微信号  6-20位
    items = db.relationship('Item', backref='user',
                            lazy='dynamic')  # 用户发布的物品

    def __init__(self, openId, avatarUrl='', nickName=''):
        self.openId = openId
        self.avatarUrl = avatarUrl
        self.nickName = nickName

    @staticmethod
    def query_user_by_openId(openId):
        user = User.query.filter_by(openId=openId).first()
        return user

    @staticmethod
    def query_user_by_id(user_id):
        user = User.query.filter_by(id=user_id).first()
        return user

    def update_avatar(self, kwargs):
        try:
            self.avatarUrl = kwargs['avatarUrl']
            self.nickName = kwargs['nickName']
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print('Exception ', e)

        return False

    def update_tel(self, tel):
        try:
            self.phoneNumber = tel
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print('Exception', e)
        return False

    def update_contact(self, kwargs):
        try:
            self.phoneNumber = kwargs['phoneNumber']
            self.qqNumber = kwargs['qqNumber']
            self.weixinNumber = kwargs['weixinNumber']
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print('Exception ', e)

        return False

    def json(self):
        user_id = self.id
        openId = self.openId

        return json.dumps(dict(id=user_id, openId=openId))

    def seri(self):
        return dict(id=self.id,avatarUrl=self.avatarUrl,\
                    nickName=self.nickName,phoneNumber=self.phoneNumber)

    def raw(self):
        return dict(id=self.id, avatarUrl=self.avatarUrl, \
            nickName=self.nickName, phoneNumber=self.phoneNumber, \
            qqNumber=self.qqNumber, weixinNumber=self.weixinNumber)

    def get_contact(self):
        phoneNumber = self.phoneNumber
        qqNumber = self.qqNumber
        weixinNumber = self.weixinNumber

        return json.dumps(dict(phoneNumber=phoneNumber, qqNumber=qqNumber,
                                weixinNumber=weixinNumber))

    def __repr__(self):
        return '{}: {}'.format(self.nickName, self.openId)
