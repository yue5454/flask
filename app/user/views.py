#coding: utf8
from app.user import user
from app.models import mySqlDB

from flask import jsonify, request
import json
from collections import namedtuple, OrderedDict
import datetime

select_user_by_name_sql = '''
SELECT * FROM lily_user WHERE user_name='{name}'
'''

select_user_by_id_sql = '''
SELECT * FROM lily_user WHERE user_id='{id}'
'''

select_all_user_sql = '''
SELECT * FROM lily_user
'''

delete_user_by_id_sql = '''
DELETE  FROM lily_user WHERE user_id='{id}'
'''

update_user_by_id_sql = '''
UPDATE lily_user SET 
user_name='{name}', user_password='{password}', user_phone='{phone}', user_email='{email}', role_id='{type}', update_time='{updateTime}'
WHERE user_id = '{id}'
'''

insert_user_sql = '''
INSERT lily_user 
(user_name, user_password, user_phone, user_email, role_id, create_time, update_time) 
VALUES 
('{name}', '{password}', '{phone}', '{email}', '{type}', '{createTime}', '{updateTime}')
'''

User = namedtuple('User', ['user_id', 'user_name', 'user_password', 'user_phone', 'user_email', 'role_id', 'create_time', 'update_time'])


@user.route('/create', methods=['post'])
def create_user():
    data = json.loads(request.data)
    data['createTime'] = data['updateTime'] = datetime.datetime.now()
    insert_user_sql_command = insert_user_sql.format(**data)
    select_user_by_name_sql_command = select_user_by_name_sql.format(name=data['name'])
    try:
        cursor = mySqlDB.select_command(select_user_by_name_sql_command)
        result = cursor.fetchone()

        if result:
            return jsonify(status='error', msg='User already exits')
        else:
            mySqlDB.general_command(insert_user_sql_command)
            return jsonify(status='success', msg='Create user successfully')
    except Exception as e:
        mySqlDB.rollback()
        return jsonify(status='error', msg='Error when try to create user')
        raise e
    finally:
        mySqlDB.close()


@user.route('/update', methods=['put'])
def update_user():
    data = json.loads(request.data)
    data['updateTime'] = datetime.datetime.now()
    update_user_by_id_sql_command = update_user_by_id_sql.format(**data)
    select_user_by_id_sql_command = select_user_by_id_sql.format(id=data['id'])
    try:
        cursor = mySqlDB.select_command(select_user_by_id_sql_command)
        result = cursor.fetchone()

        if result:
            print update_user_by_id_sql_command
            mySqlDB.general_command(update_user_by_id_sql_command)
            return jsonify(status='success', msg='Update user successfully')
        else:
            return jsonify(status='error', msg="User doesn't exit")
    except Exception as e:
        mySqlDB.rollback()
        return jsonify(status='error', msg='Error when try to update user')
        raise e
    finally:
        mySqlDB.close()


@user.route('/delete/<int:id>', methods=['delete'])  
def delete_user(id):
    delete_user_by_id_sql_command = delete_user_by_id_sql.format(id=id)
    select_user_by_id_sql_command = select_user_by_id_sql.format(id=id)
    try:
        cursor = mySqlDB.select_command(select_user_by_id_sql_command)
        tar = cursor.fetchall()

        if len(tar) == 0:
            return jsonify(status='error', msg="User doesn't exit")
        else:
            mySqlDB.general_command(delete_user_by_id_sql_command)
            return jsonify(status='success', msg='Success to delete user')
    except Exception as e:
        mySqlDB.rollback()
        return jsonify(status='error', msg='Error when try to delete user')
    finally:
        mySqlDB.close()


@user.route('/users', methods=['GET'])
def get_users():
    try:
        cursor = mySqlDB.select_command(select_all_user_sql)
        res = cursor.fetchall()
        result = OrderedDict()
        result['limit'] = 0
        result['offset'] = 10
        result['results'] = []
        result['total'] = 10
        for item in res:
            user = User._make(item)

            _item = OrderedDict()
            _item['id'] = user.user_id
            _item['name'] = user.user_name
            _item['email'] = user.user_email
            _item['phone'] = user.user_phone
            _item['password'] = user.user_password

            if user.create_time:
                _item['createTime'] = user.create_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                _item['createTime'] = ''

            if user.update_time:
                _item['updateTime'] = user.update_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                _item['updateTime'] = ''
            
            result['results'].append(_item)

        return json.dumps(result, ensure_ascii=False, indent=1) 
    except Exception as e:
        raise e
        return jsonify(status='error', msg='Error when get users')

    
    
