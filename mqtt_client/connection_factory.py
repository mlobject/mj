# -*- coding: utf-8 -*-
__author__ = 'hu'
import threading, sys, traceback, datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from mqtt_config import *
from impl import impl_controller

from utils import db_toolkit, memsql_config

threads = []

messageId = 0
# 客户端发送消息的topic
# client_publish_topic_prefix = "p_"

# 客户端接收消息的topic
# client_subscribe_topic_prefix = "s_"
reload(sys)
sys.setdefaultencoding('utf8')

def insert_data_into_memsql(table, day_time, topic, message, qos) :
    db = db_toolkit.DBToolkit(memsql_config.CmsMysqlConfig())
    sql = "insert into %s(day_time,topic,payload,qos) values('%s','%s','%s','%s');" % (table, day_time, topic, message, qos)
    db.insert_data(sql)

# 连接成功回调函数,客户端连接到MQTT代理
def on_connect(mqttc, obj, rc) :
    pass
    # print("OnConnetc, rc: " + str(rc))
    # mqttc.subscribe("topic2", qos=1)

def on_publish(mqttc, obj, mid) :
    print("OnPublish, mid: " + str(mid))


# 客户端订阅某个主题
def on_subscribe(mqttc, obj, mid, granted_qos) :
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string) :
    # print("Log:"+string)
    if str.__contains__(string, 'Mid: ') :
        global messageId
        messageId = string.split('Mid: ')[1][0 :1]


# 消息推送回调函数
def on_message(mqttc, obj, msg) :
    sub_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global messageId
    sub_topic = msg.topic
    sub_qos = msg.qos
    sub_payload = msg.payload.decode("utf8")
    # insert_data_into_memsql('login_sub',messageId,sub_time,sub_topic,sub_payload,sub_qos)

    if sub_topic != 'disconnected' :
        print "messageId:%s,sub_time:%s,sub_topic:%s,sub_payload:%s,sub_qos:%s" % (messageId, sub_time, sub_topic, sub_payload, sub_qos)
        try:
            result = impl_controller.impl_controller(msg.topic, str(sub_payload))
        except Exception as e:
            print >> sys.stderr, "{0}".format(e)
            return
        if result:
            for item in result :
                pub_topic = item.get("topic")
                pub_payload = item.get("mes")
                pub_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # insert_data_into_memsql('login_pub',messageId,pub_time,pub_topic,pub_payload,'2')
                print "messid:%s,pub_time:%s,topic:%s,payload:%s" % (messageId, pub_time, pub_topic, pub_payload)
                publish.single(pub_topic, payload=pub_payload, qos=2, hostname="121.199.14.95")
    elif sub_topic == 'disconnected' :
        print sub_payload
    else :
        return
# 创建订阅者
def create_subject(topic) :
    clean_session = False
    if topic == 'disconnected' :
        clean_session = True
    mqttc = mqtt.Client(client_id='mj_server_%s' % topic, clean_session=clean_session)
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log

    # mqttc.will_set("disconnect", "connection broken,u_id:10011", mqtt_qos)
    if mqtt_port != 1883 :
        # 加密
        mqttc.tls_set(ca_certs, certfile=certfile, keyfile=keyfile)
        # 不需要验证ip地址
        mqttc.tls_insecure_set(insecure)

    mqttc.connect('121.199.14.95', 1883, 60)
    mqttc.subscribe(topic, mqtt_qos)
    mqttc.loop_forever()


# 创建房间监听线程
def create_thread(topic_value) :
    try :
        topic = str(topic_value)
        print topic
        thread = threading.Thread(target=create_subject, args=(topic,))
        thread.start()
        # thread.join()
    except Exception as e :
        traceback.print_exc()
        raise e


def main(topic) :
    try :
        create_thread(topic)

    except Exception as e :
        traceback.print_exc()
        raise e


if __name__ == "__main__" :
    main("login")  # 登录注册
    main("create_room")  # 登录注册
    main("enter_room")  # 进入房间
    main("stop_game")  # 终止游戏
    main("signout_room")  # 退出房间
    main("start_mj")  # 首局开始游戏
    main("play_mj")  # 麻将游戏
    main("disconnected")  # 客户端异常断线
