# -*- coding: utf-8 -*-
__author__ = 'huzixu'

import sys
import datetime
import socket, sys
import paho.mqtt.client as mqtt
from mqtt_config import *

reload(sys)
sys.setdefaultencoding('utf8')

HOST = "121.199.14.95"
PORT = 1883


def transmitMQTT(strMsg):
    # mqttc = mqtt.Client(client_id="随机不能重复",clean_session=False)
    mqttc = mqtt.Client()
    # mqttc = mqttc.tls_set(self, ca_certs, certfile=None, keyfile=None, cert_reqs=cert_reqs, tls_version=tls_version, ciphers=None)
    topic = "login"
    # if PORT != 1883:
    #     # 加密
    #     mqttc.tls_set(ca_certs, certfile=certfile, keyfile=keyfile)
    #     # 不需要验证ip地址
    #     mqttc.tls_insecure_set(insecure)
    # mqttc.will_set("disconnect", "publish connect broken", 1)
    mqttc.connect(HOST, PORT, 60,)
    # for i in range(10):
    mqttc.publish(topic, payload=strMsg, qos=1, retain=True)
#     {"api":"login","u_id":"001"}
if __name__ == '__main__':

    transmitMQTT('{"api":"login","u_id":"002"}')
    # transmitMQTT('{"wx_openid":"abcdef4","wx_sex":"1","api":"login","wx_nickname":"麻将玩家A","wx_headimgurl":"http:\/\/asdfasfe\/abc","wx_country":"CN"}')
    # result = topic:002_server payload:{"api":"login","u_id":"bec7cc","card_num":"3","result":"succ"}

    # transmitMQTT('{"api":"create_room","u_id":"bec7cc","room_style":"1,2,4"}')
    # rsult = topic:bec7cc_server payload:{"api":"create_room","r_id":"349870","result":"succ"}

    # transmitMQTT('''{"api":"enter_room", "u_id":"bec7cc", "r_id":"349870"}''')
    # transmitMQTT('''{"api":"enter_room", "u_id":"ae50d7", "r_id":"349870"}''')
    # transmitMQTT('''{"api":"enter_room", "u_id":"5af1fe", "r_id":"349870"}''')
    # transmitMQTT('''{"api":"enter_room", "u_id":"1ebfac", "r_id":"349870"}''')
    # result= topic:349870_server,payload:{"api":"enter_room","u_id":"bec7cc","wx_nickname":"None","wx_sex":"0","wx_country":"None","wx_headimgurl":"None","speed_type":"0","escape_num":"0","break_num":"0","result":"succ"}
