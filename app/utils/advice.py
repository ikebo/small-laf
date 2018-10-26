# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/21
import datetime
import os
from app import app


# 将建议格式化
def format_advice(user_id, advice):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    res = user_id + '  ' + time + '\n' + advice + '\n\n'
    return res


# 添加获取建议文件的路径
def get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


# 获得建议文件的存储路径
def get_advice_route():
    # folder = os.path.join(app.config['ADVICE_PATH'], get_current_date())
    folder = app.config['ADVICE_PATH']
    if not os.path.exists(folder):
        os.mkdir(folder)
    advice_route = folder + os.path.sep + get_current_date()

    return advice_route


# 获得昨天存储的advice内容
def get_yesterday_advice():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    # tomorrow = today + datetime.timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    folder = app.config['ADVICE_PATH']
    advice_router = folder + os.path.sep + yesterday
    with open(advice_router, "rb") as f:
        content = f.read()
    return content

