from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import time
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()


# --- SCHEMA DEFINITIONS ---

class AmplitudeEvent(BaseModel):
    user_id: str
    event_type: str
    time: Optional[int] = None  # If not provided, default to now
    event_properties: Optional[Dict[str, Any]] = None


# --- ENDPOINTS ---

@app.get("/health-check")
async def health_check_endpoint() -> JSONResponse:
    return JSONResponse({"status": "up"})


@app.post("/send-event")
async def send_event_to_amplitude(event: AmplitudeEvent) -> JSONResponse:
    # Use current time in ms if not provided
    event_time = event.time if event.time else int(time.time() * 1000)

    payload = {
        "api_key": os.getenv("AMPLITUDE_API_KEY"),
        "events": [{
            "user_id": event.user_id,
            "event_type": event.event_type,
            "time": event_time,
            "event_properties": event.event_properties or {}
        }]
    }

    response = requests.post(
        "https://api2.amplitude.com/2/httpapi",
        headers={"Content-Type": "application/json"},
        json=payload
    )

    try:
        result = response.json()
    except Exception:
        result = {"error": "Invalid response from Amplitude", "status_code": response.status_code}

    return JSONResponse({
        "status_code": response.status_code,
        "amplitude_response": result
    })


# --- RUN APP LOCALLY ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


"""
Sample Payload:
POST: /send-event
{
  "user_id": "test@example.com",
  "event_type": "[HubSpot] EMAIL_TEST",
  "event_properties": {
    "source": "manual_test",
    "debug": true
  }
}
"""