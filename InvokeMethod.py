#####################################################################################################################
#############################    Author  : Ehab Magdy Abdullah                      #################################
#############################    Linkedin: https://www.linkedin.com/in/ehabmagdyy/  #################################
#############################    Youtube : https://www.youtube.com/@EhabMagdyy      #################################
#####################################################################################################################

import requests
import json
from datetime import datetime, timedelta, timezone
import hmac
import hashlib
import base64
import time

# Replace these with your IoT Hub details
IOT_HUB_NAME = "ehabhub"
DEVICE_ID = "ehabdev"
SHARED_ACCESS_KEY = "dkY4wgayKjkhrmA4XCRWYbbl/f+mHceWBAIoTFqVYV0="
SHARED_ACCESS_KEY_NAME = "iothubowner"

# Generate the SAS token
def generate_sas_token(uri, key, policy_name, expiry=3600):
    ttl = datetime.now(timezone.utc) + timedelta(seconds=expiry)
    sign_key = f"{uri}\n{int(ttl.timestamp())}"
    signature = base64.b64encode(
        hmac.HMAC(base64.b64decode(key), sign_key.encode("utf-8"), hashlib.sha256).digest()
    ).decode()
    token = f"SharedAccessSignature sr={uri}&sig={signature}&se={int(ttl.timestamp())}"
    if policy_name:
        token += f"&skn={policy_name}"
    return token

# Build the IoT Hub endpoint URL
IOT_HUB_ENDPOINT = f"{IOT_HUB_NAME}.azure-devices.net"
URI = f"{IOT_HUB_ENDPOINT}/twins/{DEVICE_ID}/methods"

# Add the API version to the URL
API_VERSION = "2021-04-12"  # Use the latest supported API version
URI_WITH_VERSION = f"{URI}?api-version={API_VERSION}"

# Generate the SAS token
sas_token = generate_sas_token(IOT_HUB_ENDPOINT, SHARED_ACCESS_KEY, SHARED_ACCESS_KEY_NAME)

# Define the headers
headers = {
    "Authorization": sas_token,
    "Content-Type": "application/json"
}

# Function to invoke a method
def invoke_method(method_name, payload):
    method_payload = {
        "methodName": method_name,
        "payload": payload,
        "responseTimeoutInSeconds": 30
    }
    response = requests.post(
        f"https://{URI_WITH_VERSION}",
        headers=headers,
        data=json.dumps(method_payload)
    )
    if response.status_code == 200:
        print(f"Method '{method_name}' invoked successfully!")
        print("Response from device:", response.json())
    else:
        print(f"Failed to invoke method '{method_name}'. Status code: {response.status_code}")
        print("Error details:", response.text)

# toggle LED on and off
while True:
    # Turn LED on
    invoke_method("led_on", {})
    time.sleep(3)

    # Turn LED off
    invoke_method("led_off", {})
    time.sleep(3)