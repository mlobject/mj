# -*- coding: utf-8 -*-
__author__ = 'huzixu'

import paho.mqtt.client as mqtt
import json
from mqtt_config import *
from impl import impl_controller
from impl import user_impl


# 客户端订阅某个主题
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# 消息推送回调函数
# 处理客户端连接断开以后的消息
def on_message(mqttc, obj, msg):
    message = msg.payload.decode("utf8")
    print message
    disconnect_msg = json.loads(msg)
    u_id = disconnect_msg["u_id"]
    room_id = disconnect_msg["r_id"]
    # 调用掉线方法
    user_impl.user_offoron_line(room_id, u_id, 0)


def main():
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.connect(mqtt_host, mqtt_port, mqtt_keepalive)
    mqttc.subscribe(mqtt_will_topic, mqtt_qos)
    mqttc.loop_forever()


if __name__ == '__main__':
    main()
