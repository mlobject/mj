# -*- coding: utf-8 -*-
__author__ = 'huzixu'
# import os
# import random, string
# from mjmanage import mahjong_checker
# from config import mj_param
# params = mj_param.impl_param()
# def get_panshan(flag, e_pionter) :  # flag不为空时则为要风牌
#     dice = 0
#     while dice < 4 :
#         dice = random.randint(2, 12)  # 取骰子点数
#     tmp = dice % 4
#     bao = tmp + 1
#     if tmp == 0 :
#         bao, tmp = 1, 4  # 宝牌 & 发牌位置
#     order = params.dic_random[e_pionter]  # 取四家牌发牌顺序
#     last_len = dice * 2  # 宝牌位置
#     if flag :  # 根据房间属性(是否要风牌)洗牌
#         paishan = mahjong_checker.init_paishan()  # 包含风牌 140张
#         li1, li2, li3, li4 = paishan[0: 34], paishan[34: 70], paishan[70:104], paishan[104: 140]
#     else :
#         paishan = mahjong_checker.init_paishan_T()  # 不包含风牌 112张
#         li1, li2, li3, li4 = paishan[0: 28], paishan[28: 56], paishan[56: 84], paishan[84: 112]
#     li1s_t = eval("li%s" % order[0])  # 抓牌位置
#     li1s_t.reverse()  # 倒排
#     pai_last = li1s_t[0: last_len]  # 定牌尾
#     li1s = li1s_t[last_len: len(li1s_t)]  # 定发牌点
#     li4s = eval("li%s" % bao)  # 定宝牌位置
#     bao = li4s[dice * 2 - 2]  # 取宝牌
#     li4s.reverse()
#     li4s = li4s + pai_last
#     li2s = eval("li%s" % order[1])
#     li2s.reverse()
#     li3s = eval("li%s" % order[2])
#     li3s.reverse()
#     pai_result = li1s + li2s + li3s + li4s  # 生成抓牌顺序的牌山集合
#     bao_index = len(li4s) - dice * 2 + len(li2s) + len(li3s) + len(li1s) - len(pai_last) + 1  # 计算宝牌位置
#     bao_list = list(bao)
#     num, str_ = int(bao_list[0]), bao_list[1]
#     if num == 9 and str_ != "z" or num == 7 and str_ == "z" :  # 计算金牌
#         num = 1
#     else :
#         num = num + 1
#     jin = "%s%s" % (num, str_)
#     pai_dict = li1, li2, li3, li4
#     print "random = " + str(dice)
#     print "order = " + str(order)
#     print li1
#     print li2
#     print li3
#     print li4
#     print "bao = " + str(bao)
#     print "jin = " + jin
#     print "bao_index = " + str(bao_index)
#     print pai_result
#     print pai_result[bao_index]
#     print "pai_dict = " + str(pai_dict)
#     if bao in ["1t", "2t", "3t", "4t"] :
#         get_panshan(flag, e_pionter)
#     return pai_result, bao_index, bao, jin, pai_dict, e_pionter, flag

# print "random = " + str(dice)
# print "order = " + str(order)
# print li1
# print li2
# print li3
# print li4
# print "bao = " + str(bao)
# print "jin = " + jin
# print "bao_index = " + str(bao_index)
# print pai_result
# print pai_result[bao_index]
# print "pai_dict = " + str(pai_dict)

import ujson as json
# def print_test(value):
#     print value
#
#
from config import mj_param
# print param.succ
#
#
# print random.sample(string.ascii_letters+string.digits, 8)
# print ''.join(random.sample(string.digits, 8))
#
#
# def test():
#     li = []
#     for i in range(3):
#         li.append(i)
#     return li
# print "r_ids:%s" % ','.join(str(i) for i in test() )
#
# mylist = [1,2,2,2,2,3,3,3,4,4,4,4]
# myset = set(mylist)  #myset是另外一个列表，里面的内容是mylist里面的无重复 项
# for item in myset:
#   print("the %d has found %d" %(item,mylist.count(item)))
#
#
# dict = {}
# dict.setdefault("a")
# print dict
# dict["a"] = "apple"
# dict.setdefault("a","default")
# print dict
# dict.setdefault("c","bbbbb")
# dict[1] = 2
# dict.__setitem__("b","f")
# print dict
# print
#
# str = "1,2,3,4,5,6"
#
# str_li = str.split(",")
#
# print str_li
# if "1" not in str_li:
#     print "not 1"
# else:
#     print "have 1"


