# -*- coding: utf-8 -*-
__author__ = 'huzixu'

import ujson as json
from utils import read_config, common_utils
from database import memsql_manage
from config import mj_param
from mjmanage import mj_data

params = mj_param.impl_param()

config = read_config.getconfig()


# ----------------------------------------------------------------------------------------
def get_room_userinfo(user_list, r_id) :
    result_list = []
    for i in user_list :
        if i.split(":")[1] :
            sql = config.get("user_impl", "user.login.check.u_id") % i.split(":")[1]
            sql_result = memsql_manage.execute_sql(sql)
            user_info = sql_result[0]
            mes = '''{"api":"enter_room","u_id":"%s","wx_nickname":"%s","wx_sex":"%s","wx_country":"%s","wx_headimgurl":"%s","speed_type":"%s","escape_num":"%s","break_num":"%s","result":"%s"}''' % (user_info.get("u_id"), user_info.get("wx_nickname"), user_info.get("wx_sex"), user_info.get("wx_country"), user_info.get("wx_headimgurl"), user_info.get("speed_type"), user_info.get("escape_num"), user_info.get("break_num"), params.enter_room)
            result_list.append({"topic" : r_id + "_server", "mes" : mes})
    return result_list


def signout(east_id, u_id, r_id) :
    # result = param.signout_room
    result = 'signout_room'
    if east_id :
        # result = param.kick_user
        result = "kick"
    sql = config.get("user_impl", "user.login.check.u_id") % u_id
    sql_result = memsql_manage.execute_sql(sql)
    if len(sql_result) == 0 :
        return None

    user_info = sql_result[0]
    sql = config.get("user_impl", "get.room.info") % r_id
    sql_result = memsql_manage.execute_sql(sql)
    if len(sql_result) == 0 :
        return None
    room_info = sql_result[0]
    if east_id and east_id != room_info.get("east_id") :
        return None

    user_list = room_info.get("user_list").split(",")
    u_list = []
    if u_id in str(room_info.get("user_list")) :
        for i in user_list :
            if i.split(":")[1] and i.split(":")[1] == u_id :
                position = i.split(":")[0]
                user_list.remove(i)
                user_list.append("%s:" % i.split(":")[0])
                u_list.append("%s:" % (i.split(":")[0]))
            else :
                u_list.append(i)
    print u_list
    print ",".join(u_list)
    sql = "UPDATE mj.room_info SET %s WHERE r_id = '%s'" % ("user_list = '%s'" % ",".join(u_list), r_id)
    memsql_manage.execute_sql(sql, action="up")
    # print u_id, position, param.signout_room
    mes = '''{"api":"signout","u_id":"%s","position":"%s","result":"%s"}''' % (u_id, position, result)
    result_list = []
    result_list.append({"topic" : "%s_server" % r_id, "mes" : mes})
    return result_list


# ----------------------------------------------------------------------------------------


# topic=uid_server, payload={"api":"login", u_id:"9c80f3", wx_openid:"ddf30182", "wx_nickname":"麻将玩家A", "wx_sex":"1", "wx_country"="CN", "wx_headimgurl":"http://asdfasfe"},qos=2,retain=True,hostname="127.0.0.1",port=1883
# user login or register玩家登录或注册 待测 ing
def login(p) :
    # print "ssssssss:" + p
    u_id_client = p.get('u_id', None)
    wx_openid = p.get('wx_openid', None)
    card_num = "3"
    user_info = mj_data.get_userinfo(u_id=u_id_client, u_openid=wx_openid)

    if user_info :
        u_id = user_info.get("u_id")
        card_num = user_info.get("card_num")
    else :
        u_id = common_utils.get_uid()
        sql = config.get('user_impl', 'user.login.register') % (u_id, wx_openid, p.get("wx_nickname", None), p.get("wx_sex", None), p.get("wx_country", None), p.get("wx_headimgurl", None))
        memsql_manage.execute_sql(sql, action="up")
    mes = '''{"api":"login","u_id":"%s","card_num":"%s","result":"succ"}''' % (u_id, card_num)
    if not u_id_client:
        u_id_client = wx_openid
    result = [{"topic" : u_id_client + "_server", "mes" : mes}]
    return result


