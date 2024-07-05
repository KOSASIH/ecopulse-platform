import bacnet

# Define BACnet settings
BACNET_HOST = "localhost"
BACNET_PORT = 47808

# Define building systems
HVAC_SYSTEM = "HVAC-1"
LIGHTING_SYSTEM = "Lighting-1"

# Create BACnet connection
bacnet_conn = bacnet.Connection(BACNET_HOST, BACNET_PORT)

# Define automation logic
def automate_hvac():
    # Get current temperature
    temp = bacnet_conn.read_property(HVAC_SYSTEM, "temperature")

    # Check if temperature is too high
    if temp > 25:
        # Turn on cooling
        bacnet_conn.write_property(HVAC_SYSTEM, "mode", "cooling")
    else:
        # Turn off cooling
        bacnet_conn.write_property(HVAC_SYSTEM, "mode", "off")

def automate_lighting():
    # Get current time
    time = datetime.datetime.now()

    # Check if it's daytime
    if time.hour >= 8 and time.hour <= 18:
        # Turn on lights
        bacnet_conn.write_property(LIGHTING_SYSTEM, "state", "on")
    else:
        # Turn off lights
        bacnet_conn.write_property(LIGHTING_SYSTEM, "state", "off")

# Run automation logic every 15 minutes
while True:
    automate_hvac()
    automate_lighting()
    time.sleep(900)  # 15 minutes