# def play_check(u_id,r_id):
#     if not u_id or not r_id:
#         print 111111111111111
#         return None,3
#     else:
#         print 22222222222222222
#         return u_id,r_id
#
#
# u_id,r_id = play_check("1","1")
# print play_check(None,None)
# print play_check("1","1")
#
# str = "1"
# str_l = str.split(":")
# print str[0]

# li = []
# str_convert =  ','.join(map(str,li))
# print str_convert
# if str_convert:
#     print 1
# else:
#     print 2
# for i in ["e","s","w","n"]:
#         print i

# a = "s"
# li = ["e","s","w","n"]
#
# print li.index(a)
#
#
# f = li[:li.index(a)+1]
# b = li.index(a)+1
# li[len(li):len(li)] = f
# del li[:b]
# print li
# pointer_position_new = "e"
#
# def package_result(e_dict, s_dict, w_dict, n_dict):
#     result_list = []
#     result_list.append(e_dict)
#     result_list.append(w_dict)
#     result_list.append(s_dict)
#     result_list.append(n_dict)
#     return result_list
#
#
# def get_pointer(r_id, eact, sact, wact, nact, pointer_position, e_id, s_id, w_id, n_id, u_act, game_data):
#     # 判断是否有胡
#     if pointer_position == "n" and "6:" in eact or "7:" in ():
#         pass
#     if pointer_position == "n" and "6:" in eact or "7:" in eact:
#         pointer_position_new = "e"
#         east_dict = {"topic": e_id + "_server", "mes": "act:%s,pointer:1" % eact}
#         south_dict = {"topic": s_id + "_server", "mes": "act:%s,pointer:0" % sact}
#         west_dict = {"topic": w_id + "_server", "mes": "act:%s,pointer:0" % wact}
#         north_dict = {"topic": n_id + "_server", "mes": "act:%s,pointer:0" % nact}
#         result_list = package_result(east_dict, south_dict, west_dict, north_dict)
#         return pointer_position_new, e_id, "%s:%s" % (
#             pointer_position_new, e_id), eact, None, sact, None, wact, None, nact, u_act, result_list
#
#
# def test(r_id, eact, sact, wact, nact, pointer_position, e_id, s_id, w_id, n_id, u_act, game_data, e0=param.eseats0,
#          s0=param.sseats0, w0=param.wseats0, n0=param.nseats0, e=param.eseats, s=param.sseats, w=param.wseats,
#          n=param.nseats):
#     names = locals()
#     # print names["%s_id" % pointer_position]
#     pointer_item = {"topic": "%s%s" % (names["%s_id" % pointer_position], "_server"),
#                     "mes": "act:%s,pointer:0" % names["%sact" % pointer_position]}
#     result_item = []
#     result_list = []
#     for i in param.seats:
#         result_item.append(
#             {i: {"topic": "%s%s" % (names["%s_id" % i], "_server"), "mes": "act:%s,pointer:0" % names["%sact" % i]}})
#     # 不是过
#     if str(u_act).split(":")[0] != str(0):
#         print names[pointer_position]
#         # pointer_temp = param.a
#         # pointer_temp = param.names["%sseats" % pointer_position]
#         print "ssss" + str(pointer_item)
#         # act_dict = {"e": eact, "s": sact, "w": wact, "n": nact}
#         # print eact
#         #
#         # r_index = param.seats.index(pointer_position) + 1
#         # if r_index == 4:
#         #     r_index = 0
#         # pointer_new = param.seats[r_index]
#         # result_list[r_index]["mes"] = result_list[r_index]["mes"][:-1] + str(1)
#         #
#         # # 按胡 接胡 (明暗)杠 碰依次判断4家事件
#         # for item in ["6:","7:","4:","5:","3:"]:
#
#
# def get_pointer(r_id, eact, sact, wact, nact, pointer_position, e_id, s_id, w_id, n_id, u_act, game_data, e0=param.eseats0,
#           s0=param.sseats0, w0=param.wseats0, n0=param.nseats0, e=param.eseats, s=param.sseats, w=param.wseats,
#           n=param.nseats):
#     names = locals()
#     # print names["%s_id" % pointer_position]
#     pointer_item = {"topic": "%s%s" % (names["%s_id" % pointer_position], "_server"),
#                     "mes": "act:%s,pointer:0" % names["%sact" % pointer_position]}
#     result_item = {}
#     result_list = []
#     for i in param.seats:
#         result_item[i] = {"topic": "%s%s" % (names["%s_id" % i], "_server"),"mes": "act:%s,pointer:0" % names["%sact" % i]}
#     print result_item
#     # 不是过
#     if str(u_act).split(":")[0] != str(0):
#         order = names[pointer_position]
#     else:
#         order = names["%s0" % pointer_position]
#     print order
#     flag = False
#     for i in ["6:", "7:", "4:", "5:", "3:"]:# 根据order 计算那个玩家为下家
#         print i
#         for o in order:
#             if i in names["%s%s" % (o, "act")]:
#                 result_item[o]["mes"] = result_item[o]["mes"][:-1] + str(1)
#                 flag = True
#             if flag: break
#         if flag: break
#     if not flag and str(u_act).split(":")[0] != str(0): # 若经过上面判断找不出有高权重事件的玩家,则指针顺势指向下一家
#         print order
#         print order[1]
#         result_item[order[1]]["mes"] = result_item[o]["mes"][:-1] + str(1)
#     else:
#         result_item[order[0]]["mes"] = result_item[o]["mes"][:-1] + str(1)
#     return
#
#
#
#
# # dicts = {"topic": "001_server","mess":"hello"}
# # print str(dicts.get("topic")).replace("_server","")
#
# list_s = ["1", "2", "3", "4", "5", "6"]
# list_v = ["9", "8", "7", "10", "5"]
# a = "1"
# print list_s
# list_s.remove(a)
# print list_s
# list_s.append(a)
# print ",".join(list_s)
# print list_s
#
# list_b = ""
# print ".".join(list_b)
# print "777"
#
#
# a = 1
# b = 1
#
# c = "a"
#
# names = locals()
# print names["a"]
#
# a = None
# print a
#
# a = 3333
# print a
#
#
# def a():
#     a = ""
#     b = ""
#     c = ""
#     a = 1
#     if a == 1:
#         b = 2
#     else:
#         c = 3
#
#     return a,b,c
# print a()

