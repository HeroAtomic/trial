import random
import time
import db
import paho.mqtt.client as mqtt
import json

# Set broker to localhost if running on pi, use broker address if running on Windows.
broker = "test.mosquitto.org"

# Some open MQTT brokers you can use to test
#broker = "test.mosquitto.org"
#broker = "iot.eclipse.org"
#broker = "broker.hivemq.com"

# Which topic to post to
topic = "VRALsensors/lobby"

client = mqtt.Client("VRAL1")
if broker:
    try:
        client.connect(broker)
    except:
        print("Couldn't connect to MQTT broker at address " + broker + ". Continuing without MQTT.")

# Set deployed = True if you are using Pi
deployed = False

# Imports for Pi and connected sensors only
if deployed:
    import RPi.GPIO as GPIO
    import LED
    import HDC2080
    HDC2000 = HDC2080.Pi_HDC2080()

    # Init all GPIO
    # Set Broadcom SOC channel pin numbering
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)


mask_ratio = []

# Faking this for now
capacity = 10


def init_data():
    db.init_db()


# Function to set the LED color based on capacity
def set_led(sensor_data):
    if deployed:
        if sensor_data["people"] >= capacity:
            LED.red()
        elif sensor_data["people"] >= (capacity*0.90):
            LED.orange()
        else:
            LED.green()
    return


# Function to get Humidity from Sensor
def get_sensor_humidity():
    if deployed:
        humidity = round(HDC2000.readHumidity(), 2)
    else:
        humidity = random.randint(0, 100)
    return humidity


# function to get Temperature from Sensor
def get_sensor_temperature():
    if deployed:
        temperature = round(HDC2000.readTemperature(), 2)
    else:
        temperature = random.randint(15, 25)
    return temperature


def get_sensor_people():
    return random.randint(0, 12)


def get_sensor_data():
    return dict({"timestamp": int(time.time() * 1000),
                 "temperature": get_sensor_temperature(),
                 "humidity": get_sensor_humidity(),
                 "people": get_sensor_people()})


def append_db_sensor_data(sensor_data):
    db.insert_sensor_data(sensor_data["timestamp"], sensor_data["temperature"], sensor_data["humidity"], sensor_data["people"])


def update_timeseries_data():
    global mask_ratio
    sensor_data = get_sensor_data()
    print(sensor_data)
    set_led(sensor_data)
    append_db_sensor_data(sensor_data)
    total_people = sensor_data["people"]
    wearing_mask = total_people - random.randint(0, total_people)
    not_wearing_mask = total_people - wearing_mask
    mask_ratio = [{"name": "Yes", "value": wearing_mask},
                  {"name": "No", "value": not_wearing_mask}]


def get_timeseries_data():
    return db.get_all_sensor_data()


def get_mask_ratio():
    global mask_ratio
    return mask_ratio


def update_loop():
    db.init_db()
    while True:
        update_timeseries_data()
        mqtt_data = json.dumps(get_sensor_data())
        print("publishing data" + str(client.is_connected()))
        ## client.publish(topic, mqtt_data)
        time.sleep(5)
