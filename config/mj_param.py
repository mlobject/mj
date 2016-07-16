# -*- coding: utf-8 -*-
__author__ = 'huzixu'

class impl_param(object):
    # error
    error = "error"
    succ = "succ"
    # 登录注册
    login = "login"
    # 房间踢人
    kick_user = "kick"
    # 房间终止游戏
    break_play = "break_play"
    # 进入房间
    enter_room = "enter_room"

    signout_room = "signout"
    # 房间人满
    room_full = "full"
    # 用户状态
    user_offline = "offline"  # 离线
    user_online = "online"  # 在线
    # user
    # 黑名单标示
    black_user = "black_user"
    # 登录成功
    login_success = "login_success"
    # 注册成功
    register_success = "register_success"

    # 发牌打牌顺序
    seats = ["e", "n", "w", "s"]

    eseats = ["e", "n", "w", "s"]

    sseats = ["s", "w", "s", "e"]

    wseats = ["w", "n", "e", "s"]

    nseats = ["n", "e", "s", "w"]

    eseats0 = ["n", "w", "s", "e"]

    sseats0 = ["e", "n", "w", "s"]

    wseats0 = ["s", "e", "n", "w"]

    nseats0 = ["w", "s", "e", "n"]

    seat_dict = {"e": "east", "n": "north", "w": "west", "s": "south"}
    seat_dict_ = {"east": "e", "north": "n", "west": "w", "south": "s"}
    # mj
    mj = "mj"
    kf = "kf"

    # mqtt
    mes = "mes"
    topic = "topic"

    # database
    up = "up"

    # 牌山剩余数
    paishan_shengyu = 12

    # mj
    # 事件 0：无动作；1：接牌；2：出牌；3：碰；4：明杠；5：暗杠；6：胡
    null_act = 0
    jp_act = 1
    cp_act = 2
    p_act = 3
    mg_act = 4
    ag_act = 5
    h_act = 6

    # dic_random = {1 : ["1", "4", "3", "2"], 2 : ["2", "1", "4", "3"], 3 : ["3", "2", "1", "4"], 4 : ["4", "3", "2", "1"]}
    # key 代表以东为起点 上次的赢家是谁
    dic_random = {1 : ["1", "4", "3", "2"], 2 : ["4", "3", "2", "1"], 3 : ["3", "2", "1", "4"], 4 : ["2", "1", "4", "3"]}