# a = ""
# # json_str = json.loads(a)
#
# if a:
#     json_str = json.loads(a)
# else:
#     print "Null"
#
# d2 = {'spam': 2, 'ham': 1, 'eggs': 3}  # make a dictionary
#
# print d2  # order is scrambled
#
# d2['ham'] = ['grill', 'bake', 'fry']  # change entry
#
# print d2
#
# act_value = []
# ';'.join(map(str, act_value))
#
# b_list = ["1m", "1p", "1m", "2z", "3p", "4t", "1m", "2t"]
# print  b_list.sort()
# print b_list
#
# print random.randint(12, 20)
#
# print 10%4

# from mjmanage import mahjong_checker, mj_utils, mj_data
#
# paishan = mahjong_checker.init_paishan()  # init
# paishan_nofeng = mahjong_checker.init_paishan_T()
# print paishan
#
# list1 = paishan.__getslice__(0,34)
# list2 = paishan.__getslice__(34,68)
# list3 = paishan.__getslice__(68,102)
# list4 = paishan.__getslice__(102,136)
#
# print paishan_nofeng
# list_1 = paishan_nofeng.__getslice__(0,27)
# list_2 = paishan_nofeng.__getslice__(27,54)
# list_3 = paishan_nofeng.__getslice__(54,81)
# list_4 = paishan_nofeng.__getslice__(81,108)




# dictt = {"e":"123"}
# strs = "easdcsadf"
# print strs[0]
#
# a = "1111"
# if a:
#     print 111
# else:
#     print 2221
#
#

#
# paishan = mahjong_checker.init_paishan_T()

#
# def get_dice(paishan, flag) :
#     '''
#     :param paishan: 牌山
#     :param flag: 是否要风牌标示
#     :return:
#     '''
#     a = random.randint(2, 12)
#     if a < 4 :
#         a = a + 2
#     # pai_dict = {0:}
#     if flag == 0 :  # 不要风牌
#         li1 = paishan.__getslice__(0, 28)
#         li2 = paishan.__getslice__(28, 55)
#         li3 = paishan.__getslice__(55, 82)
#         li4 = paishan.__getslice__(82, 109)
#     else :
#         li1 = paishan.__getslice__(0, 35)
#         li2 = paishan.__getslice__(35, 69)
#         li3 = paishan.__getslice__(69, 103)
#         li4 = paishan.__getslice__(102, 136)
#     paishan_dict = {1 : li1, 2 : li2, 3 : li3, 4 : li4}
#     if a % 4 == 0 :
#         pointer = 0
#         paishan = 0
#     return a % 4

# import re
# a = "1m2p1m3z"
# print re.search("[mpz]",a).group()   #123abc456,返回整体


# 1,2,3,4,5,6,7,8,9
# 11,12,13,14,15,16,17,18,19
# 21,22,23,24,25,26,27,28,29
# 31,32,33,34,35,36,37
# 41,42,43,44




li = [1,1,2,4,5,7]
li.sort()
print li



