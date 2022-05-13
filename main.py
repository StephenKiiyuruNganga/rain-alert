import requests
import os
from twilio.rest import Client

# --------------------- test locations for weather ------------------------- #
nairobi = {
    "lat": -1.292066,
    "lon": 36.821945
}

guangzhou = {
    "lat": 23.129110,
    "lon": 113.264381
}


# ---------------------  open weather api setup ------------------------- #
one_call_api = "https://api.openweathermap.org/data/2.5/onecall?"
api_key = os.environ['OWM_API_KEY']
one_call_params = {
    "lat": guangzhou["lat"],
    "lon": guangzhou["lon"],
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

# --------------------- twilio env variables ------------------------- #
account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_API_KEY']
steve_phone_number = "+254729666912"
twilio_phone_number = "+12398936281"

# --------------------- check for rain & send sms ------------------------- #
response = requests.get(url=one_call_api, params=one_call_params)
response.raise_for_status()
data = response.json()
status = response.status_code

will_rain = False

for hour in data["hourly"][:12]:
    if hour["weather"][0]["id"] < 700:
        will_rain = True

if will_rain:
    # send message
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remeber to bring an umbrella",
        from_=twilio_phone_number,
        to=steve_phone_number
    )
    print(message.status)
