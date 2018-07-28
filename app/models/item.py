"""
  Created by kebo on 2018/7/28
"""

from . import db

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.SmallInteger)   # 物品类型
    itemName = db.Column(db.String(20)) # 物品名称
    date = db.Column(db.Date)           # 时间
    place = db.Column(db.String(30))    # 地点
    img = db.Column(db.String(200))     # 图片
    des = db.Column(db.String(200))     # 描述
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, type, itemName, date, place, img, des, user_id):
        self.type = type
        self.itemName = itemName
        self.date = date
        self.place = place
        self.img = img
        self.des = des
        self.user_id = user_id

    def __repr__(self):
        return '{}: {}'.format(self.itemName, self.type)