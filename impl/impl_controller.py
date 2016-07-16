# -*- coding:utf-8 -*-
__author__ = 'huzixu'
import os
import user_impl
# from config import param

# os.environ['PYTHON_EGG_CACHE'] = '/tmp'
import ujson as json
import user_impl
import mj_impl


def impl_controller(r_id, params):
    if not params:
        return None
    print params

    json_params = json.loads(params)
    # json_params = eval(params)
    api = json_params.get("api")
    # 麻将业务逻辑
    # if hasattr(mj_impl, api):
    #     result = getattr(mj_impl, api)(json_params)
    # 用户业务逻辑

    if hasattr(user_impl, api):
        result = getattr(user_impl, api)(json_params)
    # 非法调用
    else:
        result = "err"
    return result
