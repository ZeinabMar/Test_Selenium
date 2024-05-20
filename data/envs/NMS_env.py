
from pytest_sina_framework import SecretText

DICT__SERVER = {
    'type': "NMS_Server",
    'server_ip': "192.168.9.127",
    'server_host': "http://192.168.5.183/auth/login",
    "webdriver" : "Firefox"
    }
    
DICT__ENV = {
    'olt_nms': DICT__SERVER
}


