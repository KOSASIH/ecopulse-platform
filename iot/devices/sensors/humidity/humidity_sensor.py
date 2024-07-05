import coapthon.client.helperclient
import time
import Adafruit_DHT

# CoAP server address
COAP_SERVER_ADDRESS = "localhost"
COAP_SERVER_PORT = 5683

# Humidity sensor pin
HUMIDITY_SENSOR_PIN = 17

# Create CoAP client
client = coapthon.client.helperclient.CoAPClient()

# Connect to CoAP server
client.connect(COAP_SERVER_ADDRESS, COAP_SERVER_PORT)

while True:
    # Read humidity data from sensor
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, HUMIDITY_SENSOR_PIN)

    # Publish humidity data to CoAP server
    client.post("humidity", humidity)

    # Wait for 1 minute before sending next reading
    time.sleep(60)
