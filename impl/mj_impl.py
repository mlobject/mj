# -*- coding:utf-8 -*-
__author__ = 'huzixu'

# 用户ID，房间ID，游戏第几局
import ujson as json
from utils import read_config
# from utils import common_utils
from database import memsql_manage
from config import mj_param
from mjmanage import mahjong_checker, mj_utils, mj_data

config = read_config.getconfig()
# print config.get("mahjong_impl", "mj")
param_conf = mj_param.impl_param()

# 用户打牌后其他玩家事件判断 doing
# topic=play_mj, payload={"api" : "play_mj", "r_id":"*****", "u_id":"*******", "act":"act 格式:1:1m;2:2m;3:3m;4:5m,6m;6:7p;7:8z,e00122;8:7m,s00211;9:8z;0"}, qos=2,retain=True,hostname="127.0.0.1",port=1883
def play_mj(p) :
    '''
    :param u_id: 出牌人
    :param pai: 牌
    :param r_id: 房间id
    :param act: action(int):pai(str)
    :return:
    '''
    # 事件 0：过；1：接牌(发牌)；2：出牌；3：碰；4：明杠；5：暗杠；6：自摸; 7：接炮；8:点炮; 9:吃; 10：申请终止牌局；11：同意终止牌局
    u_id = p.get("u_id", None)
    r_id = p.get("r_id", None)
    u_act = p.get("act", None)
    # act 格式:1:1m;2:2m;3:3m;4:5m,6m;6:7p;7:8z;8:8m;9:8z;0
    if not u_id or not r_id or not u_act :
        return None
    # 获取游戏当前房间最后一行记录,判断当前指针位置和指针id
    game_data, users_info, pointer_id, pointer_position = mj_utils.play_check(u_id, r_id)
    if not game_data or not pointer_id or not pointer_position or not u_act :
        return None
    game_style = game_data.get("room_style")
    # 校验用户事件以及操作对象是否作弊,并重新封装当前玩家的事件
    result_bol, acts = mj_utils.act_check(pointer_position, game_data, u_act)  # 需要在过一遍 看是否存在问题!!!!!!!!!!!!!!!!!!!!!!!!
    if not result_bol: # 如果非法 则返回空,不推送任何信息
        return None
    result_list = []
    u_act = str(u_act).split(",")
    act_dict = {pointer_position : acts}
    for item in u_act :
        act = str(item).split(":")[0]
        u_pai = str(item).split(":")[1]
        # 出牌事件,封装玩家新事件
        if str(act) == str(2) : # 出牌,需要判断下家,并推送事件
            users_info["%s_mj" % pointer_position] = str(game_data.get("%s_mj") % param_conf.seat_dict[pointer_position]).split(",").remove(u_pai)
            for i in param_conf.seats :
                if i != pointer_position :
                    i_act = mj_utils.get_act(str(game_data.get("%s_mj" % param_conf.seat_dict[i])).split(","), game_style, shou_pai=None, now_pai=u_pai)
                    act_dict = {i : i_act}
                    users_info["%s_act" % i] = i_act
            pointer_new, shoupai, result, now_pai, old_mj, liuju = mj_utils.get_act2_pointer(r_id, u_id, act_dict["e"], act_dict["s"], act_dict["w"], act_dict["n"], pointer_position, game_data.get("east_id"), game_data.get("south_id"), game_data.get("west_id"), game_data.get("north_id"), u_act, game_data)
            # 推送消息
            result_list = result
        # 4：明杠；5：暗杠；#提示房间其他玩家有玩家杠牌,提示杠牌的玩家新牌具备什么事件
        elif str(act) in ["4", "5"] :
            zhuapai, flag = mj_data.get_pai(r_id, game_data.get("g_num"))
            for i in param_conf.seats :
                u_id = game_data.get("%_id" % param_conf.seat_dict[i])
                mes = '''{"api":"play_mj","u_act":"%s","pointer":"0","result":"notice"}''' % (item)
                result_list.append({"topic" : "%s_server" % u_id, "mes" : mes})
            if flag :
                liuju = True  # 流局
            elif act == "4" :
                mg = u_pai
            else :
                ag = u_pai
            shoupai, flag = mj_data.get_pai(r_id, game_data.get("g_num"), flag=False)
            u_mj = str(game_data.get("%s_mj" % param_conf.seat_dict[pointer_position])).split(",").append(u_pai)
            u_mj = u_mj.append(shoupai)
            act = mj_utils.get_act(u_mj, game_style, shou_pai=shoupai)
            shoupai = "%s:%s" % (u_id, shoupai)
            result_list.append({"topic" : "%s_server" % u_id, "mes" : "act:%s,pointer:1" % act})
        elif str(act) == str(3) :
            p_mj = u_pai
            act = mj_utils.get_act("%s_mj" % game_data.get(param_conf.seat_dict[pointer_position]), game_style)
            result_list.append({"topic" : "%s_server" % u_id, "mes" : "act:,pointer:1"})
        elif str(act) in ["6", "7"] :  # 胡牌 结束当前牌局,并判断是否发新牌给玩家
            pass

    # r_id,
    # game_data.get("g_num"),
    # users_info["e_id"],
    # users_info["e_mj"],
    # users_info["e_mg"],
    # users_info["e_ag"],
    # users_info["e_mf"],
    # users_info["e_af"],
    # users_info["e_dg"],
    # users_info["e_p"],
    # users_info["e_act"],
    # users_info["e_doact"],
    # users_info["s_id"],
    # users_info["s_mj"],
    # users_info["s_mg"],
    # users_info["s_ag"],
    # users_info["s_mf"],
    # users_info["s_af"],
    # users_info["s_dg"],
    # users_info["s_p"],
    # users_info["s_act"],
    # users_info["s_doact"],
    # users_info["w_id"],
    # users_info["w_mj"],
    # users_info["w_mg"],
    # users_info["w_ag"],
    # users_info["w_mf"],
    # users_info["w_af"],
    # users_info["w_dg"],
    # users_info["w_p"],
    # users_info["w_act"],
    # users_info["w_doact"],
    # users_info["n_id"],
    # users_info["n_mj"],
    # users_info["n_mg"],
    # users_info["n_ag"],
    # users_info["n_mf"],
    # users_info["n_af"],
    # users_info["n_dg"],
    # users_info["n_p"],
    # users_info["n_act"],
    # users_info["n_doact"],
    # pointer_new,
    # shoupai,
    # old_mj,
    # now_pai,
    # game_data.get("sub_time"),
    # game_data.get("time_consume"),
    # game_data.get("data_type"),
    # game_data.get("room_style")


    # mj_data.game_manage(r_id, game_data.get("g_num"), east_id, game_data.get("east_mj"), game_data.get("east_mg"),
    #             game_data.get("east_ag"), game_data.get("east_p"), east_act, east_doact, south_id,
    #             game_data.get("south_mj"), game_data.get("south_mg"), game_data.get("south_ag"),
    #             game_data.get("south_p"), south_act, south_doact, west_id, game_data.get("west_mj"),
    #             game_data.get("west_mg"), game_data.get("west_ag"), game_data.get("west_p"), west_act, west_dotact,
    #             north_id, game_data.get("north_mj"), game_data.get("north_mg"), game_data.get("north_ag"),
    #             game_data.get("north_p"), north_act, north_doact, pointer_new, shou_pai, game_data.get("old_mj"),
    #             game_data.get("now_mj"), "0", "0", game_data.get("room_style"))


    return result_list