# 创建房间
# # topic=create_room, payload={"api": "create_room", "u_id":"", "room_style":[1,2,4]}, qos=2,retain=True,hostname="127.0.0.1",port=1883
def create_room(p) :
    result_list = []
    east_id = p.get("u_id", None)
    room_style = p.get("room_style", None)
    # room_style = ','.join([str(i) for i in room_style])
    if not east_id or not room_style :
        return None
    user_info = mj_data.get_userinfo(u_id=east_id)
    if not user_info :
        return None
    card_num = user_info.get("card_num")
    if int(card_num) == 0 :
        return [{"topic" : east_id, "mes" : ""'''{"api":"create_room","r_id":"","result":"err"}'''}]
    r_id = mj_data.get_roomid(east_id)
    mes = '''{"api":"create_room","%s":"%s","%s":"%s"}''' % ("r_id", r_id, "result", "succ")
    result = {"topic" : east_id + "_server", "mes" : mes}
    result_list.append(result)
    return result_list


# 进入房间验证 over
# {"enter_room" : "enter_room", "user_id":"*****", "r_id":"*******"}
# topic=enter_room, payload={"api": "enter_room", "u_id":"*****", "r_id":"*******"}, qos=2,retain=True,hostname="127.0.0.1",port=1883
def enter_room(p) :
    '''
    开放规则：
    # 1.房间预留一个座位给房主（花钱买房卡的人）；
    # 2.房主有踢人权利，同一个玩家被踢三次则永久不能进入该房间（后台控制）；
    # 3.房间坐满人后，首局需要房主点发牌；
    # 4.首局开始后则该房间状态标记为已使用；
    # 5.该房间玩家确认后，其他玩家不得加入，中途退出、解散、掉线不返回牌桌等异常行为视为房间所有牌局结束并计算总结果。
    1.east_id 预留房主使用
    2.每进入一个玩家 房间接发送一个信息 : 所做位置;当前进入房间的玩家接收其他玩家所坐的位置
    :param user_id:
    :param r_id:
    :return:
    1.判断是否黑名单
    2.判断房间是否人满
    4.进入房间,发送消息
    '''
    result_list = []
    # p = json.loads(p)
    u_id = p.get("u_id")
    r_id = p.get("r_id")
    if not u_id or not r_id :
        # return {"topic": user_id + "_server", "mes": param.error}
        return [{"topic" : "%s_server" % u_id, "mes" : "err"}]
    user_info = mj_data.get_userinfo(u_id=u_id)
    if not user_info :
        return None
    room_info = mj_data.get_roominfo(r_id)  # 获取房间信息
    if not room_info :
        return None
    # 当前用户是否在房间黑名单里
    print type(room_info.get("black_users"))
    print room_info.get("black_users")
    if room_info.get("black_users") and u_id in room_info.get("black_users") :
        mes = '''{"api":"%s","result":"%s"}''' % ("enter_room", "err")
        return [{"topic" : u_id + "_server", "mes" : mes}]

    # 当前用户已在房间,可能掉线,重进房间
    if u_id in room_info.get("user_list") :
        user_info = mj_data.get_userinfo(u_id=u_id)
        mes = '''{"api":"enter_room","u_id":"%s","wx_nickname":"%s","wx_sex":"%s","wx_country":"%s","wx_headimgurl":"%s","speed_type":"%s","escape_num":"%s","break_num":"%s","result":"%s"}''' % (u_id, user_info.get("wx_nickname"), user_info.get("wx_sex"), user_info.get("wx_country"), user_info.get("wx_headimgurl"), user_info.get("speed_type"), user_info.get("escape_num"), user_info.get("break_num"), params.succ)
        result_list.append({"topic" : r_id + "_server", "mes" : mes})
        return result_list
    users_id = []
    # 判断当前房间人数是否够4人
    room_users = room_info.get("user_list").split(",")
    f = 0
    for i in room_users :
        if i.split(":")[1] :
            f = f + 1
            users_id.append("%s:%s" % (i.split(":")[0], i.split(":")[1]))
    if f == 4 :  # 房间人满
        return [{"topic" : u_id + "_server", "mes" : '''{"api":"enter_room","result":"%s"}''' % "room_full"}]
    user_list = room_info.get("user_list").split(",")
    # 进入房间流程
    flag = False
    for i in user_list :
        if not i.split(":")[1] :
            user_list.remove(i)
            user_list.append("%s:%s" % (i.split(":")[0], u_id))
            users_id.append("%s:%s" % (i.split(":")[0], u_id))
            flag = True
        if flag :
            break
    sql = "UPDATE mj.room_info SET user_list = '%s' WHERE r_id = '%s'" % (",".join(user_list), r_id)
    memsql_manage.execute_sql(sql, action="up")
    users_info = []
    for user in users_id :
        user_info = mj_data.get_userinfo(u_id=user.split(":")[1])
        print user.split(":")[0][0]
        print "u_id",user_info.get("u_id")
        print "wx_nickname" , user_info.get("wx_nickname")
        print "wx_sex" , user_info.get("wx_sex")
        print "wx_country" , user_info.get("wx_country")
        print "wx_headimgurl" , user_info.get("wx_headimgurl")
        print "speed_type" , user_info.get("speed_type")
        print "escape_num" , user_info.get("escape_num")
        print "break_num" , user_info.get("break_num")
        users_info.append({"pointer" : user.split(":")[0][0], "u_id" : user_info.get("u_id"), "wx_nickname" : user_info.get("wx_nickname"), "wx_sex" : user_info.get("wx_sex"), "wx_country" : user_info.get("wx_country"), "wx_headimgurl" : user_info.get("wx_headimgurl"), "speed_type" : user_info.get("speed_type"), "escape_num" : user_info.get("escape_num"), "break_num" : user_info.get("break_num")})
    users_json = json.dumps(users_info)
    mes = '''{"api":"enter_room","users":%s,"result":"notic"}''' % str(users_json)
    result_list.append({"topic" : r_id + "_server", "mes" : mes})
    return result_list


