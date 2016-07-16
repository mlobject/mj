# -*- coding: utf-8 -*-
__author__ = 'huzixu'

# Author: Frank-the-Obscure @ Organzation Labortory @ GitHub
# mahjong AI

# import autogui
import time
import mahjong_checker
import mahjong


def heqie(hand, output_notes=False):
    """何切函数

    i: 14 card Class
    p: 比较打每张牌的向听数和有效牌
        暂时只比较种类, 不考虑张数不同
    o: 打某张牌, 及向听数
    """
    xiangtingshu_lowest = 8
    youxiaopai_max = 0
    # 统计出最小向听数和有效牌种类, MVP 版本中只取第一张
    hand.sort(key=mahjong_checker.sort_hand)

    xiangtingshu_14, num_youxiaopai, list_youxiaopai = mahjong.cal_xiangtingshu(hand, raw_hand=False)
    if xiangtingshu_14 == -1:  # 已经和牌
        return '', -1

    card0 = ''  # 排除相同牌, 可一定程度上提高速度
    for card in hand:  # 循环打每一张牌, 判断哪张向听数最小且有效牌多.
        if mahjong_checker.is_samecard(card, card0):  # 排除相同牌, 可一定程度上提高速度
            continue
        hand_card = hand[:]
        hand_card.remove(card)
        xiangtingshu, num_youxiaopai, list_youxiaopai = mahjong.cal_xiangtingshu(hand_card, raw_hand=False)
        if xiangtingshu < xiangtingshu_lowest:  # 最小向听数
            best_card = (card, xiangtingshu, num_youxiaopai, list_youxiaopai)
            xiangtingshu_lowest = xiangtingshu
            youxiaopai_max = num_youxiaopai
        elif (xiangtingshu == xiangtingshu_lowest and num_youxiaopai > youxiaopai_max):  # 或者相同向听数,但有效牌更多
            best_card = (card, xiangtingshu, num_youxiaopai, list_youxiaopai)
            youxiaopai_max = num_youxiaopai
        card0 = card
    card, xiangtingshu, num_youxiaopai, list_youxiaopai = best_card
    if output_notes:  # 输出调试信息
        youxiaopai = ''
        for i in list_youxiaopai:
            youxiaopai += str(i)
        print('打{}, 向听数{}, 有效牌{}, {}种{}张'.format(card, xiangtingshu, youxiaopai, len(list_youxiaopai), num_youxiaopai))

    return card, xiangtingshu  # 返回切出的牌及向听数


def heqie_tester():
    """发牌器, 测试何切函数
    """
    paishan = mahjong_checker.init_paishan()  # init
    print paishan
    print len(paishan)
    raw_hand1 = ''.join(paishan[-13:])  # 发手牌
    del paishan[-13:]
    raw_hand2 = ''.join(paishan[-13:])  # 发手牌
    del paishan[-13:]
    raw_hand3 = ''.join(paishan[-13:])  # 发手牌
    del paishan[-13:]
    raw_hand4 = ''.join(paishan[-13:])  # 发手牌
    del paishan[-13:]
    print paishan
    raw_hand5 = ''.join(paishan[-1:])  # 发手牌
    del paishan[-1:]
    print paishan
    print raw_hand5
    print raw_hand1
    print raw_hand2
    print raw_hand3
    print raw_hand4
    print paishan


    hand1 = mahjong_checker.hand_processer(raw_hand1, raw_hand=True)
    hand2 = mahjong_checker.hand_processer(raw_hand2, raw_hand=True)
    hand3 = mahjong_checker.hand_processer(raw_hand3, raw_hand=True)
    hand4 = mahjong_checker.hand_processer(raw_hand4, raw_hand=True)

    pai_list1=[]
    pai_list2=[]
    pai_list3=[]
    pai_list4=[]

    hand1.sort(key=mahjong_checker.sort_hand)
    hand2.sort(key=mahjong_checker.sort_hand)
    hand3.sort(key=mahjong_checker.sort_hand)
    hand4.sort(key=mahjong_checker.sort_hand)

    for i in hand1:
        pai_list1.append(str(i.get_rank())+str(i.get_suit()))
    print pai_list1

    for i in hand2:
        pai_list2.append(str(i.get_rank())+str(i.get_suit()))
    print pai_list2

    for i in hand3:
        pai_list3.append(str(i.get_rank())+str(i.get_suit()))
    print pai_list3

    for i in hand4:
        pai_list4.append(str(i.get_rank())+str(i.get_suit()))
    print pai_list4

    for card in hand1:
        mahjong_checker.used_card(card)  # 计算剩余牌量


    # while paishan:
    #     print('剩余牌量:', len(paishan))
    #     new_card = paishan.pop()  # 出一张牌
    #     checker.used_card(new_card)  # 计算剩余牌量
    #     # print('hand: ', end = '')
    #     print('hand: ', '')
    #     hand.sort(key=checker.sort_hand)
    #     checker.print_hand(hand)
    #     print('new card', new_card)
    #     hand = hand + [checker.Card(new_card)]
    #     discard_card, xiangtingshu = heqie(hand, output_notes=True)
    #     print('discard card:', discard_card)
    #     print('xiangtingshu:', xiangtingshu)
    #     print()
    #     if discard_card:
    #         for card in hand:
    #             if checker.is_samecard(card, discard_card):
    #                 hand.remove(card)
    #                 break
    #     else:
    #         print('和牌')
    #         return True
    # else:
    #     print('牌山没牌了.')


# def ai():
#     """ai using 国标v1.30
#     读取手牌-(读取新摸牌-切牌)
#     """
#     raw_hand = autogui.get_hand()
#     hand = checker.hand_processer(raw_hand, raw_hand=True)
#
#     for card in hand:
#         checker.used_card(card)  # 计算剩余牌量
#
#     while True:
#         time.sleep(1)
#         autogui.pass_mingpai()
#         time.sleep(1)
#         autogui.pass_mingpai()
#         time.sleep(1)
#         autogui.pass_mingpai()
#         time.sleep(1)
#
#         new_card = autogui.get_card()  # 出一张牌
#         checker.used_card(new_card)  # 计算剩余牌量
#         # print('hand: ', end = '')
#         print('hand: ', '')
#         hand.sort(key=checker.sort_hand)
#         checker.print_hand(hand)
#         print('new card', new_card)
#         hand_plus = hand + [checker.Card(new_card)]
#         discard_card, xiangtingshu = heqie(hand_plus, output_notes=True)
#         print('discard card:', discard_card)
#         print('xiangtingshu:', xiangtingshu)
#         if discard_card:
#             for card in hand:
#                 if checker.is_samecard(card, discard_card):
#                     print('切第n张:', hand.index(card))
#                     autogui.qiepai(hand.index(card))
#                     hand_plus.remove(card)
#                     hand = hand_plus
#                     break
#             else:
#                 autogui.qiepai(13)
#         else:
#             print('和牌')
#             return True
#     else:
#         print('牌山没牌了.')
#

print heqie_tester()

# def main():
#     ai()
#
#
# if __name__ == '__main__':
#     main()