# 发牌 doing 当前牌局属性未做
def start_mj(p) :
    '''
    :param p: json
    :param r_id: 房间id
    :param u_id: 发牌触发人（房主、首局庄家）
    :return: list[map]
    '''
    p = json.loads(p)
    r_id = p.get("r_id", None)
    u_id = p.get("u_id", None)
    style = p.get("style", None)  # 去房间信息里获取

    result_list = []
    if not r_id :
        err_dict = {"topic" : u_id + "_server", "mes" : mj_param.error}
        result_list.append(err_dict)
        return result_list
    # ?是否校验当前触发发牌的为当前房主?--------------------------------------------------------------------------------------------------------------------------------------

    g_num, east_id, west_id, south_id, north_id, room_style = mj_data.room_init(r_id)
    # 1：4局牌，2：8局牌，3：下鱼2条，4：下鱼5条，5：下鱼8条，6：不要风牌，7：自能自摸胡，格式：1,3,7
    style_list = str(room_style).split(",")
    if "6" not in style_list :
        flag = 1  # 要风牌 136张牌
    else :
        flag = 0  # 不要风牌 108张牌

    # 获取牌山,宝牌索引,宝牌,金牌,东南西北四方位牌山
    paishan, bao_index, bao, jin, lie, lin, liw, lis = mj_utils.get_panshan(flag, 1)

    east_mj, paishan = mj_utils.deal_paishan(paishan)
    south_mj, paishan = mj_utils.deal_paishan(paishan)
    west_mj, paishan = mj_utils.deal_paishan(paishan)
    north_mj, paishan = mj_utils.deal_paishan(paishan)
    shou_pai = paishan[0 :1]
    del paishan[0 :1]

    east_act = mj_utils.get_act(east_mj, style_list, shou_pai=shou_pai)
    east_mes = "{api:start_mj,pai:%s,shoupai:%s,act:%s,nowpai:,pointer:1}" % (east_mj, "".join(shou_pai), east_act)
    south_act = mj_utils.get_act(south_mj, style_list)
    south_mes = "{api:start_mj,pai:%s,shoupai:%s,act:%s,pointer:0}" % (south_mj, south_act, "")
    west_act = mj_utils.get_act(west_mj, style_list)
    west_mes = "{api:start_mj,pai:%s,shoupai:%s,act:%s,pointer:0}" % (west_mj, west_act, "")
    north_act = mj_utils.get_act(north_mj, style_list)
    north_mes = "{api:start_mj,pai:%s,shoupai:%s,act:%s,pointer:0}" % (north_mj, north_act, "")

    east_dict = {"topic" : east_id + "_server", "mes" : east_mes}
    west_dict = {"topic" : west_id + "_server", "mes" : west_mes}
    south_dict = {"topic" : south_id + "_server", "mes" : south_mes}
    north_dict = {"topic" : north_id + "_server", "mes" : north_mes}
    result_list.append(east_dict)
    result_list.append(west_dict)
    result_list.append(south_dict)
    result_list.append(north_dict)

    # print east_mj
    # print south_mj
    # print west_mj
    # print north_mj

    raw_hand = ''.join(paishan)
    hand = mahjong_checker.hand_processer(raw_hand, raw_hand=True)
    print ','.join((str(i.get_rank()) + str(i.get_suit()) for i in hand))
    print len(paishan)
    mj_data.game_manage(r_id, g_num, east_id, east_mj, None, None, None, east_act, None, south_id, south_mj, None, None, None, None, None, west_id, west_mj, None, None, None, None, None, north_id, north_mj, None, None, None, None, None, "e:%s" % east_id, shou_pai, None, None, 0, 1)
    return result_list

# print fapai(001, "")
