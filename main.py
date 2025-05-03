import requests
import os
from dotenv import load_dotenv
from defaults import (
    HUBSPOT_API_OAUTH_URL,
    AMPLITUDE_API_URL,
    HUBSPOT_API_EVENTS_URL
)

load_dotenv() 

def get_hubspot_access_token(url):
    data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "refresh_token": os.getenv("REFRESH_TOKEN"),
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_hubspot_email_events(url, token, count=50):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "count": count
    }
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get("events", [])


def transform_to_amplitude(hs_event):
    amplitude_event_type = f"[HubSpot] EMAIL_{hs_event['type']}"
    return {
        "user_id": hs_event["recipient"],
        "event_type": amplitude_event_type,
        "time": hs_event["timestamp"] * 1000,
        "event_properties": {
            "portalId": hs_event.get("portalId"),
            "appId": hs_event.get("appId"),
            "hs_email_campaign_id": hs_event.get("hs_email_campaign_id"),
            "hs_email_id": hs_event.get("hs_email_id"),
            "sendId": hs_event.get("sendId"),
            "smtpId": hs_event.get("smtpId"),
            "dropReason": hs_event.get("dropReason"),
            "dropMessage": hs_event.get("dropMessage"),
            "messageIdHash": hs_event.get("messageIdHash"),
            "sentBy": hs_event.get("sentBy"),
        },
    }


def send_to_amplitude(events, url):
    payload = {
        "api_key": os.getenv("AMPLITUDE_API_KEY"), 
        "events": events
    }
    resp = requests.post(
        AMPLITUDE_API_URL, json=payload, headers={"Content-Type": "application/json"}
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    # 1) Get a fresh HubSpot access token
    token = get_hubspot_access_token(HUBSPOT_API_OAUTH_URL)
    # 2) Fetch the email events list
    hs_events = fetch_hubspot_email_events(HUBSPOT_API_EVENTS_URL, token)
    
    # 3) Transform each event into Amplitude format
    amp_events = [transform_to_amplitude(e) for e in hs_events]
    # 4) Send the batch to Amplitude
    result = send_to_amplitude(amp_events, AMPLITUDE_API_URL)
    print("Amplitude response:", result)
