import network, time, machine, urequests, os, math, json
from umqtt.simple import MQTTClient
from machine import ADC

# –––––––––––––––––––––––––––––––––––
# ADC FOR TEMPERATURE SENSOR

adc = ADC(26)  # Thermistor

def read_temperature():
    adc_value = adc.read_u16()
    voltage = adc_value / 65535 * 3.3
    resistance = 10 * voltage / (3.3 - voltage)
    temp_c = round(1/(1/(273.15+25) + math.log(resistance/10)/3950) - 273.15)
    return adc_value, voltage, temp_c

# –––––––––––––––––––––––––––––––––––
# WI-FI MODULE

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("**-obývák-****", "*******")

for _ in range(10):  # Connection timeout 10 seconds
    if wlan.status() == 3: break
    print('Connecting...')
    time.sleep(1)
else:
    raise RuntimeError('Wi-Fi connection failed')

print(f'Connected | IP: {wlan.ifconfig()[0]}')

# –––––––––––––––––––––––––––––––––––
# AZURE IOT HUB CONFIGURATION & MQTT CONNECTION

HUB_NAME = 'pipicotest.azure-devices.net'
CLIENT_ID = 'rasp-pico'
SAS_TOKEN = 'SharedAccessSignature sr=pipicotest.azure-devices.net%2Fdevices%2Frasp-pico&sig=*****&se=1744980603'

def mqtt_connect():
    # DigiCert Certificate DER File (from https://www.digicert.com/kb/digicert-root-certificates.htm)
    # SSL/TLS encryption. Device uses the needed certificate (cryptographic credentials) ...
    # ... for authentication and encryption when connecting via MQTT over TLS.
    # Azure IoT Hub requires a certificate.

    # Loading certificate from Pico's filesystem
    with open("digicert.der", 'rb') as f: # Path relative to Pico's root
        ssl_params = {'cadata': f.read()}
    
    client = MQTTClient(
        client_id=CLIENT_ID, server=HUB_NAME, port=8883,
        user=f'{HUB_NAME}/{CLIENT_ID}/?api-version=2021-04-12',
        password=SAS_TOKEN, keepalive=3600, ssl=True, ssl_params=ssl_params
    )
    client.connect()
    print('Connected to Azure IoT Hub')
    return client

# –––––––––––––––––––––––––––––––––––
# MESSAGE HANDLING

def callback_handler(topic, msg):
    print(f"Message received: {topic.decode()} > {msg.decode()}")
    if msg.strip() == b'get_temp':
        send_temperature_data()

def send_temperature_data():
    try:
        adc_val, volts, temp = read_temperature()
        client.publish(
            b'devices/rasp-pico/messages/events/',
            json.dumps({'temperature': temp, 'voltage': round(volts, 2), 'adc_value': adc_val})
        )
        print(f"Published: {temp}°C, {volts:.2f}V, {adc_val}")
    except Exception as e:
        print(f"Publish error: {e}")

# –––––––––––––––––––––––––––––––––––
# MAIN LOOP

try:
    client = mqtt_connect()
    client.set_callback(callback_handler)
    client.subscribe(f'devices/{CLIENT_ID}/messages/devicebound/#')
except OSError:
    machine.reset()

last_temp, interval = time.ticks_ms(), 300_000  # 5 minutes

while True:
    try:
        client.check_msg()
        if time.ticks_diff(time.ticks_ms(), last_temp) >= interval:
            send_temperature_data()
            last_temp = time.ticks_ms()
        time.sleep(0.1)
    except OSError as e:
        print(f"Connection error: {e}")
        machine.reset()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
