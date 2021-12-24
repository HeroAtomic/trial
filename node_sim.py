import paho.mqtt.client as mqtt
import random
import time
import json
from numpy.random import choice
# Set broker to localhost if running on pi, use broker address if running on Windows.
broker = "broker.hivemq.com"
NUM_NODES=20

# Some open MQTT brokers you can use to test
#broker = "test.mosquitto.org"
#broker = "iot.eclipse.org"
#broker = "broker.hivemq.com"

def name_gen(idx):
    return "NODE_"+str(idx)

node_names = list(map(name_gen, range(0, NUM_NODES)))

print("Initialized node pool: ", str(node_names))

# Which topic to post to
topic_prefix = "VRALsensors/"

client = mqtt.Client("VRAL1")

client.connect(broker)

# Set deployed = True if you are using Pi
deployed = False


# Function to get Humidity from Sensor
def get_sensor_humidity(result):
    if deployed:
        humidity = result.humidity
    else:
        humidity = random.randint(0, 75)
        print('Random humidity, set deployed = True if using Pi')
    return humidity


# function to get Temperature from Sensor
def get_sensor_temperature(result):
    if deployed:
        temperature = result.temperature
    else:
        temperature = random.randint(15, 25)
        print('Random temperature, set deployed = True if using Pi')
    return temperature


def get_sensor_people():
    return random.randint(0, 12)

def check_problems(sensor_data_dict):
    return (sensor_data_dict["humidity"] > sensor_data_dict["maxhumidity"] or
                sensor_data_dict["humidity"] > sensor_data_dict["maxhumidity"] or
                sensor_data_dict["people"] > sensor_data_dict["maxpeople"])

def get_sensor_data():
    read = 0
    sensor_data_dict = dict({"timestamp": int(time.time() * 1000),
                 "temperature": get_sensor_temperature(read),
                 "maxtemperature": 24,
                 "humidity": get_sensor_humidity(read),
                 "maxhumidity": 50,
                 "people": get_sensor_people(),
                 "maxpeople": 10})
    sensor_data_dict["status"] = check_problems(sensor_data_dict)

    return sensor_data_dict

def update_timeseries_data():
    global mask_ratio
    sensor_data = get_sensor_data()
    print(sensor_data)
    total_people = sensor_data["people"]
    wearing_mask = total_people - random.randint(0, total_people)
    not_wearing_mask = total_people - wearing_mask
    mask_ratio = [{"name": "Yes", "value": wearing_mask},
                  {"name": "No", "value": not_wearing_mask}]

while True:
    for node_name in node_names:
        mqtt_data = json.dumps(get_sensor_data())
        print("publishing data" + str(client.is_connected()))
        client.publish(topic_prefix+node_name, mqtt_data)
        time.sleep(1)
    time.sleep(10)