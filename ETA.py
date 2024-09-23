import requests
from twilio.rest import Client
import schedule
import time
from datetime import datetime

GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "YOUR_TWILIO_PHONE_NUMBER"
TO_PHONE_NUMBER = "YOUR_PHONE_NUMBER"

ORIGIN = "set location"
DESTINATION = "set location"

def get_eta():
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": ORIGIN,
        "destinations": DESTINATION,
        "key": GOOGLE_MAPS_API_KEY,
        "mode": "driving"
    }
    response = requests.get(url, params=params)
    data = response.json()

    try:
        travel_time = data["rows"][0]["elements"][0]["duration"]["text"]
        return travel_time
    except (KeyError, IndexError):
        return "Error retrieving travel time"

def send_sms(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body = message,
        from_ = TWILIO_PHONE_NUMBER,
        to = TO_PHONE_NUMBER
    )

def send_eta_message():
    travel_time = get_eta()
    message = f"Good morning! Your estimated travel time from {ORIGIN} to {DESTINATION} is {travel_time}."
    send_sms(message)
    print(f"Message sent at {datetime.now()}: {message}")

schedule.every().day.at("08:00").do(send_eta_message)

print("Will send SMS at 8:00 AM every day.")

while True:
    schedule.run_pending()
    time.sleep(60)