# -*- coding:utf-8 -*-
__author__ = 'huzixu'
# from utils import read_config
# from utils import common_utils
from config import mj_param
from mjmanage import mahjong_checker
from mjmanage import mj_data
import random
import random

params = mj_param.impl_param()

# 判断牌桌上的牌是否能碰 doing
def mj_peng(mj) :
    '''
    比对玩家打出的牌是否有碰
    :param mj:
    :return:
    '''
    peng_pai = mj_p_g(mj, 3)
    return peng_pai


# 判断手上的牌是否能杠（暗杠）over
def mj_angang(mj) :
    '''
    当前手牌是否有暗杠的机会
    :param mj:
    :return:
    '''
    angang_pai = mj_p_g(mj, 4)
    return angang_pai


# 判断牌桌上的牌是否能杠（明杠）over
def mj_mgang(mj) :
    '''
    比对其他玩家打出的拍 是否有杠
    :param mj:
    :param now_mj:
    :return:
    '''
    mgang_pai = mj_p_g(mj, 4)
    return mgang_pai


# 判断杠牌
def mj_p_g(mj, num) :
    gang_pai = []
    myset = set(mj)
    for item in myset :
        if mj.count(item) == int(num) :
            gang_pai.append(item)
    return ",".join(gang_pai)


# 自摸胡
def mj_hu6(mj) :
    '''
    :param mj:
    :return:
    '''
    result = False
    return result


# 吃胡（点炮）
def mj_hu7(mj) :
    '''
    :param mj:
    :return:
    '''


# 首局房间初始化，用户存储到mj.game_info表中 over
def room_init(r_id) :
    '''
    :param r_id:房间id
    :return:
    '''
    g_num = ''
    east_id = ''
    west_id = ''
    south_id = ''
    north_id = ''
    room_style = ''
    game_info = mj_data.get_game_info(r_id)
    if not game_info :  # 房间为进行过游戏
        # sql_result = memsql_manage.execute_sql(config.get("mj_impl", "mj.get.room.users") % r_id)
        room_users = mj_data.get_room_users(r_id)
        if not room_users :
            return g_num, east_id, west_id, south_id, north_id, room_style
        else :
            data = room_users[0]
            g_num = 1
            east_id = data.get("east_id")
            south_id = data.get("south_id")
            west_id = data.get("west_id")
            north_id = data.get("north_id")
            room_style = data.get("room_style")
        return g_num, east_id, west_id, south_id, north_id, room_style
    else :  # 房间进行过游戏
        # 0：无动作(过)；1：抓牌；2：出牌；3：碰；4：明杠；5：暗杠；6：胡; 7：接炮；8：点炮；9：申请终止牌局；10：同意终止牌局；11：不同意终止牌局；12：过
        data = game_info[0]
        g_num = data.get("g_num")
        g_num = int(g_num) + 1
        east_act = data.get("east_act")
        south_act = data.get("south_act")
        west_act = data.get("west_act")
        north_act = data.get("north_act")
        room_style = data.get("room_style")
        if "6:" in east_act or "7:" in east_act :
            east_id = data.get("east_id")
            south_id = data.get("south_id")
            west_id = data.get("west_id")
            north_id = data.get("north_id")
        elif "6:" in south_act or "7:" in south_act :
            east_id = data.get("south_id")
            south_id = data.get("west_id")
            west_id = data.get("north_id")
            north_id = data.get("east_id")
        elif "6:" in west_act or "7:" in west_act :
            east_id = data.get("west_id")
            south_id = data.get("north_id")
            west_id = data.get("east_id")
            north_id = data.get("south_id")
        elif "6:" in north_act or "7:" in north_act :
            east_id = data.get("north_id")
            south_id = data.get("east_id")
            west_id = data.get("south_id")
            north_id = data.get("west_id")
        else :
            return g_num, east_id, west_id, south_id, north_id, room_style
        return g_num, east_id, west_id, south_id, north_id, room_style


# over
# def init_paishan(paishan):
#     raw_hand = ''.join(paishan[-13:])  # 发手牌
#     hand = mahjong_checker.hand_processer(raw_hand, raw_hand=True)
#     hand.sort(key=mahjong_checker.sort_hand)
#     # print len(paishan)
#     del paishan[-13:]
#     result = ','.join((str(i.get_rank()) + str(i.get_suit()) for i in hand)), paishan
#     return result


