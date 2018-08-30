"""
  Created by kebo on 2018/8/9
"""

from . import admin
from flask import session, redirect, url_for, render_template


@admin.route('/')
def index():
    if not session.get('admin', None):
        return redirect(url_for('.login'))
    return render_template('admin/index.html')


@admin.route('/itemControl')
def item_control():
    return render_template('admin/itemControl.html')


@admin.route('/userControl')
def user_control():
    return render_template('admin/userControl.html')


@admin.route('/commentControl')
def comment_control():
    return render_template('admin/commentControl.html')


@admin.route('/login')
def login():
    return render_template('admin/login.html')
