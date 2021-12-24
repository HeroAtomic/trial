import sqlite3

def init_db():
    connection = sqlite3.connect('sensor-data.db')
    cursor = connection.cursor()
    init_command = """CREATE TABLE IF NOT EXISTS
sensordata(timestamp INTEGER PRIMARY KEY, temperature INTEGER, humidity INTEGER, people INTEGER)
"""
    cursor.execute(init_command)
    init_command = """CREATE TABLE IF NOT EXISTS
    nodemeta(name TEXT PRIMARY KEY, value TEXT)
    """
    cursor.execute(init_command)
    cursor.execute("INSERT OR IGNORE INTO nodemeta VALUES ('nodeName', 'NODE A')")
    cursor.execute("INSERT OR IGNORE INTO nodemeta VALUES ('location', '123 Main street')")
    cursor.execute("INSERT OR IGNORE INTO nodemeta VALUES ('roomcapacity', '9')")
    connection.commit()

def insert_sensor_data(timestamp, temperature, humidity, people):
    connection = sqlite3.connect('sensor-data.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO sensordata VALUES ("+str(timestamp)+", "+str(temperature)+", "+str(humidity)+", "+str(people)+")")
    connection.commit()

def get_all_sensor_data():
    connection = sqlite3.connect('sensor-data.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sensordata")
    results = cursor.fetchall()
    formatted_results = []
    for row in results:
        d = dict(zip(row.keys(), row))  # a dict with column names as keys
        formatted_results.append(d)
    return formatted_results

def get_all_node_meta():
    connection = sqlite3.connect('sensor-data.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM nodemeta")
    results = cursor.fetchall()
    formatted_results = []
    for row in results:
        d = dict(zip(row.keys(), row))  # a dict with column names as keys
        formatted_results.append(d)
    return formatted_results

def update_settings(name, value):
    connection = sqlite3.connect('sensor-data.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    print("UPDATE nodemeta SET value = '"+ str(value) +"' WHERE name = '" + str(name) + "'")
    cursor.execute("UPDATE nodemeta SET value = '"+ str(value) +"' WHERE name = '" + str(name) + "'")
    connection.commit()
    cursor.execute("SELECT * FROM nodemeta")
    results = cursor.fetchall()
    formatted_results = []
    for row in results:
        d = dict(zip(row.keys(), row))  # a dict with column names as keys
        formatted_results.append(d)
    return formatted_results

#### Master DB functions

def init_master_db():
    connection = sqlite3.connect('master-data.db')
    cursor = connection.cursor()
    init_command = """CREATE TABLE IF NOT EXISTS
masterdata(nodename TEXT PRIMARY KEY, timestamp INTEGER, temperature INTEGER, maxtemperature INTEGER, humidity INTEGER, maxhumidity INTEGER, people INTEGER, maxpeople INTEGER, status INTEGER)
"""
    cursor.execute(init_command)

def insert_node_data_master_db(name, timestamp, temperature, maxtemperature, humidity, maxhumidity, people, maxpeople, status):
    print("Max people: " + str(maxpeople))
    connection = sqlite3.connect('master-data.db')
    cursor = connection.cursor()
    print("INSERT INTO masterdata VALUES (" + name + ", " + str(timestamp) + ", " + str(temperature) + ", " + str(maxtemperature) + ", " + str(
        humidity) + ", "  + str(maxhumidity) + ", " + str(people) + ", " + str(maxpeople) + ", " + str(status) +")")
    cursor.execute("INSERT INTO masterdata VALUES ('" + name + "', " + str(timestamp) + ", " + str(temperature) + ", " + str(maxtemperature) + ", " + str(
        humidity) + ", "  + str(maxhumidity) + ", " + str(people) + ", " + str(maxpeople) + ", " + str(status) + ") ON CONFLICT(nodename) DO UPDATE SET temperature=excluded.temperature, maxtemperature=excluded.maxtemperature, humidity=excluded.humidity, maxhumidity=excluded.maxhumidity,timestamp=excluded.timestamp, people=excluded.people, maxpeople=excluded.maxpeople, status=excluded.status")
    connection.commit()

def get_master_node_data():
    connection = sqlite3.connect('master-data.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM masterdata")
    results = cursor.fetchall()
    formatted_results = []
    for row in results:
        d = dict(zip(row.keys(), row))  # a dict with column names as keys
        formatted_results.append(d)
    return formatted_results

