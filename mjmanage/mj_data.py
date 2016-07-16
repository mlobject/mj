# -*- coding:utf-8 -*-
__author__ = 'huzixu'
from utils import read_config
# from utils import common_utils
from database import memsql_manage
from utils import common_utils
from config import mj_param
# from mjmanage import mahjong_checker,mj_utils

config = read_config.getconfig()
# print config.get("mahjong_impl", "mj")
params = mj_param.impl_param()


def get_roominfo(r_id) :
    sql = config.get('user_impl', "get.room.info") % (r_id)  # 房间信息
    sql_result = memsql_manage.execute_sql(sql)
    if len(sql_result) == 0 :
        return None
    else :
        return sql_result[0]


def get_roomid(u_id) :
    r_id = common_utils.get_r_id()
    sql = config.get("user_impl", "room.use.do")
    memsql_manage.execute_sql(sql, action="up")
    sql = config.get('user_impl', 'room.generate') % (r_id, u_id, u_id)
    memsql_manage.execute_sql(sql, action="up")
    return r_id


# 获取用户信息
def get_userinfo(u_id='', u_openid='') :
    if not u_id and not u_openid :
        return None
    if u_openid :
        sql = config.get('user_impl', 'user.login.check.opne_id') % (u_openid)
    elif u_id :
        sql = config.get('user_impl', 'user.login.check.u_id') % (u_id)
    sql_result = memsql_manage.execute_sql(sql)
    if len(sql_result) > 0 :
        return sql_result[0]
    else :
        return None


def get_game_info(r_id) :
    # sql = SELECT * FROM mj.game_info WHERE r_id = '%s' ORDER BY sub_time desc limit 1;
    sql = config.get("mj_impl", "mj.get.game.info") % r_id
    sql_result = memsql_manage.execute_sql(sql)
    return sql_result


def get_room_users(r_id) :
    # sql = SELECT * FROM mj.game_info WHERE r_id = '%s' ORDER BY sub_time desc limit 1;
    sql = config.get("mj_impl", "mj.get.room.users") % r_id
    sql_result = memsql_manage.execute_sql(sql)
    return sql_result


def game_manage(r_id, g_num, east_id, east_mj, east_mg, east_ag, east_p, east_act, east_doact, south_id, south_mj, south_mg, south_ag, south_p, south_act, south_doact, west_id, west_mj, west_mg, west_ag, west_p, west_act, west_dotact, north_id, north_mj, north_mg, north_ag, north_p, north_act, north_doact, pointer, shou_pai, old_mj, now_mj, time_consume, data_typ, room_style) :
    # sql = INSERT INTO mj.game_info (gi_id,r_id, g_num, east_id, east_mj, east_mg, east_ag, east_p, east_act, east_doact, south_id, south_mj, south_mg, south_ag, south_p, south_act, south_doact, west_id, west_mj, west_mg, west_ag, west_p, west_act, west_dotact, north_id, north_mj, north_mg, north_ag, north_p, north_act, north_doact, pointer, shou_pai, old_mj, now_mj, time_consume, data_typ) VALUES (uuid(),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
    sql = config.get("mj_impl", "mj.game.info.ing") % (r_id, g_num, east_id, east_mj, east_mg, east_ag, east_p, east_act, east_doact, south_id, south_mj, south_mg, south_ag, south_p, south_act, south_doact, west_id, west_mj, west_mg, west_ag, west_p, west_act, west_dotact, north_id, north_mj, north_mg, north_ag, north_p, north_act, north_doact, pointer, shou_pai, old_mj, now_mj, time_consume, data_typ, room_style)
    memsql_manage.execute_sql(sql, action="up")


# CREATE TABLE room_mj_info(
#   mj_id VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '', -- primary
#   r_id varchar(25) NOT NULL, -- 房间id
#   paishan varchar(800) NOT NULL, -- 房间id
#   g_num int(2) NOT NULL , -- 牌局
#   ga_num int(10) DEFAULT 0 , -- 当前牌局杠次数
#   sub_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 时间戳
#
#   PRIMARY (mj_id)
# )

# 玩家抓牌
def get_pai(r_id, g_num, flag=True) :
    '''
    :param r_id: 房间id
    :param g_num: 游戏局数
    :param gang: 是否为杠抓牌,默认不是杠
    :param flag: 是否需要入库记录抓牌事件,默认为True
    :return:
    '''
    flag = False  # 标示是不是宝牌
    sql = config.get("mj_impl", "mj.game.paishan") % (r_id, g_num)
    sql_result = memsql_manage.execute_sql(sql)

    if not sql_result :
        return None
    mj_data = sql_result[0]
    paishan = str(mj_data.get("paishan")).split(",")
    # ga_num = int(mj_data.get("ga_num"))
    # shengpai = params.paishan_shengyu
    # if gang :
    #     ga_num = ga_num + 1
    # if len(paishan) == shengpai + ga_num :
    #     return "0"
    shou_pai = paishan[-1 :]
    if flag :
        del paishan[-1 :]
        sql = config.get("mj_impl", "mj.game.paishan.up")
        memsql_manage.execute_sql(sql, action="up")

    return shou_pai, flag