# over
def deal_paishan(paishan) :
    pai = sort_hand(paishan[0 :13])
    del paishan[0 : 13]
    return pai, paishan


# 排序
def sort_hand(pai) :
    raw_hand = ''.join(pai)  # 发手牌
    hand = mahjong_checker.hand_processer(raw_hand, raw_hand=True)
    hand.sort(key=mahjong_checker.sort_hand)
    result = ",".join((str(i.get_rank()) + str(i.get_suit()) for i in hand))
    return result


def get_panshan(flag, e_pionter) :  # flag不为空时则为要风牌
    dice = 0
    while dice < 4 :
        dice = random.randint(2, 12)  # 取骰子点数
    tmp = dice % 4
    bao = tmp + 1
    if tmp == 0 :
        bao, tmp = 1, 4  # 宝牌 & 发牌位置
    order = params.dic_random[e_pionter]  # 取四家牌发牌顺序
    last_len = dice * 2  # 宝牌位置
    if flag == 1 :  # 根据房间属性(是否要风牌)洗牌
        paishan = mahjong_checker.init_paishan()  # 包含风牌 140张
        li1, li2, li3, li4 = paishan[0 : 34], paishan[34 : 70], paishan[70 :104], paishan[104 : 140]
    else :
        paishan = mahjong_checker.init_paishan_T()  # 不包含风牌 112张
        li1, li2, li3, li4 = paishan[0 : 28], paishan[28 : 56], paishan[56 : 84], paishan[84 : 112]
    li1s_t = eval("li%s" % order[0])  # 抓牌位置
    li1s_t.reverse()  # 倒排
    pai_last = li1s_t[0 : last_len]  # 定牌尾
    li1s = li1s_t[last_len : len(li1s_t)]  # 定发牌点
    li4s = eval("li%s" % bao)  # 定宝牌位置
    bao = li4s[dice * 2 - 2]  # 取宝牌
    li4s.reverse()
    li4s = li4s + pai_last
    li2s = eval("li%s" % order[1])
    li2s.reverse()
    li3s = eval("li%s" % order[2])
    li3s.reverse()
    pai_result = li1s + li2s + li3s + li4s  # 生成抓牌顺序的牌山集合
    bao_index = len(li4s) - dice * 2 + len(li2s) + len(li3s) + len(li1s) - len(pai_last) + 1  # 计算宝牌位置
    bao_list = list(bao)
    num, str_ = int(bao_list[0]), bao_list[1]
    if num == 9 and str_ != "z" or num == 7 and str_ == "z" :  # 计算金牌
        num = 1
        jin = ["%s%s" % (num, str_)] * 4
    elif str_ == "t" :
        jin = ["1t", "2t", "3t", "4t"].remove(bao)
    else :
        num = num + 1
        jin = ["%s%s" % (num, str_)] * 4

    return pai_result, bao_index, bao, jin, li1, li2, li3, li4


# 3：碰；4：明杠；5：暗杠；6：胡; 7：接炮；
def get_act(u_pai, style_list, shou_pai=None, now_pai=None) :
    '''
    :param u_pai: 玩家牌
    :param shou_pai: 当前玩家抓的牌
    :param now_pai: 牌桌上玩家打出的牌
    :return: 事件
    '''
    act_value = []
    act3 = ""
    act4 = ""
    act5 = ""
    act6 = ""
    act7 = ""
    if shou_pai :  # 判断玩家抓牌事件
        mj = u_pai.append(shou_pai)
        hu6_pai = mj_hu6(mj)

        if hu6_pai :
            act6 = "6:%s" % shou_pai
    ag_pai = mj_angang(mj)
    if ag_pai :
        act5 = "5:%s" % ag_pai
    if now_pai :
        mj = u_pai.append(now_pai)
        if "7" not in style_list :
            hu7_pai = mj_hu7(mj)
            if hu7_pai :
                act7 = "7:%s" % now_pai
        mg_pai = mj_mgang(mj)
        if mg_pai :
            act4 = "4:%s" % mg_pai
        p_pai = mj_peng(mj)
        if p_pai :
            act3 = "3:%s" % p_pai
    if act3 :
        act_value.append(act3)
    if act4 :
        act_value.append(act4)
    if act5 :
        act_value.append(act5)
    if act6 :
        act_value.append(act6)
    if act7 :
        act_value.append(act7)

    return ';'.join(map(str, act_value))