# 退出房间
def signout_room(p) :
    # p = json.loads(p)
    u_id = p.get("u_id", None)
    r_id = p.get("r_id", None)
    result_list = signout('', u_id, r_id)
    return result_list


# print login('''{"api":"login","u_id":"001"}''')
# print create_room('''{"api":"create_room","u_id":"742810","room_style":"1,2,4"}''')
# print enter_room('''{"u_id":"5232ef","r_id":"17529834"}''')
# print signout_room('''{"api":"signout","u_id":"5232ef","r_id":"17529834"}''')



# 房主踢人 over
# topic=kick_user, payload={"api" : "kick_user", "east_id":"*****", "ku_id":"*******", "r_id":"*******"}, qos=2,retain=True,hostname="127.0.0.1",port=1883
def kick_user(p) :
    '''
    判断是否为房主，判断游戏是否开始，结果是否可以踢人
    备注：玩家被踢三次则不可以进入房间
    :param p:
    :return: 是否踢出 0：房间游戏进行中，不可以踢人；1：踢人成功
    '''
    p = json.loads(p)
    east_id = p.get("u_id")
    u_id = p.get("ku_id")
    r_id = p.get("r_id")
    if not east_id or not u_id or not r_id :
        return None
    result_list = signout(east_id, u_id, r_id)
    return result_list


# 申请终止游戏 over
# topic=stop_game, payload={"api" : "stop_game", "r_id":"*****", "u_id":"*******", act:"10：申请终止牌局；11：同意终止牌局；12：不同意终止牌局"}, qos=2,retain=True,hostname="127.0.0.1",port=1883
def stop_game(p) :
    '''
    :param r_id:
    :param u_id:
    :return:
    '''
    # p = json.loads(p)
    r_id = p.get("r_id", None)
    u_id = p.get("u_id", None)
    u_act = p.get("u_act", None)
    topic = r_id + "_server"
    if not r_id and not u_id and not u_act :
        sql = config.get('user_impl', "room.user.fix.pointer") % r_id
        sql_result = memsql_manage.execute_sql(sql)
        obj = sql_result[0]
        east_id = obj.get("east_id")
        south_id = obj.get("south_id")
        west_id = obj.get("west_id")
        north_id = obj.get("north_id")
        g_num = obj.get("g_num")
        if east_id == u_id :
            sql = config.get('user_impl', "room.act.update") % (r_id, u_act, 'south_act', 'west_act', 'north_act', r_id, "east_id = 's%' " % u_id)
        elif south_id == u_id :
            sql = config.get('user_impl', "room.act.update") % (r_id, 'east_act', u_act, 'west_act', 'north_act', r_id, "south_id = 's%' " % u_id)
        elif west_id == u_id :
            sql = config.get('user_impl', "room.act.update") % (r_id, 'east_act', 'south_act', u_act, 'north_act', r_id, "west_id = 's%' " % u_id)
        elif north_id == u_id :
            sql = config.get('user_impl', "room.act.update") % (r_id, 'east_act', 'south_act', 'west_act', u_act, r_id, "north_id = 's%' " % u_id)
        else :
            sql = ""
        if len(sql) < 2 :
            # mes = param.error
            mes = "err"
        else :
            memsql_manage.execute_sql(sql, action='up')
            mes = "u_id:%s,u_act:%s,r_id:%s" % (u_id, u_act, r_id)
        result = {"topic" : topic + "_server", "mes" : mes}
    return result


# 用户离线上线
def user_offoron_line(r_id, u_id) :
    # user.onoff.line =   UPDATE mj.user_info SET offon_line = '%s' WHERE u_id = '%s';
    sql = config.get('user_impl', "user.onoff.line") % (0, u_id)
    memsql_manage.execute_sql(sql, action="up")
    return
