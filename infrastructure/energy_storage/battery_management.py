import ocpp
import datetime

# OCPP connection settings
OCPP_HOST = "localhost"
OCPP_PORT = 8080

# Battery settings
BATTERY_CAPACITY = 100  # kWh
BATTERY_CHARGE_RATE = 50  # kW
BATTERY_DISCHARGE_RATE = 50  # kW

# Create OCPP connection
ocpp_conn = ocpp.Connection(OCPP_HOST, OCPP_PORT)

# Define charging and discharging logic
def charge_battery():
    # Check if battery is not fully charged
    if ocpp_conn.get_battery_level() < BATTERY_CAPACITY:
        # Start charging
        ocpp_conn.start_charging(BATTERY_CHARGE_RATE)
        print("Charging battery...")
    else:
        print("Battery is fully charged.")

def discharge_battery():
    # Check if battery is not empty
    if ocpp_conn.get_battery_level() > 0:
        # Start discharging
        ocpp_conn.start_discharging(BATTERY_DISCHARGE_RATE)
        print("Discharging battery...")
    else:
        print("Battery is empty.")

# Define scheduling logic
def schedule_charging():
    # Check if it's peak hour (e.g. 12pm-4pm)
    if datetime.datetime.now().hour >= 12 and datetime.datetime.now().hour <= 16:
        # Charge battery during peak hour
        charge_battery()
    else:
        # Discharge battery during off-peak hour
        discharge_battery()

# Run scheduling logic every 15 minutes
while True:
    schedule_charging()
    time.sleep(900)  # 15 minutes
