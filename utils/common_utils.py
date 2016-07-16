# -*- coding: utf-8 -*-
__author__ = 'huzixu'


import os
import random, string
from utils import read_config
from database import memsql_manage


config = read_config.getconfig()

# 生成唯一的uid
def get_uid():
    u_id = ""
    while True:
        u_id = generate_uid()
        # sql = read_config.getconfig("user_impl").get("user.login.u_id") % u_id
        sql = config.get('user_impl',"user.login.u_id") % u_id
        sql_result = memsql_manage.execute_sql(sql)
        if not sql_result:
            break
    return u_id


def generate_uid():
    return ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(5)))[0:6]


# 生成房间号
def get_r_id():
    r_id = ""
    while True:
        r_id = generate_rid()

        sql = config.get("user_impl","room.id.check") % (r_id)
        print "%s,%s"% ("sssss:",sql)
        sql_result = memsql_manage.execute_sql(sql)
        if not sql_result:
            break
    return r_id


def generate_rid():
    return ''.join(random.sample(string.digits, 6))


print generate_uid()