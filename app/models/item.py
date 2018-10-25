"""
  Created by kebo on 2018/7/28
"""

from . import db
import datetime
from app import app

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.SmallInteger)   # 物品类型
    itemName = db.Column(db.String(20)) # 物品名称
    date = db.Column(db.Date)           # 丢失或捡到时间
    time = db.Column(db.DateTime)       # 发布时间
    place = db.Column(db.String(30))    # 地点
    srcs = db.Column(db.String(300))    # 图片
    des = db.Column(db.String(200))     # 描述
    viewNum = db.Column(db.Integer)     # 查看次数
    goodNum = db.Column(db.Integer)     # 点赞次数
    commentNum = db.Column(db.Integer)  # 评论次数
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 物品所属用户
    comments = db.relationship('Comment', backref='item',
                               lazy='dynamic')  # 物品评论

    def __init__(self, type, srcs, des, place, user_id):
        self.type = type
        self.des = des
        self.srcs = srcs
        self.place = place
        self.user_id = user_id

        self.time = datetime.datetime.now()
        self.viewNum = 0
        self.goodNum = 0
        self.commentNum = 0


    def edit(self, kwargs):
        try:
            kwargs = kwargs['postData']
            self.type = kwargs['itemType']
            self.itemName = kwargs['itemName']
            date_str = kwargs['date']
            kwargs['date'] = datetime.date(*map(int, date_str.split('-')))
            self.date = kwargs['date']
            self.place = kwargs['place']
            self.img = kwargs['img']
            print('img: ', self.img)
            self.des = kwargs['des']
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def createItemByPostData(kwargs, user_id):
        try:
            print(kwargs)
            item = Item(type=kwargs['type'], des=kwargs['des'],\
                srcs=kwargs['srcs'], place=kwargs['place'], user_id=user_id)
            db.session.add(item)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def raw(self):
        if not self.time:
            self.time = datetime.datetime.now()
        return dict(id=self.id,type=self.type,des=self.des,\
                srcs=self.srcs, place=self.place, user_id=self.user_id, \
                time=self.time.strftime('%m-%d-%H-%M-%S'),user=self.user.seri())

    def __repr__(self):
        return '{}: {}'.format(self.itemName, self.type)
