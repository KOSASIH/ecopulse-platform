from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import coapthon.client.helperclient

app = Flask(__name__)

# Define MQTT and CoAP clients
mqtt_client = mqtt.Client()
coap_client = coapthon.client.helperclient.CoAPClient()

# Define API endpoints
@app.route("/iot/devices", methods=["GET"])
def get_devices():
    # Get list of IoT devices
    devices = []
    for device in mqtt_client.get_devices():
        devices.append({"id": device, "status": mqtt_client.get_device_status(device)})
    return jsonify({"devices": devices})

@app.route("/iot/devices/<device_id>/data", methods=["GET"])
def get_device_data(device_id):
    # Get sensor data from IoT device
    data = mqtt_client.get_device_data(device_id)
    return jsonify({"data": data})

@app.route("/iot/devices/<device_id>/control", methods=["POST"])
def control_device(device_id):
    # Control IoT device
    command = request.json["command"]
    mqtt_client.send_command(device_id, command)
    return jsonify({"status": "success"})

@app.route("/iot/devices/<device_id>/coap", methods=["GET"])
def get_coap_data(device_id):
    # Get CoAP data from IoT device
    data = coap_client.get(device_id)
    return jsonify({"data": data})

if __name__ == "__main__":
    app.run(debug=True)
