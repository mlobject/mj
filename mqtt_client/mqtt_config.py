__author__ = 'hu'


# mqtt_host = "192.168.99.100"
mqtt_host = "127.0.0.1"
mqtt_port = 1883
# mqtt_port = 8883
mqtt_keepalive = 60
mqtt_qos = 2
mqtt_will_topic = "disconnect"

ca_certs = "../tls/ca.crt"
certfile = "../tls/client.crt"
keyfile = "../tls/client.key",
insecure = True