def play_check(u_id, r_id) :
    '''
    校验当前房间里是否有该用户,是否能做当前申请的麻将事件
    :param u_id:
    :param r_id:
    :return:
    '''
    if not u_id or not r_id :
        # exit(0)
        return None, None
    game_info = mj_data.get_game_info(r_id)
    if not game_info :
        # exit(0)
        return None, None, None
    game_data = game_info[0]
    pointer = game_data.get("pointer").split(":")
    pointer_id = pointer[1]
    pointer_position = pointer[0]
    if str(u_id) != str(pointer_id) :
        return None, None, None, None
    else :
        users_info = {}
        for i in params.seats :
            users_info["%s_id", i] = game_data.get("%s_id" % params.seat_dict[i])
            users_info["%s_mj", i] = game_data.get("%s_mj" % params.seat_dict[i])
            users_info["%s_mg", i] = game_data.get("%s_mg" % params.seat_dict[i])
            users_info["%s_ag", i] = game_data.get("%s_ag" % params.seat_dict[i])
            users_info["%s_mf", i] = game_data.get("%s_mf" % params.seat_dict[i])
            users_info["%s_af", i] = game_data.get("%s_af" % params.seat_dict[i])
            users_info["%s_df", i] = game_data.get("%s_df" % params.seat_dict[i])
            users_info["%s_p", i] = game_data.get("%s_p" % params.seat_dict[i])
            users_info["%s_act", i] = game_data.get("%s_act" % params.seat_dict[i])
            users_info["%s_doact", i] = game_data.get("%s_doact" % params.seat_dict[i])
        return game_data, users_info, pointer_id, pointer_position


# 校验用户事件以及操作对象是否作弊
def act_check(pointer_position, game_data, u_act) :
    result_bol = False
    seat_item = params.seat_dict.get(pointer_position)
    act_his = game_data.get("%s_act" % seat_item)  # 用户历史事件集合
    act_list = str(u_act).split(":")  # 用户历史事件集合
    if len(act_list) != 2 :  # 非法数据
        return result_bol, None
    act = act_list[0]  # 用户事件
    act_obj = act_list[1]  # 用户事件操作对象
    acts = str(act_his).split(";")
    if act != str(2) :
        for item in acts :
            if str(item).split(":")[0] == str(act) and str(act_obj) in str(item).split(":")[1] :
                pai_list = str(item).split(":")[1].split(",")
                pai_list.remove(act_obj)
                acts.remove(item)
                if len(pai_list) != 0 :
                    pai_list.remove(act_obj)
                    item = "%s:%s" % act, ",".join(pai_list)
                    acts.append(item)
                result_bol = True
            if result_bol :
                break
    else :
        result_bol = True
    return result_bol, acts


# 抓牌 doing
def zhua_pai(r_id) :
    return None


# 牌局结果 doing
def play_result(room_id) :
    return None


def get_playjson(u_act, act, shoupai, pointer) :
    json = '''{"api":"play_mj","u_act":"%s","act":"%s","shoupai"="%s","pointer":"%s","result":"notice"}''' % (u_act, act, shoupai, pointer)
    return json


def room_result(room_id) :
    return None


