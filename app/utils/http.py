"""
  Created by kebo on 2018/7/28
"""

import requests
import re
from pyquery import PyQuery as pq
import json
from selenium import webdriver
import time

class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text


lt_pattern = re.compile(r'value="(_c.*?)"')
login_url = 'http://uia.whxy.edu.cn/cas/login'
portal_url = 'http://portal.whxy.edu.cn'
headers = {
	'Content-Type': 'application/x-www-form-urlencoded', 
	'Host': 'uia.whxy.edu.cn', 
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

# brower = webdriver.PhantomJS()
# brower.implicitly_wait(5)

# 获取学生课表信息
def get_course_info(username, password):
	try:
		brower.get(portal_url)
		userele = brower.find_element_by_name('username')
		pwdele = brower.find_element_by_name('password')
		btnele = brower.find_element_by_class_name('login')
		userele.send_keys(username)
		pwdele.send_keys(password)
		btnele.click()
	except Exception as e:
		print(e)
		# print(brower.page_source)
	try:
		aele = brower.find_element_by_css_selector('.module-list-vertical li:nth-child(2) a')
	except Exception as e:
		print(e)
		btnele.click()
		try:
			aele = brower.find_element_by_css_selector('.module-list-vertical li:nth-child(2) a')
		except Exception as e:
			return False
	aele.click()
	if len(brower.window_handles) <= 1:
		return False
	print(brower.window_handles)
	# 进入教务系统
	brower.switch_to_window(brower.window_handles[1])
	handle_login_again()
	# 点击我的课表
	aele = brower.find_element_by_css_selector('.scroll_box li:nth-child(5) a')
	aele.click()
	# 若获取课表失败，则关闭当前tab, 返回继续
	got = has_got_course()
	if not got:
		brower.close()
		brower.switch_to_window(brower.window_handles[0])
		aele = brower.find_element_by_css_selector('.module-list-vertical li:nth-child(2) a')
		aele.click()
		aele = brower.find_element_by_css_selector('.scroll_box li:nth-child(5) a')
		got = has_got_course()
		if not got:
			return False
	else:
		return filter_course()

# 退出登录, 不关闭浏览器以供其他用户查询课表且节省内存开销
def brower_logout():
	aele = brower.find_element_by_css_selector('.ico_exit+a')
	aele.click()
	return 

# 处理出现 "该用户存在重复登录" 的情况
def handle_login_again():
	aele = brower.find_element_by_tag_name('a')
	if aele.text == '点击此处':
		aele.click()
	return

# 过滤课表信息
def filter_course():
	tabele = brower.find_element_by_id('manualArrangeCourseTable')
	tbody = tabele.find_element_by_css_selector('tbody')
	first = tbody.find_element_by_css_selector('tr:nth-child(1)')
	second = tbody.find_element_by_css_selector('tr:nth-child(3)')
	third = tbody.find_element_by_css_selector('tr:nth-child(5)')
	fourth = tbody.find_element_by_css_selector('tr:nth-child(7)')
	
	first_day1 = first.find_element_by_css_selector('td:nth-child(2)').text
	first_day2 = first.find_element_by_css_selector('td:nth-child(3)').text
	first_day3 = first.find_element_by_css_selector('td:nth-child(4)').text
	first_day4 = first.find_element_by_css_selector('td:nth-child(5)').text
	first_day5 = first.find_element_by_css_selector('td:nth-child(6)').text

	second_day1 = second.find_element_by_css_selector('td:nth-child(2)').text
	second_day2 = second.find_element_by_css_selector('td:nth-child(3)').text
	second_day3 = second.find_element_by_css_selector('td:nth-child(4)').text
	second_day4 = second.find_element_by_css_selector('td:nth-child(5)').text
	second_day5 = second.find_element_by_css_selector('td:nth-child(6)').text

	third_day1 = third.find_element_by_css_selector('td:nth-child(2)').text
	third_day2 = third.find_element_by_css_selector('td:nth-child(3)').text
	third_day3 = third.find_element_by_css_selector('td:nth-child(4)').text
	third_day4 = third.find_element_by_css_selector('td:nth-child(5)').text
	third_day5 = third.find_element_by_css_selector('td:nth-child(6)').text

	fourth_day1 = fourth.find_element_by_css_selector('td:nth-child(2)').text
	fourth_day2 = fourth.find_element_by_css_selector('td:nth-child(3)').text
	fourth_day3 = fourth.find_element_by_css_selector('td:nth-child(4)').text
	fourth_day4 = fourth.find_element_by_css_selector('td:nth-child(5)').text
	fourth_day5 = fourth.find_element_by_css_selector('td:nth-child(6)').text

	day1 = [first_day1, second_day1, third_day1, fourth_day1]

	day2 = [first_day2, second_day2, third_day2, fourth_day2]

	day3 = [first_day3, second_day3, third_day3, fourth_day3]

	day4 = [first_day4, second_day4, third_day4, fourth_day4]

	day5 = [first_day5, second_day5, third_day5, fourth_day5]

	res = {
		'day1': day1,
		'day2': day2,
		'day3': day3,
		'day4': day4,
		'day5': day5
	}
	print(brower.window_handles)
	try:
		brower.close()
		brower.switch_to_window(brower.window_handles[0])
		# 退出 
	except Exception as e:
		print(e)
	print(brower.window_handles)
	brower_logout()
	return res


# 判断是否成功获取课表
def has_got_course():
	try:
		tabele = brower.find_element_by_id('manualArrangeCourseTable')
		return tabele
	except Exception as e:
		return False


# 获取个人信息
def get_personal_info(username, password):
	# 登录
	ses = mock_login(username, password)
	print(ses)
	if (isinstance(ses, dict)):
		return ses
	if not ses:
		return False
	# portal 首页
	r = ses.get(portal_url)
	doc = pq(r.text)
	print('enter portal', r.text)
	# 学籍信息直接url
	personal_url = portal_url + doc('#emphases_tab_1')('ul li:nth-child(9)')('a').attr.href
	r = ses.get(personal_url)
	doc = pq(r.text)
	# 学籍信息跳转url
	target_url = json.loads(doc('span#linkurl').text())['url'][0]['url']
	r = ses.get(target_url)
	doc = pq(r.text) 
	# 跳转后可能显示重复登录, 再进入跳转url
	if doc('table'):
		return filter_personal(doc)
	else:
		r = ses.get(target_url)
		doc = pq(r.text)
		return filter_personal(doc) if doc('table') else False


# 过滤学生学籍信息
def filter_personal(doc):
	trs = doc('table tr')
	# print('trs', trs)
	stuid_stuname = pq(trs[1]).text().split('\n')
	# 学号 姓名 专业 班级 系别
	stu_id = stuid_stuname[1]
	stu_name = stuid_stuname[3]
	print('bp 1')
	stu_major = pq(trs[6]).text().split('\n')[1]
	stu_cls = pq(trs[11]).text().split('\n')[2]
	stu_department = pq(trs[5]).text().split('\n')[3]
	print('bp 2')
	return dict(stu_id=stu_id, stu_name=stu_name, stu_major=stu_major, \
				stu_cls=stu_cls, stu_department=stu_department)


# session登录
def mock_login(username, password):
	ses = requests.Session()
	r = ses.get(login_url)
	data = dict(username=username, password=password, _eventId='submit')
	lt = re.search(lt_pattern, r.text).group(1)
	data['lt'] = lt
	pr = ses.post(login_url, data=data, headers=headers)
	print(pr.text)
	doc = pq(pr.text)
	if(doc('.message-btn').attr('value') == '跳过'):
		return handle_login_secure(username, password)
	return ses if '用户登录' not in pq(pr.text)('title').text() else False


def handle_login_secure(username, password):
	try:
		brower.get(portal_url)
		userele = brower.find_element_by_name('username')
		pwdele = brower.find_element_by_name('password')
		btnele = brower.find_element_by_class_name('login')
		userele.send_keys(username)
		pwdele.send_keys(password)
		btnele.click()
	except Exception as e:
		print(e)
	try:
		aele = brower.find_element_by_css_selector('.message-btn')
	except Exception as e:
		print(e)
		btnele.click()
		try:
			aele = brower.find_element_by_css_selector('.message-btn')
		except Exception as e:
			return False
	aele.click()
	doc = pq(brower.page_source)
	# print(brower.page_source)
	personal_url = portal_url + doc('#emphases_tab_1')('ul li:nth-child(9)')('a').attr.href
	print(personal_url)
	brower.get(personal_url)
	doc = pq(brower.page_source)
	print(brower.page_source)
	handle_login_again()
	doc = pq(brower.page_source)
	print(brower.page_source)
	if doc('table'):
		print('yes')
		return filter_personal(doc)
	else:
		return False



# 模拟登录
def request_auth(username, password):
	url = 'http://uia.whxy.edu.cn/cas/login'
	headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'JSESSIONID=7315B7866D151FA81AA418936677F345; Path=/cas; HttpOnly', 'Host': 'uia.whxy.edu.cn', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
	data = dict(username=username, password=password, _eventId='submit')
	res = requests.get(url)
	headers['Cookie'] = res.headers['Set-Cookie']
	lt = re.search(lt_pattern, res.text).group(1)
	data['lt'] = lt
	pr = requests.post(url, data=data, headers=headers)
	return '用户登录' not in pq(pr.text)('title').text()