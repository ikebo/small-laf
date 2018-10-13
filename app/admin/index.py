"""
  Created by kebo on 2018/8/9
"""
from app.utils.decorators import login_required
from . import admin
from flask import  render_template


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/itemControl')
@login_required
def item_control():
    return render_template('admin/itemControl.html')


@admin.route('/userControl')
@login_required
def user_control():
    return render_template('admin/userControl.html')


@admin.route('/commentControl')
@login_required
def comment_control():
    return render_template('admin/commentControl.html')


@admin.route('/login')
def login():
    return render_template('admin/login.html')
