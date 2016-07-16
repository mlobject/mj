# -*- coding: utf-8 -*-
__author__ = 'hu'
import threading
import traceback
import datetime
import paho.mqtt.client as mqtt
# from mqtt_config import *
# from impl import impl_controller

threads = []
# 客户端发送消息的topic
# client_publish_topic_prefix = "p_"

# 客户端接收消息的topic
# client_subscribe_topic_prefix = "s_"

mqtt_host = "121.199.14.95"
mqtt_port = 1883
mqtt_qos = 2
# 连接成功回调函数,客户端连接到MQTT代理
def on_connect(mqttc, obj, rc):
    pass
    #print("OnConnetc, rc: " + str(rc))
    #mqttc.subscribe("topic2", qos=1)


# 客户端订阅某个主题
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# 消息推送回调函数
def on_message(mqttc, obj, msg):
    curtime = datetime.datetime.now()
    strcurtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    print("qos = " + str(msg.qos) + '/n')
    print(strcurtime + ": " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    # topic的格式：s_roomid
    # room_id = msg.topic.split("_")[1]

    message = msg.payload.decode("utf8")
    print message
    # flag, result = impl_controller.impl_controller(msg.topic, str(message))
    # if result:
    #     for data in result:
    #         topic = data.get("topic")
    #         mes = data.get("mes")
    #         mqttc.publish(topic, mes)


# 创建订阅者
def create_subject(topic):
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.will_set("disconnect", "connection broken,u_id:10011", mqtt_qos)
    if mqtt_port != 1883:
        # # 加密
        # mqttc.tls_set(ca_certs, certfile=certfile, keyfile=keyfile)
        # # 不需要验证ip地址
        # mqttc.tls_insecure_set(insecure)
        pass

    mqttc.connect(mqtt_host, mqtt_port, 60)
    mqttc.subscribe(topic, mqtt_qos)
    mqttc.loop_forever()


# 创建房间监听线程
def create_thread(topic_value):
    try:
        topic = str(topic_value)
        print topic
        thread = threading.Thread(target=create_subject, args=(topic,))
        thread.start()
    except Exception as e:
        traceback.print_exc()
        raise e


def main(topic):
    try:
        create_thread(topic)

    except Exception as e:
        traceback.print_exc()
        raise e


if __name__ == "__main__":
    main("001_server") # 登录注册
    # main("create_room") # 登录注册
    # main("enter_room") # 进入房间
    # main("stop_game") # 终止游戏
    # main("signout_room") # 退出房间
    # main("start_mj") # 首局开始游戏
    # main("play_mj") # 麻将游戏