# 打牌判断指针 封装消息
def get_act2_pointer(u_id, eact, sact, wact, nact, pointer_position, e_id, s_id, w_id, n_id, u_act, game_data, e0=params.eseats0, s0=params.sseats0, w0=params.wseats0, n0=params.nseats0, e=params.eseats, s=params.sseats, w=params.wseats, n=params.nseats) :
    '''
    :param u_id:
    :param eact,sact,wact,nact:
    :param pointer_position:
    :param e_id,s_id,w_id,n_id:
    :param u_act:
    :param game_data:
    :param e0,s0,w0,n0:
    :param e,s,w,n:
    :return:
    '''
    # 通知房间其他玩家当前用户做了什么事件
    # room_item = {"topic": "%s%s" % (eval("%s_id" % pointer_position), "_server"), "mes": "act:%s,pointer:0" % eval("%sact" % pointer_position)}
    old_mj = game_data.get("old_mj")  # 牌桌上打出的牌
    liuju = False
    # 通知房间所有玩家是否有可做事件
    result_item = {}
    # 封装消息集合包含topic payload消息题
    result_list = []
    for i in params.seats :
        # mes = '''{"api":"play_mj","u_act":"%s","act":"%s","shoupai"="","pointer":"0","result":"notice"}''' % (u_act, names["%sact" % i])
        result_item[i] = {"topic" : "%s%s" % (eval("%s_id" % i), "_server"), "mes" : get_playjson(u_act, eval("%sact" % i), "", "0")}
    # 0：无动作(过)；1：抓牌；2：打牌；3：碰；4：明杠；5：暗杠；6：胡; 7：接炮；8：点炮；9：申请终止牌局；10：同意终止牌局；11：不同意终止牌局
    order = eval("%s0" % pointer_position)  # 打牌顺序
    shoupai = params.seat_dict[order[0]]  # 手牌具备指针功能(当东家打牌,但西南家有碰or杠则保持指针在北家,shoupai存储west)
    nowpai = str(u_id) + ":" + str(str(u_act).split(":")[1])  # 牌桌上的牌,用来标示当前玩家打出的牌
    flag = False
    # 根据order 计算那个玩家为下家,if 4:杠牌需要存储杠牌,并给玩家发牌(玩家决定是否需要杠牌,if不杠则过发的牌and自动放弃,else杠自动显示发的牌--少一次通信),并判断事件
    for i in ["7:", "4:", "3:"] :
        for o in order :
            if i in eval("%s%s" % (o, "act")) :
                pointer_new = "%s:%s" % (params.seat_dict[o], eval("%s_id" % o))  # 记录指针位置为当前事件权重最高的玩家
                if order[0] == o :
                    shoupai = None
                if i == "4:" :
                    pai = mj_data.get_pai(game_data.get("r_id"), game_data.get("g_num"), flag=False)
                    # if shoupai == "0": liuju = True # if shoupai == 0 流局 -- 由杠导致,因杠要抓牌,但牌已经不够数,因此流局,但当前流程不构成流局,因抓牌行为还为发生
                mes = get_playjson(u_act, eval("%sact" % i), pai, "1")
                result_item[o] = {"topic" : "%s%s" % (eval("%s_id" % i), "_server"), "mes" : mes}
                flag = True
            if flag :
                break
        if flag :
            break

    # if not flag and str(u_act).split(":")[0] != str(2): # 若经过上面判断找不出有高权重事件的玩家,则指针顺势指向下一家,并发牌判断当前拿牌是否存在事件
    if not flag :  # 若经过上面判断找不出有高权重事件的玩家,则指针顺势指向下一家,并发牌判断当前拿牌是否存在事件
        # pai = mj_data.get_pai(r_id,game_data.get("g_num"),str(u_act).split(":")[0])
        pai, flag = mj_data.get_pai(game_data.get("r_id"), game_data.get("g_num"))
        if not flag :
            act = get_act(game_data.get("%s_mj" % params.seat_dict[pointer_position]), game_data.get("room_style"), shoupai=pai, now_pai=None)
            act_dict = {"e" : eact, "s" : sact, "w" : wact, "n" : nact}
            for i in params.seats :
                if i != pointer_position :
                    act_dict[i] = eval("%sact" % i)
                else :
                    act_dict[i] = act
            shoupai = eval("%s_id" % pointer_position) + ":" + pai
            # mes = '''{"api":"play_mj","u_act":"%s","act":"%s","shoupai":"%s","pointer":"1","result":"notice"}''' % (u_act, names["%sact" % order[0]])
            mes = get_playjson(u_act, eval("%sact" % order[0]), "1")
            result_item[order[0]] = {"topic" : "%s%s" % (eval("%s_id" % i), "_server"), "mes" : mes}
            result_item[pointer_position]["mes"] = result_item[pointer_position]["mes"][:-1] + str(1)
            pointer_new = "%s:%s" % (order[0], eval("%s_id" % pointer_position))
            old_mj = "%s,%s" % (old_mj, str(str(u_act).split(":")[1]))

        # else:#找出事件人 则发送事件
        #     result_item[order[0]]["mes"] = result_item[o]["mes"][:-1] + str(1)
        else :
            liuju = True  # 游戏终止 流局
            result_item = {}
    result_list.append(result_item)
    # pointer_new返回指针位置--存储入库,shoupai存储数据用记录指针功能(当东家打牌,但西南家有碰or杠则保持指针在北家,shoupai存储west),result_list消息推送用,liuju判断是否流局,如果流局则result_list为空!
    return pointer_new, shoupai, result_list, nowpai, old_mj, liuju
