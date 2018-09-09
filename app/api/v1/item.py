from . import api_v1
from flask import jsonify, request, url_for, Response
import json
from app.utils.res import Res
from app.utils.file import allowed_file, get_fileRoute
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from app.models.item import Item
from app.models.user import User
from app.models import db
import os

def R(r):
    return '/item' + r

@api_v1.route('/item', methods=['GET'])
def get_items():
    try:
        query = Item.query.join(User)
        items = query.order_by(Item.time.desc()).all()
        data = [item.raw() for item in items]
        return jsonify(Res(1, 'get items successfully', data).raw())
    except Exception as e:
        print(e)
    return jsonify(Res(0, 'something error').raw())


@api_v1.route(R('/<int:user_id>'), methods=['GET'])
def get_by_userId(user_id):
    try:
        items = Item.query.filter_by(user_id=user_id).order_by(Item.time.desc()).all()
        data = [item.raw() for item in items]
        print(data)
        return jsonify(Res(1, 'get items successfully', data).raw())
    except Exception as e:
        print(e)
    return jsonify(Res(0, 'something error').raw())


@api_v1.route(R('/<int:item_id>'), methods=['PUT'])
def edit_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify(Res(0, 'item does not exists').raw())
    postData = json.loads(str(request.data, encoding='utf-8'))
    print('edit_item', postData)
    if item.edit(postData):
        return jsonify(Res(1, 'edit item successfully').raw())
    return jsonify(Res(2, 'something error').raw())


@api_v1.route(R('/<int:item_id>'), methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify(Res(0, 'item does not exists').raw())
    if item.delete():
        return jsonify(Res(1, 'delete item successfully').raw())


@api_v1.route(R('/<int:user_id>'), methods=['POST'])
def post(user_id):
    postData = json.loads(str(request.data, encoding='utf-8'))
    print('postData', postData)
    # TODO 数据校验
    # type, itemName, date, place, img, des, user_id
    if Item.createItemByPostData(postData, user_id):
        return jsonify(Res(1, 'post item successfully').raw())
    return jsonify(Res(0, 'something error').raw())



# 上传图片，返回图片地址
@api_v1.route(R('/upload_img'), methods=['POST'])
def upload_img():
    print(request.files)
    if 'img' not in request.files:
        return jsonify(Res(0, '文件名不正确').raw())
    file = request.files['img']
    if file.filename == '':
        return jsonify(Res(0, '请先选择图片').raw())
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            path = get_fileRoute(filename)
            file.save(path)
            print(path)
            ra = path.rsplit('\\',3)
            print('ra', ra)
            r = url_for('static', filename=(ra[-3]+'/'+ra[-2]+'/'+ra[-1]))
            print(r)
            data = dict(imgServerPath=r)
            return jsonify(Res(1,'upload img successfully', data).raw())
        except RequestEntityTooLarge as e:
            return jsonify(Res(0, 'the img is too large').raw())
        except Exception as e:
            print(e)
            return jsonify(Res(0, 'something error').raw())
    else:
        return jsonify(Res(0, 'invalid extension').raw())
