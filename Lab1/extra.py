import random
import paho.mqtt.client as mqttclient
import time
import json
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "sNxR6bc2MHSZKzeoIViJ"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")

def getLocation():
    options = Options()
    options.add_argument("--use--fake-ui-for-media-stream")
    driver = webdriver.Chrome(executable_path = 'D:\Application\chromedriver_win32\chromedriver.exe',options=options)
    timeout = 20
    driver.get("https://www.google.com/maps/")
    wait = WebDriverWait(driver, timeout)
    time.sleep(5)
    
    locatingButton = driver.find_element_by_xpath('//*[@id="pWhrzc-mylocation"]/div')
    locatingButton.click()
    time.sleep(2)
    url = driver.current_url
    res = url[url.find("@") + 1:].split(",")
    return (float(res[0]), float(res[1]))

client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
light_intesity = 100
counter = 0

while True:
    latitude, longitude = getLocation()
    collect_data = {'temperature': temp, 'humidity': humi, 'light':light_intesity, 'longitude': longitude, 'latitude': latitude}
    temp += 1
    humi += 1
    light_intesity += 1
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    time.sleep(5)
