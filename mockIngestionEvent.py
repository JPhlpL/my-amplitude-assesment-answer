import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

AMPLITUDE_API_URL = "https://api2.amplitude.com/2/httpapi"

# Step 1: Create a mock HubSpot event structure
mock_hubspot_event = {
    "appId": 123456,
    "portalId": 7890123,
    "recipient": "mock_user@example.com",
    "type": "TEST",
    "timestamp": int(time.time()),  # current time in seconds
    "hs_email_campaign_id": 4567890,
    "hs_email_id": 1234567,
    "sendId": "abc123-def456-ghi789",
    "smtpId": "202503240001.abc123@example.com",
    "dropReason": "MOCK_REASON",
    "dropMessage": "This is a test mock event.",
    "messageIdHash": "abcdef1234567890",
    "sentBy": "sender@example.com"
}

# Step 2: Transform it into Amplitude format
amplitude_event = {
    "user_id": mock_hubspot_event["recipient"],
    "event_type": f"[HubSpot] EMAIL_{mock_hubspot_event['type']}",
    "time": mock_hubspot_event["timestamp"] * 1000,
    "event_properties": {
        "portalId": mock_hubspot_event["portalId"],
        "appId": mock_hubspot_event["appId"],
        "hs_email_campaign_id": mock_hubspot_event["hs_email_campaign_id"],
        "hs_email_id": mock_hubspot_event["hs_email_id"],
        "sendId": mock_hubspot_event["sendId"],
        "smtpId": mock_hubspot_event["smtpId"],
        "dropReason": mock_hubspot_event["dropReason"],
        "dropMessage": mock_hubspot_event["dropMessage"],
        "messageIdHash": mock_hubspot_event["messageIdHash"],
        "sentBy": mock_hubspot_event["sentBy"],
        "debug": True,
        "source": "mock_test"
    }
}

# Step 3: Wrap into final payload
payload = {
    "api_key": os.getenv("AMPLITUDE_API_KEY"),
    "events": [amplitude_event]
}

# Step 4: Send to Amplitude
response = requests.post(
    AMPLITUDE_API_URL,
    headers={"Content-Type": "application/json"},
    json=payload
)

# Step 5: Print result
print("📨 Sent mock event to Amplitude.")
print("Status Code:", response.status_code)
print("Response:", response.json())
