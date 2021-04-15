from Gateway import IOT_Database as db
from Gateway import WEB_Database as db_web
import paho.mqtt.client as mqtt
import datetime as dt
import json

threshold_device = 30
broker_address = "raspberrypi.local"
broker_subscribing_url = "/isha/#"
node_id = "Server"

db_iot = db.IOT_Database()
db_iot.create_table()
db_web_app = db_web.WEB_Database()
db_web_app.create_table()


# MQTT_Functions_Start
def on_log(client, userdata, level, buf):
    print("log: " + buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
        client.subscribe(broker_subscribing_url)
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("DisConnected result code" + str(rc))


def on_message(client, userdata, message):
    message = str(message.payload.decode("utf-8"))
    extract_message(message)


def extract_message(message):
    #     print('Extract')
    message = json.loads(message)
    table_name = message.pop('Type')
    #     print(type(message))
    message['Timestamp'] = dt.datetime.now()
    db_iot.insert_value(table_name, message)


def publishing_command():
    for el in db_web_app.ret_config_list():
        client.publish('/isha/' + el[1] + '/conf', json.dumps({"Time_Intreval": el[2]}))
        print('/isha/' + el[1] + '/conf' + str(el[2]))


# MQTT_Functions_End
broker = broker_address
client = mqtt.Client(node_id, clean_session=True)
client.on_connect = on_connect
client.on_log = on_log
client.on_disconnect = on_disconnect
client.on_message = on_message
print("Connecting to broker", broker)
client.connect(broker)
while (1):
    client.loop()
    publishing_command()
client.disconnect()

