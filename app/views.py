#coding:utf-8
from flask import jsonify
from flask import request
from flask import render_template
import json

from app import app
from models import mySqlDB

user_login_sql = '''
SELECT * FROM lily_user WHERE user_name='{username}' AND user_password='{password}'
'''


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/login", methods=['post'])
def login():
  data = json.loads(request.data)
  user_login_sql_command = user_login_sql.format(**data)

  try:
    cursor = mySqlDB.select_command(user_login_sql_command)
    result = cursor.fetchone()
    if result:
      return jsonify(status='success', msg='Login successfully')
    else:
      return jsonify(status='error', msg='username or password is not correct, please check')
  except Exception as e:
    return jsonify(status='error', msg="username doesn't exit")
    raise e
