import paho.mqtt.client as mqtt
import time
import Adafruit_DHT

# MQTT broker address
MQTT_BROKER_ADDRESS = "localhost"
MQTT_BROKER_PORT = 1883

# Temperature sensor pin
TEMPERATURE_SENSOR_PIN = 17

# Create MQTT client
client = mqtt.Client()

# Connect to MQTT broker
client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT)

while True:
    # Read temperature data from sensor
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, TEMPERATURE_SENSOR_PIN)

    # Publish temperature data to MQTT broker
    client.publish("temperature", temperature)

    # Wait for 1 minute before sending next reading
    time.sleep(60)
