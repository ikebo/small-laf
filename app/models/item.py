"""
  Created by kebo on 2018/7/28
"""

from . import db
import datetime

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
            kwargs = kwargs['postData']
            date_str = kwargs['date']
            kwargs['date'] = datetime.date(*map(int, date_str.split('-')))
            item = Item(kwargs['itemType'], kwargs['itemName'],\
                kwargs['date'], kwargs['place'], \
                kwargs['img'], kwargs['des'], user_id)
            db.session.add(item)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def raw(self):
        return dict(id=self.id,itemType=self.type, itemName=self.itemName, \
            date=self.date.strftime('%Y-%m-%d'), place=self.place, img='http://127.0.0.1:3000' + \
            self.img, des=self.des, user_id=self.user_id)

    def __repr__(self):
        return '{}: {}'.format(self.itemName, self.type)