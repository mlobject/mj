# -*- coding: utf-8 -*-
__author__ = 'huzixu'
import random

lis_wan = [1, 2, 3, 4, 5, 6, 7, 8, 9]
lis_ton = [11, 12, 13, 14, 15, 16, 17, 18, 19]
lis_tiao = [21, 22, 23, 24, 25, 26, 27, 28, 29]
lis_zi = [31, 32, 33, 34, 35, 36, 37]
lis_hua = [41, 42, 43, 44]
pai_13 = [1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37]

list = lis_wan * 4 + lis_tiao * 4 + lis_ton * 4 + lis_zi * 4 + lis_hua

# print len(list)
#
# print len(pai_13)
# random.shuffle(list)
# print list
# list.sort()
# print list

JIAMIAN = ['cha_2', 'cha_1']
GUPAI = ['cha>2', 'zi']
JIANG = ['double']
ZHENMIAN = ['ke', 'shun', 'peng', 'gang']


def is_samecard(card1, card2) :
    return card1 == card2


# 4金胡牌
def check_4jin(jin_card_num=0) :
    return jin_card_num == 4


# 7小对
def check_qidui(card_lis, jin_card_num=0) :
    all_len = len(card_lis) + jin_card_num
    if all_len != 14 :
        return False
    card_lis.sort()
    i = 0
    j = 0
    card_len = len(card_lis)
    while i < card_len and i + 1 < card_len :
        if is_samecard(card_lis[i], card_lis[i + 1]) :
            j += 1
            i += 2
        else :
            i += 1
    if j + jin_card_num == 7 or j == 7 :
        return True
    else :
        return False


# 13妖
def check_13(card_lis, jin_card_num=0) :
    card_lis.sort()
    all_len = len(card_lis) + jin_card_num
    if all_len != 14 :
        return False
    yao_13 = [1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37]
    card_len = len(card_lis)
    i = 0
    k = 0
    while i < card_len :
        if k < 2 and len(yao_13) != 0 and card_lis[i] in yao_13 :
            yao_13.remove(card_lis[i])
            i += 1
        elif k < 2 :
            k += 1
            i += 1
        else :
            return False
    if len(yao_13) == jin_card_num :
        return True


from collections import Counter


def get_jiang_ke_num(card_lis) :
    dic = Counter(card_lis)
    num_2 = {10 : [], 20 : [], 30 : [], 40 : []}
    num_3 = {10 : [], 20 : [], 30 : [], 40 : []}
    jiang_num = 0
    ke_num = 0
    for (k, v) in dic.items() :
        if v > 1 :
            if v == 4:
                jiang_num +=2
            elif v == 2:
                jiang_num +=1
            else:
                ke_num += 1
            if k < 10 :
                f = v / 2 if v == 4 else v
                eval("num_%s" % f)[10].append(k if v < 4 else [k, k])
            elif 10 < k < 20 :
                f = v / 2 if v == 4 else v
                eval("num_%s" % f)[10].append(k if v < 4 else [k, k])
            elif 20 < k < 30 :
                f = v / 2 if v == 4 else v
                eval("num_%s" % f)[10].append(k if v < 4 else [k, k])
            elif 30 < k < 40 :
                f = v / 2 if v == 4 else v
                eval("num_%s" % f)[10].append(k if v < 4 else [k, k])
            card_lis = [i for i in card_lis if i != k]
    card_lis.sort()
    return num_2, num_3,jiang_num,ke_num, card_lis


card_lis = [1, 1, 1, 1, 11, 11, 11, 32, 33, 34, 35, 36, 36]
num_jiang, num_ke,jiang_num,ke_num, card_lis = get_jiang_ke_num(card_lis)
print num_jiang
print num_ke
print jiang_num
print ke_num
print card_lis



# 校验是否顺子
def check_shun(card1, card2, card3) :
    return card3 - card2 == card1


# 校验两张拍是否假面
def check_jiamian(card1, card2) :
    return card2 - card1 < 2


# 一般胡牌4面1将校验
def check_432(card_lis, gang_num=0, peng_num=0, jin_card_num=0) :
    '''
    先取面子数,再取对子数,再取孤张 计算缺金牌
    先取对子数,再取面子数,再算孤张 计算缺金牌
    :param card_lis:
    :param jin_card_num:
    :return:
    '''
    # 是否按万条饼 分辨计算将,刻,顺的数量?
    jiang_num = 0  # 将数量
    ke_num = 0  # 刻数量
    shun_num = 0  # 顺数量
    gucard_num = 0  # 孤牌数量
    jiamian_num = 0  # 假面数量差<2

    # jiang_num_ = {10 : [], 20 : [], 30 : [], 40 : []}
    # ke_dic = {10 : [], 20 : [], 30 : [], 40 : []}
    shun_num_ = {10 : [], 20 : [], 30 : []}
    gucard_num_ = {10 : [], 20 : [], 30 : 0, 40 : []}
    jiamian_num_ = {10 : [], 20 : [], 30 : []}

    jiang_dic, ke_dic,jiang_num,ke_num, card_item = get_jiang_ke_num(card_lis)

    if len(ke_dic) + len(shun_num_) + gang_num + peng_num == 4 and (len(jiang_dic) == 2 or jin_card_num == 1) :
        return True
    if len(jiamian_num_) + jin_card_num == 4 and len(jiang_dic) == 1 :
        return True
    if len(jiang_dic) > 2 and jin_card_num == len(jiang_dic) - 1 and gucard_num == 0 :
        return True

    list_10 = []
    list_20 = []
    list_30 = []
    list_40 = []

    return True


def check_hu(card_lis, jin_card_num=0) :
    if check_4jin(jin_card_num) :
        return True
    if check_qidui(card_lis, jin_card_num) :
        print "7 对"
        return True
    if check_13(card_lis, jin_card_num) :
        print "13妖 "
        return True
    if check_432(card_lis, jin_card_num) :
        return True
    return False


card_lis = [1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 36]
check_hu(card_lis)

print
