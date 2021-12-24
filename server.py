import os
from flask import Flask
from flask_cors import CORS
from flask import request
import data_generator
import threading
import json
import db
import paho.mqtt.client as mqtt
import traceback

broker="broker.hivemq.com"
topic="VRALsensors/#"

# On message call back (what do do with message when one is received)
# Using for testing right now, doesn't actually do anything other than print the message.
# In the future, the master node will read the messages and do something.
def on_message(client, userdata, message):
    print("data received topic", message.topic)
    node_name = str(message.topic).split("/")[1]
    sensor_dict=json.loads(str(message.payload.decode("utf-8","ignore")))
    try:
        db.insert_node_data_master_db(node_name, sensor_dict["timestamp"], sensor_dict["temperature"], sensor_dict["maxtemperature"],
                                      sensor_dict["humidity"], sensor_dict["maxhumidity"], sensor_dict["people"], sensor_dict["maxpeople"], sensor_dict["status"])
    except Exception:
        traceback.print_exc()
    print("Recieved message: " + str(sensor_dict))

# On Connect callback
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code ", str(rc))
    print("Subscribing to topic " + topic)
    client.subscribe(topic)
    db.init_master_db()

# Connect to broker to monitor messages
print("Creating new instance...")
client = mqtt.Client()
client.on_message=on_message
client.on_connect=on_connect
if broker:
    print("Connecting to broker")
    try:
        client.connect(broker)
        client.loop_start()
    except:
        print("Couldn't connect to MQTT broker at address " + broker + ". Continuing without MQTT.")

def background():
    data_generator.update_loop()

# Only spawn one thread when in debug mode
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    t = threading.Thread(target=background)
    t.start()

app = Flask(__name__)
CORS(app)

@app.route('/sensor-data')
def sensor_data():
    print(db.get_all_sensor_data())
    return json.dumps(data_generator.get_timeseries_data())

@app.route('/node-meta')
def node_meta():
    print(db.get_all_node_meta())
    return json.dumps(db.get_all_node_meta())

@app.route('/mask-ratio')
def mask_ratio():
    return json.dumps(data_generator.get_mask_ratio())

@app.route('/settings', methods=['PATCH'])
def settings():
    if request.method == 'PATCH':
        request_data = json.loads(request.data)
        db.update_settings(request_data['name'], request_data['value'])
    return "success"

@app.route('/master-node-data')
def master_node_data():
    print(db.get_master_node_data())
    return json.dumps(db.get_master_node_data())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    print ("Running!")